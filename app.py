"""
Main entry point for DERSLY Streamlit application.
Simplified version using browser storage instead of database.
"""
import streamlit as st
from utils.storage_manager import StorageManager
from utils.user_manager import UserManager
from utils.ui_styles import apply_modern_style, show_logo_in_sidebar

# Page configuration
st.set_page_config(
    page_title="DERSLY - Öğrenci Destek Platformu",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "DERSLY - Üniversite Öğrenci Destek Platformu v2.0"
    }
)

# Redirect to Ana Sayfa
st.switch_page("pages/1_🏠_Ana_Sayfa.py")
