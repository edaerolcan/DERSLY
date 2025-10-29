"""
Configuration module for DERSLY Streamlit application.
Simplified version for browser storage (no database needed).
"""
import os
from dotenv import load_dotenv

# Try to import streamlit for secrets support
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

# Load environment variables from .env file (local development)
load_dotenv()

def get_config(key: str, default: str = '') -> str:
    """
    Get configuration value from Streamlit secrets or environment variables.
    Priority: Streamlit secrets > Environment variables > Default
    
    Args:
        key: Configuration key
        default: Default value if not found
    
    Returns:
        Configuration value
    """
    # Try Streamlit secrets first (for Streamlit Cloud)
    if HAS_STREAMLIT and hasattr(st, 'secrets'):
        try:
            return st.secrets.get(key, os.getenv(key, default))
        except:
            pass
    
    # Fall back to environment variables
    return os.getenv(key, default)

# Application configuration
DEBUG = get_config('DEBUG', 'False') == 'True'

# Deployment info
IS_PRODUCTION = get_config('ENVIRONMENT', 'development') == 'production'

# App version
APP_VERSION = "2.0.0"
