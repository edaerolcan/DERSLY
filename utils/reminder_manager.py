"""
Reminder Manager for DERSLY Streamlit application.
Manages reminders and calculates urgency for upcoming assignments.
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from utils.assignment_manager import AssignmentManager


class ReminderManager:
    """Manages reminders for upcoming assignments."""
    
    @staticmethod
    def get_reminders(days_ahead: int = 7) -> List[Dict[str, Any]]:
        """
        Get reminders for assignments due within specified days.
        
        Args:
            days_ahead: Number of days to look ahead (default: 7)
        
        Returns:
            List of reminder dictionaries with urgency information
        """
        # Get all pending assignments
        assignments = AssignmentManager.get_assignments_by_status('pending')
        
        now = datetime.now()
        future = now + timedelta(days=days_ahead)
        
        reminders = []
        for assignment in assignments:
            try:
                # Parse due date
                due_date_str = assignment.get('due_date', '')
                if 'T' in due_date_str:
                    due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                else:
                    due_date = datetime.fromisoformat(due_date_str)
                
                # Check if within range (including overdue)
                if due_date <= future:
                    # Calculate urgency
                    urgency_color, urgency_label, urgency_score = ReminderManager.calculate_urgency(due_date)
                    
                    # Calculate time remaining
                    time_diff = due_date - now
                    days_remaining = time_diff.days
                    hours_remaining = int(time_diff.total_seconds() / 3600)
                    
                    # Create reminder
                    reminder = {
                        **assignment,  # Include all assignment data
                        'urgency_color': urgency_color,
                        'urgency_label': urgency_label,
                        'urgency_score': urgency_score,
                        'days_remaining': days_remaining,
                        'hours_remaining': hours_remaining,
                        'due_date_obj': due_date
                    }
                    reminders.append(reminder)
            except (ValueError, AttributeError):
                # Skip assignments with invalid dates
                continue
        
        # Sort by urgency score (highest first), then by due date
        reminders.sort(key=lambda x: (-x['urgency_score'], x['due_date_obj']))
        
        return reminders
    
    @staticmethod
    def get_urgent_reminders() -> List[Dict[str, Any]]:
        """
        Get urgent reminders (due today or overdue).
        
        Returns:
            List of urgent reminder dictionaries
        """
        all_reminders = ReminderManager.get_reminders(days_ahead=1)
        return [r for r in all_reminders if r['urgency_score'] >= 4]
    
    @staticmethod
    def get_reminders_by_period(period: str) -> List[Dict[str, Any]]:
        """
        Get reminders by period.
        
        Args:
            period: Time period ('today', 'tomorrow', 'this_week', 'all')
        
        Returns:
            List of reminder dictionaries for the specified period
        """
        now = datetime.now()
        
        if period == 'today':
            # Due today
            end_of_today = now.replace(hour=23, minute=59, second=59)
            reminders = ReminderManager.get_reminders(days_ahead=1)
            return [r for r in reminders if r['due_date_obj'] <= end_of_today]
        
        elif period == 'tomorrow':
            # Due tomorrow
            start_of_tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0)
            end_of_tomorrow = (now + timedelta(days=1)).replace(hour=23, minute=59, second=59)
            reminders = ReminderManager.get_reminders(days_ahead=2)
            return [r for r in reminders if start_of_tomorrow <= r['due_date_obj'] <= end_of_tomorrow]
        
        elif period == 'this_week':
            # Due within 7 days
            return ReminderManager.get_reminders(days_ahead=7)
        
        elif period == 'all':
            # All pending assignments
            return ReminderManager.get_reminders(days_ahead=365)
        
        else:
            return []
    
    @staticmethod
    def calculate_urgency(due_date: datetime) -> Tuple[str, str, int]:
        """
        Calculate urgency level for a reminder.
        
        Args:
            due_date: Due date of the assignment
        
        Returns:
            Tuple of (color, label, urgency_score)
            - color: CSS color for display (red, yellow, green)
            - label: Turkish label for urgency
            - urgency_score: Numeric score (0-5, higher is more urgent)
        """
        now = datetime.now()
        time_diff = due_date - now
        
        # Overdue
        if time_diff.total_seconds() < 0:
            days_overdue = abs(time_diff.days)
            return '#fc8181', f'{days_overdue} gün gecikti', 5
        
        # Due today
        if time_diff.days == 0:
            hours_left = int(time_diff.total_seconds() / 3600)
            if hours_left < 3:
                return '#fc8181', f'{hours_left} saat kaldı!', 4
            return '#fc8181', 'Bugün bitiyor!', 4
        
        # Due tomorrow
        if time_diff.days == 1:
            return '#f6ad55', 'Yarın bitiyor', 3
        
        # Due in 2-3 days
        if time_diff.days <= 3:
            return '#f6ad55', f'{time_diff.days} gün kaldı', 2
        
        # Due in 4-7 days
        if time_diff.days <= 7:
            return '#68d391', f'{time_diff.days} gün kaldı', 1
        
        # More than a week
        return '#68d391', f'{time_diff.days} gün kaldı', 0
    
    @staticmethod
    def get_reminder_count() -> Dict[str, int]:
        """
        Get count of reminders by urgency level.
        
        Returns:
            Dictionary with counts: {
                'urgent': count of urgent reminders (score >= 4),
                'soon': count of soon reminders (score 2-3),
                'later': count of later reminders (score 0-1),
                'total': total count
            }
        """
        reminders = ReminderManager.get_reminders(days_ahead=7)
        
        urgent = sum(1 for r in reminders if r['urgency_score'] >= 4)
        soon = sum(1 for r in reminders if 2 <= r['urgency_score'] < 4)
        later = sum(1 for r in reminders if r['urgency_score'] < 2)
        
        return {
            'urgent': urgent,
            'soon': soon,
            'later': later,
            'total': len(reminders)
        }
    
    @staticmethod
    def get_reminder_by_id(reminder_id: int) -> Dict[str, Any]:
        """
        Get a specific reminder by assignment ID.
        
        Args:
            reminder_id: Assignment ID
        
        Returns:
            Reminder dictionary or None if not found
        """
        reminders = ReminderManager.get_reminders(days_ahead=365)
        for reminder in reminders:
            if reminder['id'] == reminder_id:
                return reminder
        return None
