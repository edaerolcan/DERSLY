"""
Course Manager for DERSLY Streamlit application.
Manages course data operations using session state.
"""
import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any, List
from utils.storage_manager import StorageManager


class CourseManager:
    """
    Manages course data in session state.
    Provides CRUD operations for courses.
    """
    
    @staticmethod
    def add_course(course_data: Dict[str, Any]) -> int:
        """
        Add new course and return ID.
        
        Args:
            course_data: Dictionary containing course information
                Required: course_name, course_code, day, start_time, end_time
                Optional: color, credits
        
        Returns:
            ID of the created course
        """
        StorageManager.initialize_storage()
        
        # Get next ID
        course_id = st.session_state['next_course_id']
        st.session_state['next_course_id'] += 1
        
        # Create course with ID
        course = {
            'id': course_id,
            'course_name': course_data['course_name'],
            'course_code': course_data['course_code'],
            'day': course_data['day'],
            'start_time': course_data['start_time'],
            'end_time': course_data['end_time'],
            'color': course_data.get('color', '#FF5733'),
            'credits': course_data.get('credits', 3),
            'created_at': datetime.now().isoformat()
        }
        
        # Store in session state
        st.session_state['courses'][course_id] = course
        
        return course_id
    
    @staticmethod
    def get_course(course_id: int) -> Optional[Dict[str, Any]]:
        """
        Get course by ID.
        
        Args:
            course_id: Course ID
        
        Returns:
            Course dictionary if found, None otherwise
        """
        StorageManager.initialize_storage()
        return st.session_state['courses'].get(course_id)
    
    @staticmethod
    def get_all_courses() -> List[Dict[str, Any]]:
        """
        Get all courses.
        
        Returns:
            List of all course dictionaries
        """
        StorageManager.initialize_storage()
        return list(st.session_state['courses'].values())
    
    @staticmethod
    def update_course(course_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update course with new values.
        
        Args:
            course_id: Course ID
            updates: Dictionary of fields to update
        
        Returns:
            True if update successful, False if course not found
        """
        StorageManager.initialize_storage()
        
        course = st.session_state['courses'].get(course_id)
        if course is None:
            return False
        
        # Update fields
        allowed_fields = ['course_name', 'course_code', 'day', 'start_time', 'end_time', 'color', 'credits']
        for key, value in updates.items():
            if key in allowed_fields:
                course[key] = value
        
        st.session_state['courses'][course_id] = course
        return True
    
    @staticmethod
    def delete_course(course_id: int) -> bool:
        """
        Delete course by ID.
        
        Args:
            course_id: Course ID
        
        Returns:
            True if deletion successful, False if course not found
        """
        StorageManager.initialize_storage()
        
        if course_id in st.session_state['courses']:
            del st.session_state['courses'][course_id]
            return True
        return False
    
    @staticmethod
    def get_courses_by_day(day: str) -> List[Dict[str, Any]]:
        """
        Get courses for specific day.
        
        Args:
            day: Day of week (e.g., "Monday", "Tuesday")
        
        Returns:
            List of courses for the specified day
        """
        StorageManager.initialize_storage()
        
        courses = []
        for course in st.session_state['courses'].values():
            if course.get('day') == day:
                courses.append(course)
        
        # Sort by start time
        courses.sort(key=lambda x: x.get('start_time', '00:00'))
        
        return courses
    
    @staticmethod
    def get_course_count() -> int:
        """
        Get total number of courses.
        
        Returns:
            Number of courses
        """
        StorageManager.initialize_storage()
        return len(st.session_state['courses'])
    
    @staticmethod
    def check_time_conflict(day: str, start_time: str, end_time: str, exclude_course_id: Optional[int] = None) -> tuple[bool, Optional[Dict[str, Any]]]:
        """
        Check if a course time conflicts with existing courses.
        
        Args:
            day: Day of week
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            exclude_course_id: Course ID to exclude from conflict check (for updates)
        
        Returns:
            Tuple of (has_conflict, conflicting_course)
        """
        StorageManager.initialize_storage()
        
        # Convert times to minutes for easier comparison
        def time_to_minutes(time_str: str) -> int:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        
        new_start = time_to_minutes(start_time)
        new_end = time_to_minutes(end_time)
        
        # Check all courses on the same day
        for course in st.session_state['courses'].values():
            # Skip if this is the course being updated
            if exclude_course_id and course['id'] == exclude_course_id:
                continue
            
            # Only check courses on the same day
            if course.get('day') != day:
                continue
            
            existing_start = time_to_minutes(course['start_time'])
            existing_end = time_to_minutes(course['end_time'])
            
            # Check for overlap
            # Overlap occurs if: new_start < existing_end AND new_end > existing_start
            if new_start < existing_end and new_end > existing_start:
                return True, course
        
        return False, None
    
    @staticmethod
    def get_weekly_schedule() -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all courses organized by day of week.
        
        Returns:
            Dictionary with days as keys and list of courses as values
        """
        StorageManager.initialize_storage()
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        schedule = {day: [] for day in days}
        
        for course in st.session_state['courses'].values():
            day = course.get('day')
            if day in schedule:
                schedule[day].append(course)
        
        # Sort courses by start time for each day
        for day in schedule:
            schedule[day].sort(key=lambda x: x.get('start_time', '00:00'))
        
        return schedule
    
    @staticmethod
    def get_today_courses() -> List[Dict[str, Any]]:
        """
        Get courses for today.
        
        Returns:
            List of today's courses sorted by start time
        """
        StorageManager.initialize_storage()
        
        # Get current day
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        today = day_names[datetime.now().weekday()]
        
        return CourseManager.get_courses_by_day(today)
