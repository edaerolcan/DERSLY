"""
Storage Manager for DERSLY Streamlit application.
Manages all data storage operations using Streamlit session state.
"""
import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional
import sys


class StorageManager:
    """
    Manages all data storage operations using Streamlit session state.
    Provides initialization, export/import, and cleanup functionality.
    """
    
    # Data format version for compatibility checking
    DATA_VERSION = "1.0.0"
    
    @staticmethod
    def initialize_storage() -> None:
        """
        Initialize empty data structures in session state if not exists.
        Sets up all required data containers and metadata.
        """
        # Initialize user profile
        if 'user_profile' not in st.session_state:
            st.session_state['user_profile'] = None
        
        # Initialize courses dictionary
        if 'courses' not in st.session_state:
            st.session_state['courses'] = {}
        
        # Initialize assignments dictionary
        if 'assignments' not in st.session_state:
            st.session_state['assignments'] = {}
        
        # Initialize grades dictionary
        if 'grades' not in st.session_state:
            st.session_state['grades'] = {}
        
        # Initialize reminders dictionary
        if 'reminders' not in st.session_state:
            st.session_state['reminders'] = {}
        
        # Initialize metadata
        if 'metadata' not in st.session_state:
            st.session_state['metadata'] = {
                'version': StorageManager.DATA_VERSION,
                'last_export': None,
                'last_import': None,
                'created_at': datetime.now().isoformat()
            }
        
        # Initialize auto-increment counters
        if 'next_course_id' not in st.session_state:
            st.session_state['next_course_id'] = 1
        
        if 'next_assignment_id' not in st.session_state:
            st.session_state['next_assignment_id'] = 1
        
        if 'next_grade_id' not in st.session_state:
            st.session_state['next_grade_id'] = 1
        
        if 'next_reminder_id' not in st.session_state:
            st.session_state['next_reminder_id'] = 1
    
    @staticmethod
    def get_storage_info() -> Dict[str, Any]:
        """
        Get storage usage information and statistics.
        
        Returns:
            Dictionary containing storage statistics
        """
        StorageManager.initialize_storage()
        
        # Count items
        num_courses = len(st.session_state.get('courses', {}))
        num_assignments = len(st.session_state.get('assignments', {}))
        num_grades = len(st.session_state.get('grades', {}))
        num_reminders = len(st.session_state.get('reminders', {}))
        
        # Estimate storage size (rough approximation)
        # Calculate size of session state data
        total_size = 0
        try:
            # Estimate size of each data structure
            for key in ['user_profile', 'courses', 'assignments', 'grades', 'reminders', 'metadata']:
                if key in st.session_state and st.session_state[key] is not None:
                    total_size += sys.getsizeof(str(st.session_state[key]))
        except Exception:
            total_size = 0
        
        # Convert to KB/MB
        size_kb = total_size / 1024
        size_mb = size_kb / 1024
        
        # Check if profile exists
        has_profile = st.session_state.get('user_profile') is not None
        
        return {
            'has_profile': has_profile,
            'num_courses': num_courses,
            'num_assignments': num_assignments,
            'num_grades': num_grades,
            'num_reminders': num_reminders,
            'total_items': num_courses + num_assignments + num_grades + num_reminders,
            'size_bytes': total_size,
            'size_kb': round(size_kb, 2),
            'size_mb': round(size_mb, 2),
            'version': st.session_state.get('metadata', {}).get('version', 'Unknown'),
            'last_export': st.session_state.get('metadata', {}).get('last_export'),
            'last_import': st.session_state.get('metadata', {}).get('last_import')
        }
    
    @staticmethod
    def clear_all_data() -> None:
        """
        Clear all data from session state.
        Removes all user data and resets to initial state.
        """
        # Clear all data structures
        st.session_state['user_profile'] = None
        st.session_state['courses'] = {}
        st.session_state['assignments'] = {}
        st.session_state['grades'] = {}
        st.session_state['reminders'] = {}
        
        # Reset metadata
        st.session_state['metadata'] = {
            'version': StorageManager.DATA_VERSION,
            'last_export': None,
            'last_import': None,
            'created_at': datetime.now().isoformat()
        }
        
        # Reset auto-increment counters
        st.session_state['next_course_id'] = 1
        st.session_state['next_assignment_id'] = 1
        st.session_state['next_grade_id'] = 1
        st.session_state['next_reminder_id'] = 1
    
    @staticmethod
    def has_data() -> bool:
        """
        Check if any data exists in storage.
        
        Returns:
            True if any data exists, False otherwise
        """
        StorageManager.initialize_storage()
        
        # Check if profile exists
        if st.session_state.get('user_profile') is not None:
            return True
        
        # Check if any items exist
        if len(st.session_state.get('courses', {})) > 0:
            return True
        if len(st.session_state.get('assignments', {})) > 0:
            return True
        if len(st.session_state.get('grades', {})) > 0:
            return True
        if len(st.session_state.get('reminders', {})) > 0:
            return True
        
        return False
    
    @staticmethod
    def export_data() -> Dict[str, Any]:
        """
        Export all data as a dictionary for JSON serialization.
        Includes metadata with version and timestamp.
        
        Returns:
            Dictionary containing all user data in JSON-serializable format
        """
        StorageManager.initialize_storage()
        
        # Get current timestamp
        export_timestamp = datetime.now().isoformat()
        
        # Convert courses dict to list
        courses_list = []
        for course_id, course_data in st.session_state.get('courses', {}).items():
            courses_list.append(course_data)
        
        # Convert assignments dict to list
        assignments_list = []
        for assignment_id, assignment_data in st.session_state.get('assignments', {}).items():
            assignments_list.append(assignment_data)
        
        # Convert grades dict to list
        grades_list = []
        for grade_id, grade_data in st.session_state.get('grades', {}).items():
            grades_list.append(grade_data)
        
        # Convert reminders dict to list
        reminders_list = []
        for reminder_id, reminder_data in st.session_state.get('reminders', {}).items():
            reminders_list.append(reminder_data)
        
        # Build export data structure
        export_data = {
            'version': StorageManager.DATA_VERSION,
            'exported_at': export_timestamp,
            'user_profile': st.session_state.get('user_profile'),
            'courses': courses_list,
            'assignments': assignments_list,
            'grades': grades_list,
            'reminders': reminders_list,
            'next_course_id': st.session_state.get('next_course_id', 1),
            'next_assignment_id': st.session_state.get('next_assignment_id', 1),
            'next_grade_id': st.session_state.get('next_grade_id', 1),
            'next_reminder_id': st.session_state.get('next_reminder_id', 1)
        }
        
        # Update metadata with last export timestamp
        if 'metadata' in st.session_state:
            st.session_state['metadata']['last_export'] = export_timestamp
        
        return export_data
    
    @staticmethod
    def import_data(data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Import data from dictionary and update session state.
        Validates data structure and integrity before importing.
        
        Args:
            data: Dictionary containing exported data
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Validate required fields
            required_fields = ['version', 'exported_at']
            for field in required_fields:
                if field not in data:
                    return False, f"❌ Geçersiz veri formatı: '{field}' alanı eksik"
            
            # Check version compatibility
            imported_version = data.get('version', '0.0.0')
            if imported_version != StorageManager.DATA_VERSION:
                # For now, we'll accept any version but warn the user
                # In future, we can add version migration logic
                pass
            
            # Validate data types
            if 'user_profile' in data and data['user_profile'] is not None:
                if not isinstance(data['user_profile'], dict):
                    return False, "❌ Geçersiz kullanıcı profili formatı"
            
            if 'courses' in data and not isinstance(data['courses'], list):
                return False, "❌ Geçersiz ders listesi formatı"
            
            if 'assignments' in data and not isinstance(data['assignments'], list):
                return False, "❌ Geçersiz ödev listesi formatı"
            
            if 'grades' in data and not isinstance(data['grades'], list):
                return False, "❌ Geçersiz not listesi formatı"
            
            if 'reminders' in data and not isinstance(data['reminders'], list):
                return False, "❌ Geçersiz hatırlatıcı listesi formatı"
            
            # Initialize storage first
            StorageManager.initialize_storage()
            
            # Import user profile
            st.session_state['user_profile'] = data.get('user_profile')
            
            # Import courses (convert list to dict with ID keys)
            courses_dict = {}
            for course in data.get('courses', []):
                if 'id' in course:
                    courses_dict[course['id']] = course
            st.session_state['courses'] = courses_dict
            
            # Import assignments (convert list to dict with ID keys)
            assignments_dict = {}
            for assignment in data.get('assignments', []):
                if 'id' in assignment:
                    assignments_dict[assignment['id']] = assignment
            st.session_state['assignments'] = assignments_dict
            
            # Import grades (convert list to dict with ID keys)
            grades_dict = {}
            for grade in data.get('grades', []):
                if 'id' in grade:
                    grades_dict[grade['id']] = grade
            st.session_state['grades'] = grades_dict
            
            # Import reminders (convert list to dict with ID keys)
            reminders_dict = {}
            for reminder in data.get('reminders', []):
                if 'id' in reminder:
                    reminders_dict[reminder['id']] = reminder
            st.session_state['reminders'] = reminders_dict
            
            # Import ID counters
            st.session_state['next_course_id'] = data.get('next_course_id', 1)
            st.session_state['next_assignment_id'] = data.get('next_assignment_id', 1)
            st.session_state['next_grade_id'] = data.get('next_grade_id', 1)
            st.session_state['next_reminder_id'] = data.get('next_reminder_id', 1)
            
            # Update metadata
            import_timestamp = datetime.now().isoformat()
            if 'metadata' in st.session_state:
                st.session_state['metadata']['last_import'] = import_timestamp
                st.session_state['metadata']['version'] = StorageManager.DATA_VERSION
            
            return True, "✅ Veriler başarıyla içe aktarıldı!"
            
        except Exception as e:
            return False, f"❌ Veri içe aktarma hatası: {str(e)}"
