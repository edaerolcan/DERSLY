"""
Calculation utilities for DERSLY Streamlit application.
Handles GPA calculations (GNO and DNO).
"""
from typing import List, Dict, Tuple
import logging

from database.models import GradeEntry

logger = logging.getLogger(__name__)


class GPACalculator:
    """
    GPA Calculator for computing semester and cumulative GPAs.
    """
    
    @staticmethod
    def validate_grade(grade: float) -> bool:
        """
        Validate that grade is within acceptable range (0.0 to 4.0).
        
        Args:
            grade: Grade value to validate
        
        Returns:
            True if valid, False otherwise
        """
        return 0.0 <= grade <= 4.0
    
    @staticmethod
    def calculate_gno(grade_entries: List[GradeEntry]) -> float:
        """
        Calculate GNO (Semester GPA) for a list of grade entries.
        GNO = Sum(grade * credits) / Sum(credits)
        
        Args:
            grade_entries: List of GradeEntry objects for a semester
        
        Returns:
            GNO value (0.0 to 4.0), or 0.0 if no valid entries
        """
        if not grade_entries:
            return 0.0
        
        try:
            total_points = 0.0
            total_credits = 0
            
            for entry in grade_entries:
                # Validate grade
                if not GPACalculator.validate_grade(entry.grade):
                    logger.warning(f"Invalid grade value: {entry.grade} for course {entry.course_name}")
                    continue
                
                # Validate credits
                if entry.credits <= 0:
                    logger.warning(f"Invalid credits value: {entry.credits} for course {entry.course_name}")
                    continue
                
                total_points += entry.grade * entry.credits
                total_credits += entry.credits
            
            if total_credits == 0:
                return 0.0
            
            gno = total_points / total_credits
            return round(gno, 2)
            
        except Exception as e:
            logger.error(f"Error calculating GNO: {str(e)}")
            return 0.0
    
    @staticmethod
    def calculate_dno(grade_entries: List[GradeEntry]) -> float:
        """
        Calculate DNO (Cumulative GPA) for all grade entries across all semesters.
        DNO = Sum(grade * credits) / Sum(credits)
        
        Args:
            grade_entries: List of all GradeEntry objects
        
        Returns:
            DNO value (0.0 to 4.0), or 0.0 if no valid entries
        """
        if not grade_entries:
            return 0.0
        
        try:
            total_points = 0.0
            total_credits = 0
            
            for entry in grade_entries:
                # Validate grade
                if not GPACalculator.validate_grade(entry.grade):
                    logger.warning(f"Invalid grade value: {entry.grade} for course {entry.course_name}")
                    continue
                
                # Validate credits
                if entry.credits <= 0:
                    logger.warning(f"Invalid credits value: {entry.credits} for course {entry.course_name}")
                    continue
                
                total_points += entry.grade * entry.credits
                total_credits += entry.credits
            
            if total_credits == 0:
                return 0.0
            
            dno = total_points / total_credits
            return round(dno, 2)
            
        except Exception as e:
            logger.error(f"Error calculating DNO: {str(e)}")
            return 0.0
    
    @staticmethod
    def calculate_semester_gpas(grade_entries: List[GradeEntry]) -> Dict[str, float]:
        """
        Calculate GNO for each semester.
        
        Args:
            grade_entries: List of all GradeEntry objects
        
        Returns:
            Dictionary mapping semester names to GNO values
        """
        if not grade_entries:
            return {}
        
        try:
            # Group entries by semester
            semester_entries = {}
            for entry in grade_entries:
                semester_key = f"{entry.semester} {entry.year}"
                if semester_key not in semester_entries:
                    semester_entries[semester_key] = []
                semester_entries[semester_key].append(entry)
            
            # Calculate GNO for each semester
            semester_gpas = {}
            for semester, entries in semester_entries.items():
                gno = GPACalculator.calculate_gno(entries)
                semester_gpas[semester] = gno
            
            return semester_gpas
            
        except Exception as e:
            logger.error(f"Error calculating semester GPAs: {str(e)}")
            return {}
    
    @staticmethod
    def get_gpa_statistics(grade_entries: List[GradeEntry]) -> Dict[str, any]:
        """
        Get comprehensive GPA statistics.
        
        Args:
            grade_entries: List of all GradeEntry objects
        
        Returns:
            Dictionary containing various GPA statistics
        """
        if not grade_entries:
            return {
                'dno': 0.0,
                'total_credits': 0,
                'total_courses': 0,
                'semester_gpas': {},
                'highest_gno': 0.0,
                'lowest_gno': 0.0,
                'average_gno': 0.0
            }
        
        try:
            # Calculate DNO
            dno = GPACalculator.calculate_dno(grade_entries)
            
            # Calculate semester GPAs
            semester_gpas = GPACalculator.calculate_semester_gpas(grade_entries)
            
            # Calculate total credits
            total_credits = sum(entry.credits for entry in grade_entries if entry.credits > 0)
            
            # Calculate total courses
            total_courses = len(grade_entries)
            
            # Calculate highest and lowest GNO
            gno_values = list(semester_gpas.values())
            highest_gno = max(gno_values) if gno_values else 0.0
            lowest_gno = min(gno_values) if gno_values else 0.0
            average_gno = sum(gno_values) / len(gno_values) if gno_values else 0.0
            
            return {
                'dno': dno,
                'total_credits': total_credits,
                'total_courses': total_courses,
                'semester_gpas': semester_gpas,
                'highest_gno': round(highest_gno, 2),
                'lowest_gno': round(lowest_gno, 2),
                'average_gno': round(average_gno, 2)
            }
            
        except Exception as e:
            logger.error(f"Error calculating GPA statistics: {str(e)}")
            return {
                'dno': 0.0,
                'total_credits': 0,
                'total_courses': 0,
                'semester_gpas': {},
                'highest_gno': 0.0,
                'lowest_gno': 0.0,
                'average_gno': 0.0
            }
    
    @staticmethod
    def letter_grade_to_gpa(letter_grade: str) -> float:
        """
        Convert letter grade to GPA value (4.0 scale).
        
        Args:
            letter_grade: Letter grade (AA, BA, BB, CB, CC, DC, DD, FD, FF)
        
        Returns:
            GPA value (0.0 to 4.0)
        """
        grade_mapping = {
            'AA': 4.0,
            'BA': 3.5,
            'BB': 3.0,
            'CB': 2.5,
            'CC': 2.0,
            'DC': 1.5,
            'DD': 1.0,
            'FD': 0.5,
            'FF': 0.0
        }
        
        return grade_mapping.get(letter_grade.upper(), 0.0)
    
    @staticmethod
    def gpa_to_letter_grade(gpa: float) -> str:
        """
        Convert GPA value to letter grade.
        
        Args:
            gpa: GPA value (0.0 to 4.0)
        
        Returns:
            Letter grade string
        """
        if gpa >= 3.75:
            return 'AA'
        elif gpa >= 3.25:
            return 'BA'
        elif gpa >= 2.75:
            return 'BB'
        elif gpa >= 2.25:
            return 'CB'
        elif gpa >= 1.75:
            return 'CC'
        elif gpa >= 1.25:
            return 'DC'
        elif gpa >= 0.75:
            return 'DD'
        elif gpa >= 0.25:
            return 'FD'
        else:
            return 'FF'
    
    @staticmethod
    def calculate_required_gpa(current_dno: float, current_credits: int, 
                              target_dno: float, new_credits: int) -> float:
        """
        Calculate required GPA for new courses to reach target DNO.
        
        Args:
            current_dno: Current cumulative GPA
            current_credits: Current total credits
            target_dno: Target cumulative GPA
            new_credits: Credits for new courses
        
        Returns:
            Required GPA for new courses, or -1 if impossible, or 0.0 if already above target
        """
        if new_credits <= 0:
            return -1
        
        # If already above target, return 0.0
        if current_dno >= target_dno:
            return 0.0
        
        try:
            current_points = current_dno * current_credits
            target_points = target_dno * (current_credits + new_credits)
            required_points = target_points - current_points
            required_gpa = required_points / new_credits
            
            # Check if achievable
            if required_gpa > 4.0:
                return -1  # Impossible to achieve
            elif required_gpa < 0.0:
                return 0.0  # Already above target
            
            return round(required_gpa, 2)
            
        except Exception as e:
            logger.error(f"Error calculating required GPA: {str(e)}")
            return -1
