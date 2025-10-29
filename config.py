"""
Configuration file for the Electronics Store Q&A System
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "electronics_store"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "port": os.getenv("DB_PORT", "5432"),
}

# Vector Database Configuration
VECTOR_DB_CONFIG = {"db_path": "./chroma_db", "collection_name": "electronics_qa"}

# Similarity Search Configuration
SIMILARITY_CONFIG = {
    "default_threshold": 0.3,
    "max_results": 5,
    "embedding_model": "all-MiniLM-L6-v2",
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "Electronics Store Q&A System",
    "page_icon": "🛒",
    "layout": "wide",
}
