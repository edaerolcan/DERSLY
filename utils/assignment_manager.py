"""
Assignment Manager for DERSLY Streamlit application.
Manages assignment data operations using session state.
"""
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from utils.storage_manager import StorageManager


class AssignmentManager:
    """
    Manages assignment data in session state.
    Provides CRUD operations for assignments.
    """
    
    @staticmethod
    def add_assignment(assignment_data: Dict[str, Any]) -> int:
        """
        Add new assignment and return ID.
        
        Args:
            assignment_data: Dictionary containing assignment information
                Required: title, due_date, type
                Optional: course_id, description, status, priority
        
        Returns:
            ID of the created assignment
        """
        StorageManager.initialize_storage()
        
        # Get next ID
        assignment_id = st.session_state['next_assignment_id']
        st.session_state['next_assignment_id'] += 1
        
        # Create assignment with ID
        assignment = {
            'id': assignment_id,
            'course_id': assignment_data.get('course_id'),
            'title': assignment_data['title'],
            'description': assignment_data.get('description'),
            'type': assignment_data.get('type', 'assignment'),
            'due_date': assignment_data['due_date'],
            'status': assignment_data.get('status', 'pending'),
            'priority': assignment_data.get('priority', 'medium'),
            'created_at': datetime.now().isoformat()
        }
        
        # Store in session state
        st.session_state['assignments'][assignment_id] = assignment
        
        return assignment_id
    
    @staticmethod
    def get_assignment(assignment_id: int) -> Optional[Dict[str, Any]]:
        """
        Get assignment by ID.
        
        Args:
            assignment_id: Assignment ID
        
        Returns:
            Assignment dictionary if found, None otherwise
        """
        StorageManager.initialize_storage()
        return st.session_state['assignments'].get(assignment_id)
    
    @staticmethod
    def get_all_assignments() -> List[Dict[str, Any]]:
        """
        Get all assignments.
        
        Returns:
            List of all assignment dictionaries
        """
        StorageManager.initialize_storage()
        return list(st.session_state['assignments'].values())
    
    @staticmethod
    def update_assignment(assignment_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update assignment with new values.
        
        Args:
            assignment_id: Assignment ID
            updates: Dictionary of fields to update
        
        Returns:
            True if update successful, False if assignment not found
        """
        StorageManager.initialize_storage()
        
        assignment = st.session_state['assignments'].get(assignment_id)
        if assignment is None:
            return False
        
        # Update fields
        allowed_fields = ['course_id', 'title', 'description', 'type', 'due_date', 'status', 'priority']
        for key, value in updates.items():
            if key in allowed_fields:
                assignment[key] = value
        
        st.session_state['assignments'][assignment_id] = assignment
        return True
    
    @staticmethod
    def delete_assignment(assignment_id: int) -> bool:
        """
        Delete assignment by ID.
        
        Args:
            assignment_id: Assignment ID
        
        Returns:
            True if deletion successful, False if assignment not found
        """
        StorageManager.initialize_storage()
        
        if assignment_id in st.session_state['assignments']:
            del st.session_state['assignments'][assignment_id]
            return True
        return False
    
    @staticmethod
    def get_assignments_by_status(status: str) -> List[Dict[str, Any]]:
        """
        Get assignments by status.
        
        Args:
            status: Assignment status (e.g., "pending", "completed")
        
        Returns:
            List of assignments with the specified status
        """
        StorageManager.initialize_storage()
        
        assignments = []
        for assignment in st.session_state['assignments'].values():
            if assignment.get('status') == status:
                assignments.append(assignment)
        
        # Sort by due date
        assignments.sort(key=lambda x: x.get('due_date', ''))
        
        return assignments
    
    @staticmethod
    def get_upcoming_assignments(days: int = 7) -> List[Dict[str, Any]]:
        """
        Get assignments due in next N days.
        
        Args:
            days: Number of days to look ahead (default: 7)
        
        Returns:
            List of upcoming assignments
        """
        StorageManager.initialize_storage()
        
        now = datetime.now()
        future = now + timedelta(days=days)
        
        upcoming = []
        for assignment in st.session_state['assignments'].values():
            # Skip completed assignments
            if assignment.get('status') == 'completed':
                continue
            
            # Parse due date
            try:
                due_date_str = assignment.get('due_date', '')
                if 'T' in due_date_str:
                    due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                else:
                    due_date = datetime.fromisoformat(due_date_str)
                
                # Check if within range
                if now <= due_date <= future:
                    upcoming.append(assignment)
            except (ValueError, AttributeError):
                # Skip assignments with invalid dates
                continue
        
        # Sort by due date
        upcoming.sort(key=lambda x: x.get('due_date', ''))
        
        return upcoming
    
    @staticmethod
    def get_assignment_count() -> int:
        """
        Get total number of assignments.
        
        Returns:
            Number of assignments
        """
        StorageManager.initialize_storage()
        return len(st.session_state['assignments'])
    
    @staticmethod
    def get_pending_count() -> int:
        """
        Get number of pending assignments.
        
        Returns:
            Number of pending assignments
        """
        StorageManager.initialize_storage()
        count = 0
        for assignment in st.session_state['assignments'].values():
            if assignment.get('status') == 'pending':
                count += 1
        return count
