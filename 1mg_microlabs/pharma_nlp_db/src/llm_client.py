"""LLM Client module supporting multiple providers (OpenAI, Anthropic, Ollama)."""

import os
import sys
from typing import Optional, List, Dict, Any

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config


class LLMClient:
    """Universal LLM client supporting multiple providers."""
    
    def __init__(self, provider: Optional[str] = None):
        """Initialize LLM client with specified provider."""
        self.provider = provider or Config.LLM_PROVIDER
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client based on provider."""
        if self.provider == "openai":
            self._initialize_openai()
        elif self.provider == "anthropic":
            self._initialize_anthropic()
        elif self.provider == "ollama":
            self._initialize_ollama()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _initialize_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = Config.OPENAI_MODEL
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def _initialize_anthropic(self):
        """Initialize Anthropic client."""
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            self.model = Config.ANTHROPIC_MODEL
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
    
    def _initialize_ollama(self):
        """Initialize Ollama client (using OpenAI compatibility layer)."""
        try:
            from openai import OpenAI
            self.client = OpenAI(
                base_url=Config.OLLAMA_BASE_URL + "/v1",
                api_key="ollama"  # Dummy key for Ollama
            )
            self.model = Config.OLLAMA_MODEL
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def get_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Get completion from LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        if self.provider == "anthropic":
            return self._get_anthropic_completion(prompt, system_prompt, temperature, max_tokens)
        else:  # OpenAI or Ollama
            return self._get_openai_completion(prompt, system_prompt, temperature, max_tokens)
    
    def _get_openai_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str], 
        temperature: float, 
        max_tokens: int
    ) -> str:
        """Get completion from OpenAI or Ollama."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    def _get_anthropic_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str], 
        temperature: float, 
        max_tokens: int
    ) -> str:
        """Get completion from Anthropic."""
        kwargs = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        response = self.client.messages.create(**kwargs)
        return response.content[0].text
    
    def get_json_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.3
    ) -> str:
        """Get completion optimized for JSON output.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Lower temperature for more consistent JSON
            
        Returns:
            Generated JSON string
        """
        if not system_prompt:
            system_prompt = "You are a helpful assistant that generates valid JSON responses."
        
        return self.get_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=4000
        )


# Convenience function
def get_llm_client(provider: Optional[str] = None) -> LLMClient:
    """Get LLM client instance.
    
    Args:
        provider: LLM provider (openai, anthropic, ollama). If None, uses config default.
        
    Returns:
        LLMClient instance
    """
    return LLMClient(provider)


if __name__ == "__main__":
    # Test the LLM client
    try:
        Config.validate()
        client = get_llm_client()
        response = client.get_completion("Say hello!")
        print(f"LLM Response: {response}")
    except Exception as e:
        print(f"Error: {e}")

