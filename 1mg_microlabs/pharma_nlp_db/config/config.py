"""Configuration module for Pharma NLP Database System."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application."""
    
    # LLM Provider
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Anthropic Configuration
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # Database Configuration
    DB_NAME = os.getenv("DB_NAME", "pharmadb")
    TABLE_NAME = os.getenv("TABLE_NAME", "pharmadata")
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    DB_PATH = DATA_DIR / f"{DB_NAME}.db"
    
    # JSON Data Path (external)
    JSON_DATA_PATH = os.getenv("DATA_PATH", str(BASE_DIR.parent / "1mg_microlabs"))
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
        elif cls.LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required when using Anthropic provider")
        
        # Create data directory if it doesn't exist
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        return True

