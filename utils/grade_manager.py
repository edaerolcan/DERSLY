"""
Grade Manager for DERSLY Streamlit application.
Manages grade data operations and GPA calculations using session state.
"""
import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any, List
from utils.storage_manager import StorageManager


class GradeManager:
    """
    Manages grade entries and GPA calculations.
    Provides CRUD operations for grades and GPA computation.
    """
    
    @staticmethod
    def add_grade(grade_data: Dict[str, Any]) -> int:
        """
        Add new grade entry and return ID.
        
        Args:
            grade_data: Dictionary containing grade information
                Required: course_name, grade, credits, semester, year
        
        Returns:
            ID of the created grade entry
        """
        StorageManager.initialize_storage()
        
        # Get next ID
        grade_id = st.session_state['next_grade_id']
        st.session_state['next_grade_id'] += 1
        
        # Create grade entry with ID
        grade = {
            'id': grade_id,
            'course_name': grade_data['course_name'],
            'grade': float(grade_data['grade']),
            'credits': int(grade_data['credits']),
            'semester': grade_data['semester'],
            'year': int(grade_data['year']),
            'created_at': datetime.now().isoformat()
        }
        
        # Store in session state
        st.session_state['grades'][grade_id] = grade
        
        return grade_id
    
    @staticmethod
    def get_grade(grade_id: int) -> Optional[Dict[str, Any]]:
        """
        Get grade entry by ID.
        
        Args:
            grade_id: Grade ID
        
        Returns:
            Grade dictionary if found, None otherwise
        """
        StorageManager.initialize_storage()
        return st.session_state['grades'].get(grade_id)
    
    @staticmethod
    def get_all_grades() -> List[Dict[str, Any]]:
        """
        Get all grade entries.
        
        Returns:
            List of all grade dictionaries
        """
        StorageManager.initialize_storage()
        return list(st.session_state['grades'].values())
    
    @staticmethod
    def update_grade(grade_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update grade entry with new values.
        
        Args:
            grade_id: Grade ID
            updates: Dictionary of fields to update
        
        Returns:
            True if update successful, False if grade not found
        """
        StorageManager.initialize_storage()
        
        grade = st.session_state['grades'].get(grade_id)
        if grade is None:
            return False
        
        # Update fields
        allowed_fields = ['course_name', 'grade', 'credits', 'semester', 'year']
        for key, value in updates.items():
            if key in allowed_fields:
                if key == 'grade':
                    grade[key] = float(value)
                elif key in ['credits', 'year']:
                    grade[key] = int(value)
                else:
                    grade[key] = value
        
        st.session_state['grades'][grade_id] = grade
        return True
    
    @staticmethod
    def delete_grade(grade_id: int) -> bool:
        """
        Delete grade entry by ID.
        
        Args:
            grade_id: Grade ID
        
        Returns:
            True if deletion successful, False if grade not found
        """
        StorageManager.initialize_storage()
        
        if grade_id in st.session_state['grades']:
            del st.session_state['grades'][grade_id]
            return True
        return False
    
    @staticmethod
    def calculate_gpa() -> float:
        """
        Calculate overall GPA (Grade Point Average).
        
        Returns:
            Overall GPA (0.0 to 4.0 scale)
        """
        StorageManager.initialize_storage()
        
        total_points = 0.0
        total_credits = 0
        
        for grade in st.session_state['grades'].values():
            grade_value = float(grade.get('grade', 0))
            credits = int(grade.get('credits', 0))
            
            total_points += grade_value * credits
            total_credits += credits
        
        if total_credits == 0:
            return 0.0
        
        return round(total_points / total_credits, 2)
    
    @staticmethod
    def calculate_semester_gpa(semester: str, year: int) -> float:
        """
        Calculate GPA for specific semester.
        
        Args:
            semester: Semester name (e.g., "Fall", "Spring")
            year: Year (e.g., 2024)
        
        Returns:
            Semester GPA (0.0 to 4.0 scale)
        """
        StorageManager.initialize_storage()
        
        total_points = 0.0
        total_credits = 0
        
        for grade in st.session_state['grades'].values():
            if grade.get('semester') == semester and grade.get('year') == year:
                grade_value = float(grade.get('grade', 0))
                credits = int(grade.get('credits', 0))
                
                total_points += grade_value * credits
                total_credits += credits
        
        if total_credits == 0:
            return 0.0
        
        return round(total_points / total_credits, 2)
    
    @staticmethod
    def get_grades_by_semester(semester: str, year: int) -> List[Dict[str, Any]]:
        """
        Get grades for specific semester.
        
        Args:
            semester: Semester name (e.g., "Fall", "Spring")
            year: Year (e.g., 2024)
        
        Returns:
            List of grades for the specified semester
        """
        StorageManager.initialize_storage()
        
        grades = []
        for grade in st.session_state['grades'].values():
            if grade.get('semester') == semester and grade.get('year') == year:
                grades.append(grade)
        
        # Sort by course name
        grades.sort(key=lambda x: x.get('course_name', ''))
        
        return grades
    
    @staticmethod
    def get_grade_count() -> int:
        """
        Get total number of grade entries.
        
        Returns:
            Number of grade entries
        """
        StorageManager.initialize_storage()
        return len(st.session_state['grades'])
    
    @staticmethod
    def get_total_credits() -> int:
        """
        Get total number of credits across all grades.
        
        Returns:
            Total credits
        """
        StorageManager.initialize_storage()
        
        total = 0
        for grade in st.session_state['grades'].values():
            total += int(grade.get('credits', 0))
        
        return total
    
    @staticmethod
    def get_semesters() -> List[tuple]:
        """
        Get list of unique semesters with grades.
        
        Returns:
            List of (semester, year) tuples
        """
        StorageManager.initialize_storage()
        
        semesters = set()
        for grade in st.session_state['grades'].values():
            semester = grade.get('semester')
            year = grade.get('year')
            if semester and year:
                semesters.add((semester, year))
        
        # Sort by year and semester
        return sorted(list(semesters), key=lambda x: (x[1], x[0]))
