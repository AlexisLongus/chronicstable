"""Service for interacting with Ollama LLM API.

Provides methods for sending prompts to an Ollama LLM instance and handling responses.
"""
import json
from typing import Dict, Any, List, Optional

import requests


class OllamaService:
    """Service for interacting with Ollama LLM API through AWS load balancer."""
    
    def __init__(self, base_url: str, model: str):
        """Initialize the Ollama service.
        
        Args:
            base_url: Base URL for the Ollama API (with load balancer)
            model: Model name to use
        """
        # The base URL already includes /api/generate, so we don't need to add it again
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.generate_endpoint = self.base_url
    
    def get_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Get a response from the Ollama API.
        
        Args:
            prompt: The prompt to send to the model
            context: Additional context to provide to the model (patient info, etc.)
            
        Returns:
            The generated response text
        """
        # Build complete prompt with context if provided
        complete_prompt = prompt
        if context:
            complete_prompt = f"Context:\n{context}\n\nQuestion: {prompt}"
        
        payload = {
            "model": self.model,
            "prompt": complete_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 1024
            }
        }
        
        try:
            response = requests.post(self.generate_endpoint, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "No response received from model.")
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error connecting to Ollama API: {str(e)}"
            print(error_msg)
            return f"Error: {error_msg}"
            
        except json.JSONDecodeError:
            error_msg = "Invalid JSON response from Ollama API"
            print(error_msg)
            return f"Error: {error_msg}"
    
    def health_check(self) -> bool:
        """Check if the Ollama API is available.
        
        Returns:
            True if the API is available, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/health")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
