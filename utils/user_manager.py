"""
User Manager for DERSLY Streamlit application.
Manages user profile operations using session state.
"""
import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any
from utils.storage_manager import StorageManager


class UserManager:
    """
    Simplified user management without database.
    Stores single user profile in session state.
    """
    
    @staticmethod
    def create_profile(name: str, email: str, **kwargs) -> Dict[str, Any]:
        """
        Create user profile in session state.
        
        Args:
            name: User's full name
            email: User's email address
            **kwargs: Additional optional fields (student_id, department, class_year)
        
        Returns:
            Created user profile dictionary
        """
        StorageManager.initialize_storage()
        
        profile = {
            'name': name,
            'email': email,
            'student_id': kwargs.get('student_id'),
            'department': kwargs.get('department'),
            'class_year': kwargs.get('class_year'),
            'created_at': datetime.now().isoformat()
        }
        
        st.session_state['user_profile'] = profile
        return profile
    
    @staticmethod
    def get_profile() -> Optional[Dict[str, Any]]:
        """
        Get current user profile from session state.
        
        Returns:
            User profile dictionary if exists, None otherwise
        """
        StorageManager.initialize_storage()
        return st.session_state.get('user_profile')
    
    @staticmethod
    def update_profile(updates: Dict[str, Any]) -> bool:
        """
        Update user profile with new values.
        
        Args:
            updates: Dictionary of fields to update
        
        Returns:
            True if update successful, False otherwise
        """
        StorageManager.initialize_storage()
        
        profile = st.session_state.get('user_profile')
        if profile is None:
            return False
        
        # Update fields
        for key, value in updates.items():
            if key in ['name', 'email', 'student_id', 'department', 'class_year']:
                profile[key] = value
        
        st.session_state['user_profile'] = profile
        return True
    
    @staticmethod
    def is_profile_exists() -> bool:
        """
        Check if user profile exists in session state.
        
        Returns:
            True if profile exists, False otherwise
        """
        StorageManager.initialize_storage()
        profile = st.session_state.get('user_profile')
        return profile is not None
    
    @staticmethod
    def delete_profile() -> None:
        """
        Delete user profile from session state.
        """
        StorageManager.initialize_storage()
        st.session_state['user_profile'] = None
