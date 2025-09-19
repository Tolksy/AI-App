"""
Configuration settings for the RAG-based Agentic AI System
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RAG-based Agentic AI System"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Advanced AI system combining RAG with autonomous agents"
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./ai_system.db", env="DATABASE_URL")
    MONGODB_URL: Optional[str] = Field(default=None, env="MONGODB_URL")
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # Vector Database
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma_db"
    VECTOR_DB_TYPE: str = Field(default="chroma", env="VECTOR_DB_TYPE")  # chroma, faiss, pinecone
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    DEFAULT_LLM_PROVIDER: str = Field(default="openai", env="DEFAULT_LLM_PROVIDER")
    DEFAULT_MODEL: str = Field(default="gpt-4-turbo-preview", env="DEFAULT_MODEL")
    
    # Embeddings
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-large", env="EMBEDDING_MODEL")
    EMBEDDING_DIMENSIONS: int = Field(default=1536, env="EMBEDDING_DIMENSIONS")
    
    # RAG Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    MAX_CONTEXT_LENGTH: int = 4000
    
    # Agent Configuration
    MAX_AGENT_ITERATIONS: int = 10
    AGENT_TIMEOUT_SECONDS: int = 300
    ENABLE_AUTO_EXECUTION: bool = True
    
    # Document Processing
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    SUPPORTED_FILE_TYPES: List[str] = [
        ".pdf", ".txt", ".md", ".docx", ".html", ".json", ".csv"
    ]
    DOCUMENT_STORAGE_PATH: str = "./data/documents"
    
    # Cloud Storage (Optional)
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET: Optional[str] = Field(default=None, env="AWS_S3_BUCKET")
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = Field(
        default=None, env="AZURE_STORAGE_CONNECTION_STRING"
    )
    AZURE_CONTAINER_NAME: Optional[str] = Field(default=None, env="AZURE_CONTAINER_NAME")
    
    GCP_PROJECT_ID: Optional[str] = Field(default=None, env="GCP_PROJECT_ID")
    GCP_BUCKET_NAME: Optional[str] = Field(default=None, env="GCP_BUCKET_NAME")
    
    # Monitoring and Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # Development
    DEBUG: bool = Field(default=False, env="DEBUG")
    RELOAD: bool = Field(default=True, env="RELOAD")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Database configuration
DATABASE_CONFIG = {
    "sqlite": {
        "url": settings.DATABASE_URL,
        "echo": settings.DEBUG
    },
    "mongodb": {
        "url": settings.MONGODB_URL,
        "database": "ai_system"
    } if settings.MONGODB_URL else None
}

# Vector database configuration
VECTOR_DB_CONFIG = {
    "chroma": {
        "persist_directory": settings.CHROMA_PERSIST_DIRECTORY,
        "collection_name": "documents"
    },
    "faiss": {
        "index_path": "./data/faiss_index",
        "dimension": settings.EMBEDDING_DIMENSIONS
    },
    "pinecone": {
        "api_key": os.getenv("PINECONE_API_KEY"),
        "environment": os.getenv("PINECONE_ENVIRONMENT"),
        "index_name": os.getenv("PINECONE_INDEX_NAME")
    }
}

# LLM configuration
LLM_CONFIG = {
    "openai": {
        "api_key": settings.OPENAI_API_KEY,
        "model": settings.DEFAULT_MODEL,
        "temperature": 0.7,
        "max_tokens": 2000
    },
    "anthropic": {
        "api_key": settings.ANTHROPIC_API_KEY,
        "model": "claude-3-sonnet-20240229",
        "temperature": 0.7,
        "max_tokens": 2000
    }
}

# Agent configuration
AGENT_CONFIG = {
    "general": {
        "max_iterations": settings.MAX_AGENT_ITERATIONS,
        "timeout": settings.AGENT_TIMEOUT_SECONDS,
        "tools": ["search", "calculator", "web_search", "file_operations"]
    },
    "scheduling": {
        "max_iterations": 5,
        "timeout": 60,
        "tools": ["calendar", "time_analysis", "suggestion_generator"]
    },
    "research": {
        "max_iterations": 15,
        "timeout": 600,
        "tools": ["web_search", "document_analysis", "data_extraction"]
    }
}

