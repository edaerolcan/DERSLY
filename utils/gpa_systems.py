"""
GPA Calculation Systems for DERSLY.
Support for different grading scales used by Turkish universities.
"""
from typing import Dict, List, Tuple


class GPASystem:
    """GPA calculation system with customizable grade scales."""
    
    # Pre-defined grade systems
    SYSTEMS = {
        "4.0 Çift Harf": {
            "max_gpa": 4.0,
            "scale": {
                "AA": 4.0,
                "BA": 3.5,
                "BB": 3.0,
                "CB": 2.5,
                "CC": 2.0,
                "DC": 1.5,
                "DD": 1.0,
                "FD": 0.5,
                "FF": 0.0
            },
            "passing_grade": 2.0,
            "description": "4.0'lık sistem - Çift harfli notlar (AA, BA, BB, ...)"
        },
        "4.0 Tek Harf": {
            "max_gpa": 4.0,
            "scale": {
                "A": 4.0,
                "B": 3.0,
                "C": 2.0,
                "D": 1.0,
                "F": 0.0
            },
            "passing_grade": 2.0,
            "description": "4.0'lık sistem - Tek harfli notlar (A, B, C, D, F)"
        },
        "4.0 Artı/Eksi": {
            "max_gpa": 4.0,
            "scale": {
                "A+": 4.0,
                "A": 4.0,
                "A-": 3.7,
                "B+": 3.3,
                "B": 3.0,
                "B-": 2.7,
                "C+": 2.3,
                "C": 2.0,
                "C-": 1.7,
                "D+": 1.3,
                "D": 1.0,
                "F": 0.0
            },
            "passing_grade": 2.0,
            "description": "4.0'lık sistem - Artı/Eksi notlar (A+, A, A-, ...)"
        },
        "5.0 Sistem": {
            "max_gpa": 5.0,
            "scale": {
                "5": 5.0,
                "4": 4.0,
                "3": 3.0,
                "2": 2.0,
                "1": 1.0,
                "0": 0.0
            },
            "passing_grade": 2.5,
            "description": "5.0'lık sistem - Sayısal notlar (5, 4, 3, 2, 1, 0)"
        },
        "100 Sistem": {
            "max_gpa": 100.0,
            "scale": {
                "90-100": 4.0,
                "85-89": 3.5,
                "80-84": 3.0,
                "75-79": 2.5,
                "70-74": 2.0,
                "65-69": 1.5,
                "60-64": 1.0,
                "50-59": 0.5,
                "0-49": 0.0
            },
            "passing_grade": 60.0,
            "description": "100'lük sistem - Yüzdelik notlar"
        }
    }
    
    # University presets
    UNIVERSITY_PRESETS = {
        "Boğaziçi Üniversitesi": "4.0 Tek Harf",
        "İTÜ": "4.0 Çift Harf",
        "ODTÜ": "4.0 Tek Harf",
        "Koç Üniversitesi": "4.0 Artı/Eksi",
        "Sabancı Üniversitesi": "4.0 Artı/Eksi",
        "Bahçeşehir Üniversitesi": "4.0 Artı/Eksi",
        "Bilkent Üniversitesi": "4.0 Tek Harf",
        "Hacettepe Üniversitesi": "4.0 Çift Harf",
        "Ankara Üniversitesi": "4.0 Çift Harf",
        "İstanbul Üniversitesi": "4.0 Çift Harf",
        "Ege Üniversitesi": "4.0 Çift Harf",
        "Marmara Üniversitesi": "4.0 Çift Harf",
        "Yıldız Teknik Üniversitesi": "4.0 Çift Harf"
    }
    
    @staticmethod
    def get_system_names() -> List[str]:
        """Get list of available system names."""
        return list(GPASystem.SYSTEMS.keys())
    
    @staticmethod
    def get_system(system_name: str) -> Dict:
        """Get system configuration by name."""
        return GPASystem.SYSTEMS.get(system_name, GPASystem.SYSTEMS["4.0 Çift Harf"])
    
    @staticmethod
    def get_grade_options(system_name: str) -> List[str]:
        """Get available grade options for a system."""
        system = GPASystem.get_system(system_name)
        return list(system['scale'].keys())
    
    @staticmethod
    def grade_to_point(grade: str, system_name: str) -> float:
        """Convert grade to GPA point."""
        system = GPASystem.get_system(system_name)
        return system['scale'].get(grade, 0.0)
    
    @staticmethod
    def calculate_gpa(grades: List[Tuple[str, int]], system_name: str) -> float:
        """
        Calculate GPA from list of (grade, credits) tuples.
        
        Args:
            grades: List of (grade, credits) tuples
            system_name: Name of the GPA system to use
        
        Returns:
            Calculated GPA
        """
        if not grades:
            return 0.0
        
        total_points = 0.0
        total_credits = 0
        
        for grade, credits in grades:
            point = GPASystem.grade_to_point(grade, system_name)
            total_points += point * credits
            total_credits += credits
        
        if total_credits == 0:
            return 0.0
        
        return total_points / total_credits
    
    @staticmethod
    def get_university_system(university: str) -> str:
        """Get recommended GPA system for a university."""
        return GPASystem.UNIVERSITY_PRESETS.get(university, "4.0 Çift Harf")
    
    @staticmethod
    def get_system_description(system_name: str) -> str:
        """Get description of a GPA system."""
        system = GPASystem.get_system(system_name)
        return system.get('description', '')
    
    @staticmethod
    def validate_grade(grade: str, system_name: str) -> bool:
        """Check if grade is valid for the system."""
        system = GPASystem.get_system(system_name)
        return grade in system['scale']
    
    @staticmethod
    def get_passing_grade(system_name: str) -> float:
        """Get minimum passing grade for the system."""
        system = GPASystem.get_system(system_name)
        return system.get('passing_grade', 2.0)
