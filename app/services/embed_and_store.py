import numpy as np
import faiss
from typing import List, Tuple, Dict, Any
from sentence_transformers import SentenceTransformer
import pickle
import os

from app.core.config import settings
from app.models.repository import Repository

class EmbeddingService:
    """Service for generating embeddings and performing semantic search"""
    
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model_name)
        self.index = None
        self.repositories = []
        self.dimension = settings.embedding_dimension
        
        # Initialize FAISS index
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize FAISS index based on configuration"""
        if settings.faiss_index_type == "IndexFlatL2":
            self.index = faiss.IndexFlatL2(self.dimension)
        elif settings.faiss_index_type == "IndexFlatIP":
            self.index = faiss.IndexFlatIP(self.dimension)
        elif settings.faiss_index_type == "IndexIVFFlat":
            # For IVF, we need to train on some data first
            self.index = faiss.IndexFlatL2(self.dimension)  # Start with flat, will convert later
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a text string
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as numpy array
        """
        if not text:
            return np.zeros(self.dimension)
        
        embedding = self.model.encode([text])[0]
        
        if settings.normalize_vectors:
            embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a batch of texts
        
        Args:
            texts: List of text strings
            
        Returns:
            Embeddings as numpy array
        """
        if not texts:
            return np.array([])
        
        # Filter out empty texts
        valid_texts = [text for text in texts if text]
        if not valid_texts:
            return np.array([])
        
        embeddings = self.model.encode(valid_texts)
        
        if settings.normalize_vectors:
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / norms
        
        return embeddings
    
    def add_repositories(self, repositories: List[Repository]):
        """
        Add repositories to the vector store
        
        Args:
            repositories: List of Repository objects
        """
        if not repositories:
            return
        
        # Prepare texts for embedding
        texts = []
        for repo in repositories:
            # Combine repository information for embedding
            text_parts = []
            
            if repo.name:
                text_parts.append(f"Repository: {repo.name}")
            
            if repo.description:
                text_parts.append(f"Description: {repo.description}")
            
            if repo.readme_content:
                # Truncate README to avoid token limits
                readme_preview = repo.readme_content[:2000]  # First 2000 chars
                text_parts.append(f"README: {readme_preview}")
            
            if repo.language:
                text_parts.append(f"Language: {repo.language}")
            
            combined_text = " ".join(text_parts)
            texts.append(combined_text)
        
        # Generate embeddings
        embeddings = self.generate_embeddings_batch(texts)
        
        if len(embeddings) == 0:
            return
        
        # Add to FAISS index
        self.index.add(embeddings.astype('float32'))
        
        # Store repository metadata
        self.repositories.extend(repositories)
    
    def search_similar(self, query: str, top_k: int = 5) -> List[Tuple[Repository, float]]:
        """
        Search for repositories similar to the query
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            
        Returns:
            List of (Repository, similarity_score) tuples
        """
        if not self.repositories or self.index.ntotal == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        query_vector = query_embedding.reshape(1, -1).astype('float32')
        
        # Search in FAISS index
        distances, indices = self.index.search(query_vector, min(top_k, len(self.repositories)))
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.repositories):
                # Convert distance to similarity score (1 - normalized distance)
                similarity_score = 1.0 - (distance / np.max(distances[0]))
                results.append((self.repositories[idx], similarity_score))
        
        return results
    
    def clear_index(self):
        """Clear the vector store"""
        self.index = None
        self.repositories = []
        self._initialize_index()
    
    def save_index(self, filepath: str):
        """
        Save the FAISS index and repository metadata
        
        Args:
            filepath: Path to save the index
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, f"{filepath}.faiss")
        
        # Save repository metadata
        with open(f"{filepath}.pkl", "wb") as f:
            pickle.dump(self.repositories, f)
    
    def load_index(self, filepath: str):
        """
        Load the FAISS index and repository metadata
        
        Args:
            filepath: Path to load the index from
        """
        try:
            # Load FAISS index
            self.index = faiss.read_index(f"{filepath}.faiss")
            
            # Load repository metadata
            with open(f"{filepath}.pkl", "rb") as f:
                self.repositories = pickle.load(f)
                
        except Exception as e:
            print(f"Error loading index: {e}")
            self.clear_index() 