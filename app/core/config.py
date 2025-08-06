import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Server settings
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # OpenAI settings
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-3.5-turbo", env="OPENAI_MODEL")
    max_tokens: int = Field(default=1000, env="MAX_TOKENS")
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    
    # GitHub API settings
    github_token: Optional[str] = Field(default=None, env="GITHUB_TOKEN")
    github_rate_limit_delay: float = Field(default=1.0, env="GITHUB_RATE_LIMIT_DELAY")
    min_stars_for_inspiration: int = Field(default=10, env="MIN_STARS_FOR_INSPIRATION")
    
    # Embedding settings
    embedding_model_name: str = Field(default="all-MiniLM-L6-v2", env="EMBEDDING_MODEL_NAME")
    embedding_dimension: int = Field(default=384, env="EMBEDDING_DIMENSION")
    faiss_index_type: str = Field(default="IndexFlatL2", env="FAISS_INDEX_TYPE")
    normalize_vectors: bool = Field(default=True, env="NORMALIZE_VECTORS")
    
    class Config:
        env_file = None  # Disable .env file loading
        case_sensitive = False


# Create settings instance
settings = Settings() 