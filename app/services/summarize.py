import openai
from typing import List, Dict, Any
import asyncio

from app.core.config import settings
from app.models.repository import Repository

class SummarizationService:
    """Service for generating AI summaries and learning insights for repositories"""
    
    def __init__(self):
        self.api_key_available = bool(settings.openai_api_key)
        
        if self.api_key_available:
            openai.api_key = settings.openai_api_key
            self.model = settings.openai_model
            self.max_tokens = settings.max_tokens
            self.temperature = settings.temperature
        else:
            print("Warning: OpenAI API key not found. Summarization features will be disabled.")
    
    async def generate_repository_summary(self, repository: Repository) -> Dict[str, Any]:
        """
        Generate comprehensive summary and learning insights for a repository
        
        Args:
            repository: Repository object
            
        Returns:
            Dictionary with summary, key features, learning insights, and implementation tips
        """
        if not self.api_key_available:
            return {
                "summary": "Summarization disabled - OpenAI API key required",
                "key_features": ["API key required for feature analysis"],
                "learning_insights": ["Enable OpenAI API key for learning insights"],
                "implementation_tips": ["Enable OpenAI API key for implementation tips"]
            }
        
        # Prepare context for the AI
        context = self._prepare_repository_context(repository)
        
        # Generate summary
        summary = await self._generate_summary(context)
        
        # Generate key features
        key_features = await self._generate_key_features(context)
        
        # Generate learning insights
        learning_insights = await self._generate_learning_insights(context)
        
        # Generate implementation tips
        implementation_tips = await self._generate_implementation_tips(context)
        
        return {
            "summary": summary,
            "key_features": key_features,
            "learning_insights": learning_insights,
            "implementation_tips": implementation_tips
        }
    
    def _prepare_repository_context(self, repository: Repository) -> str:
        """
        Prepare context string for AI analysis
        
        Args:
            repository: Repository object
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        # Basic repository info
        context_parts.append(f"Repository: {repository.full_name}")
        context_parts.append(f"Description: {repository.description or 'No description'}")
        context_parts.append(f"Language: {repository.language or 'Unknown'}")
        context_parts.append(f"Stars: {repository.stargazers_count}")
        context_parts.append(f"Created: {repository.created_at.strftime('%Y-%m-%d')}")
        context_parts.append(f"Last updated: {repository.updated_at.strftime('%Y-%m-%d')}")
        
        if repository.last_commit_date:
            context_parts.append(f"Last commit: {repository.last_commit_date.strftime('%Y-%m-%d')}")
        
        context_parts.append(f"Inspiration score: {repository.inspiration_score:.2f}")
        
        # README content (truncated for token limits)
        if repository.readme_content:
            readme_preview = repository.readme_content[:3000]  # Limit to 3000 chars
            context_parts.append(f"README Preview:\n{readme_preview}")
        
        return "\n".join(context_parts)
    
    async def _generate_summary(self, context: str) -> str:
        """
        Generate a summary of what the repository does
        
        Args:
            context: Repository context
            
        Returns:
            AI-generated summary
        """
        prompt = f"""
        Based on the following GitHub repository information, provide a concise summary (2-3 sentences) of what this project does and its main purpose:

        {context}

        Focus on the main functionality, purpose, and value of the project.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes GitHub repositories and provides clear, concise summaries of their functionality and purpose."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Unable to generate summary due to an error."
    
    async def _generate_key_features(self, context: str) -> List[str]:
        """
        Generate key features and technologies used in the repository
        
        Args:
            context: Repository context
            
        Returns:
            List of key features
        """
        prompt = f"""
        Based on the following GitHub repository information, identify 3-5 key features, technologies, or architectural patterns used in this project:

        {context}

        Focus on:
        - Programming languages and frameworks
        - Notable libraries or tools
        - Architectural patterns
        - Key functionality
        - Technical innovations

        Provide specific, technical details that would be useful for someone learning from this repository.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that identifies key technical features and technologies in GitHub repositories."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the response into a list of features
            content = response.choices[0].message.content.strip()
            
            # Split by common list indicators and clean up
            features = []
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.') or line.startswith('5.')):
                    # Remove the bullet/number and clean up
                    feature = line.lstrip('-•123456789. ')
                    if feature:
                        features.append(feature)
            
            # If parsing failed, return the whole content as one feature
            if not features:
                features = [content]
            
            return features[:5]  # Limit to 5 features
            
        except Exception as e:
            print(f"Error generating key features: {e}")
            return ["Unable to generate key features due to an error."]
    
    async def _generate_learning_insights(self, context: str) -> List[str]:
        """
        Generate learning insights from the repository
        
        Args:
            context: Repository context
            
        Returns:
            List of learning insights
        """
        prompt = f"""
        Based on the following GitHub repository information, provide 3-5 specific learning insights that a developer could gain from studying this repository:

        {context}

        Consider:
        - Code organization and structure
        - Design patterns and best practices
        - Problem-solving approaches
        - Performance optimizations
        - User experience considerations
        - Testing strategies
        - Documentation practices

        Provide actionable insights that would help someone improve their own projects.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides learning insights from GitHub repositories to help developers improve their skills."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the response into a list of insights
            content = response.choices[0].message.content.strip()
            
            # Split by common list indicators and clean up
            insights = []
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.') or line.startswith('5.')):
                    # Remove the bullet/number and clean up
                    insight = line.lstrip('-•123456789. ')
                    if insight:
                        insights.append(insight)
            
            # If parsing failed, return the whole content as one insight
            if not insights:
                insights = [content]
            
            return insights[:5]  # Limit to 5 insights
            
        except Exception as e:
            print(f"Error generating learning insights: {e}")
            return ["Unable to generate learning insights due to an error."]
    
    async def _generate_implementation_tips(self, context: str) -> List[str]:
        """
        Generate implementation tips for similar features
        
        Args:
            context: Repository context
            
        Returns:
            List of implementation tips
        """
        prompt = f"""
        Based on the following GitHub repository information, provide 3-5 practical implementation tips for someone who wants to build similar features:

        {context}

        Consider:
        - Getting started steps
        - Common pitfalls to avoid
        - Performance considerations
        - Scalability approaches
        - Testing strategies
        - Deployment considerations
        - Maintenance best practices

        Provide specific, actionable tips that could save time and improve quality.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides practical implementation tips for building similar features to those found in GitHub repositories."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the response into a list of tips
            content = response.choices[0].message.content.strip()
            
            # Split by common list indicators and clean up
            tips = []
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.') or line.startswith('5.')):
                    # Remove the bullet/number and clean up
                    tip = line.lstrip('-•123456789. ')
                    if tip:
                        tips.append(tip)
            
            # If parsing failed, return the whole content as one tip
            if not tips:
                tips = [content]
            
            return tips[:5]  # Limit to 5 tips
            
        except Exception as e:
            print(f"Error generating implementation tips: {e}")
            return ["Unable to generate implementation tips due to an error."]
    
    async def generate_batch_summaries(self, repositories: List[Repository]) -> List[Dict[str, Any]]:
        """
        Generate summaries for multiple repositories concurrently
        
        Args:
            repositories: List of Repository objects
            
        Returns:
            List of summary dictionaries
        """
        tasks = [self.generate_repository_summary(repo) for repo in repositories]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        summaries = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Error generating summary for repository {i}: {result}")
                summaries.append({
                    "summary": "Error generating summary",
                    "key_features": ["Error generating features"],
                    "learning_insights": ["Error generating insights"],
                    "implementation_tips": ["Error generating tips"]
                })
            else:
                summaries.append(result)
        
        return summaries 