"""
Calendar Export Utilities for DERSLY Streamlit application.
Export assignments and courses to iCalendar (.ics) format for mobile calendar integration.
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List
import base64


class CalendarExport:
    """Utilities for exporting to calendar formats."""
    
    @staticmethod
    def create_ics_event(
        title: str,
        description: str,
        start_datetime: datetime,
        end_datetime: datetime = None,
        location: str = "",
        alarm_minutes: int = 60
    ) -> str:
        """
        Create an iCalendar (.ics) event.
        
        Args:
            title: Event title
            description: Event description
            start_datetime: Start date and time
            end_datetime: End date and time (optional, defaults to start + 1 hour)
            location: Event location (optional)
            alarm_minutes: Minutes before event to trigger alarm (default: 60)
        
        Returns:
            iCalendar format string
        """
        if end_datetime is None:
            end_datetime = start_datetime + timedelta(hours=1)
        
        # Format dates in iCalendar format (YYYYMMDDTHHMMSS)
        start_str = start_datetime.strftime("%Y%m%dT%H%M%S")
        end_str = end_datetime.strftime("%Y%m%dT%H%M%S")
        
        # Create unique ID
        uid = f"{start_str}-{hash(title)}@dersly.app"
        
        # Current timestamp
        dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        
        # Escape special characters in text fields
        title = title.replace(',', '\\,').replace(';', '\\;').replace('\\', '\\\\')
        description = description.replace(',', '\\,').replace(';', '\\;').replace('\\', '\\\\')
        location = location.replace(',', '\\,').replace(';', '\\;').replace('\\', '\\\\')
        
        # Build iCalendar content
        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//DERSLY//Student Support Platform//TR
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART:{start_str}
DTEND:{end_str}
SUMMARY:{title}
DESCRIPTION:{description}
LOCATION:{location}
STATUS:CONFIRMED
SEQUENCE:0
BEGIN:VALARM
TRIGGER:-PT{alarm_minutes}M
ACTION:DISPLAY
DESCRIPTION:Hatırlatma: {title}
END:VALARM
END:VEVENT
END:VCALENDAR"""
        
        return ics_content
    
    @staticmethod
    def create_assignment_ics(assignment: Dict[str, Any]) -> str:
        """
        Create iCalendar event from assignment.
        
        Args:
            assignment: Assignment dictionary
        
        Returns:
            iCalendar format string
        """
        # Parse due date
        due_date_str = assignment.get('due_date', '')
        try:
            if 'T' in due_date_str:
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            else:
                due_date = datetime.fromisoformat(due_date_str)
        except:
            due_date = datetime.now() + timedelta(days=7)
        
        # Get assignment details
        title = assignment.get('title', 'Ödev')
        description = assignment.get('description', '')
        assignment_type = assignment.get('type', 'assignment')
        priority = assignment.get('priority', 'medium')
        
        # Add type and priority to description
        type_labels = {
            'assignment': 'Ödev',
            'exam': 'Sınav',
            'project': 'Proje',
            'quiz': 'Quiz'
        }
        priority_labels = {
            'high': 'Yüksek',
            'medium': 'Orta',
            'low': 'Düşük'
        }
        
        full_description = f"""Tür: {type_labels.get(assignment_type, 'Ödev')}
Öncelik: {priority_labels.get(priority, 'Orta')}

{description}

DERSLY - Öğrenci Destek Platformu"""
        
        # Set alarm based on priority
        alarm_map = {
            'high': 120,  # 2 hours before
            'medium': 60,  # 1 hour before
            'low': 30     # 30 minutes before
        }
        alarm_minutes = alarm_map.get(priority, 60)
        
        # Create event (1 hour duration)
        return CalendarExport.create_ics_event(
            title=f"{type_labels.get(assignment_type, 'Ödev')}: {title}",
            description=full_description,
            start_datetime=due_date - timedelta(hours=1),
            end_datetime=due_date,
            location="DERSLY",
            alarm_minutes=alarm_minutes
        )
    
    @staticmethod
    def create_course_ics(course: Dict[str, Any], weeks: int = 14) -> str:
        """
        Create recurring iCalendar events for a course.
        
        Args:
            course: Course dictionary
            weeks: Number of weeks to create events for (default: 14, one semester)
        
        Returns:
            iCalendar format string with recurring events
        """
        # Get course details
        course_name = course.get('course_name', 'Ders')
        course_code = course.get('course_code', '')
        day = course.get('day', 'Monday')
        start_time_str = course.get('start_time', '09:00')
        end_time_str = course.get('end_time', '10:30')
        
        # Map day names to weekday numbers (Monday=0, Sunday=6)
        day_map = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6
        }
        
        # Find next occurrence of the day
        today = datetime.now()
        target_weekday = day_map.get(day, 0)
        days_ahead = target_weekday - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        
        next_occurrence = today + timedelta(days=days_ahead)
        
        # Parse times
        start_hour, start_min = map(int, start_time_str.split(':'))
        end_hour, end_min = map(int, end_time_str.split(':'))
        
        # Create start and end datetime
        start_datetime = next_occurrence.replace(hour=start_hour, minute=start_min, second=0, microsecond=0)
        end_datetime = next_occurrence.replace(hour=end_hour, minute=end_min, second=0, microsecond=0)
        
        # Calculate until date (weeks from now)
        until_date = start_datetime + timedelta(weeks=weeks)
        until_str = until_date.strftime("%Y%m%dT%H%M%S")
        
        # Format dates
        start_str = start_datetime.strftime("%Y%m%dT%H%M%S")
        end_str = end_datetime.strftime("%Y%m%dT%H%M%S")
        
        # Create unique ID
        uid = f"{start_str}-{hash(course_name)}@dersly.app"
        dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        
        # Escape special characters
        title = f"{course_code} - {course_name}".replace(',', '\\,').replace(';', '\\;')
        
        # Build recurring event
        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//DERSLY//Student Support Platform//TR
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART:{start_str}
DTEND:{end_str}
RRULE:FREQ=WEEKLY;UNTIL={until_str}
SUMMARY:{title}
DESCRIPTION:Ders Kodu: {course_code}\\nDers Adı: {course_name}\\n\\nDERSLY - Öğrenci Destek Platformu
LOCATION:Kampüs
STATUS:CONFIRMED
SEQUENCE:0
BEGIN:VALARM
TRIGGER:-PT15M
ACTION:DISPLAY
DESCRIPTION:Hatırlatma: {title} 15 dakika sonra başlıyor
END:VALARM
END:VEVENT
END:VCALENDAR"""
        
        return ics_content
    
    @staticmethod
    def create_download_link(ics_content: str, filename: str) -> str:
        """
        Create a download link for iCalendar content.
        
        Args:
            ics_content: iCalendar format string
            filename: Filename for download (without .ics extension)
        
        Returns:
            HTML download link
        """
        # Encode content to base64
        b64 = base64.b64encode(ics_content.encode()).decode()
        
        # Create download link
        href = f'data:text/calendar;base64,{b64}'
        
        return f"""
        <a href="{href}" download="{filename}.ics" style="
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 12px rgba(0, 0, 0, 0.15)';" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px rgba(0, 0, 0, 0.1)';">
            📅 Takvime Ekle (.ics)
        </a>
        """
    
    @staticmethod
    def create_multiple_events_ics(assignments: List[Dict[str, Any]]) -> str:
        """
        Create iCalendar file with multiple assignment events.
        
        Args:
            assignments: List of assignment dictionaries
        
        Returns:
            iCalendar format string with multiple events
        """
        # Start calendar
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//DERSLY//Student Support Platform//TR
CALSCALE:GREGORIAN
METHOD:PUBLISH
"""
        
        # Add each assignment as an event
        for assignment in assignments:
            try:
                # Parse due date
                due_date_str = assignment.get('due_date', '')
                if 'T' in due_date_str:
                    due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                else:
                    due_date = datetime.fromisoformat(due_date_str)
                
                # Get details
                title = assignment.get('title', 'Ödev')
                description = assignment.get('description', '')
                assignment_type = assignment.get('type', 'assignment')
                priority = assignment.get('priority', 'medium')
                
                type_labels = {
                    'assignment': 'Ödev',
                    'exam': 'Sınav',
                    'project': 'Proje',
                    'quiz': 'Quiz'
                }
                
                # Format dates
                start_datetime = due_date - timedelta(hours=1)
                start_str = start_datetime.strftime("%Y%m%dT%H%M%S")
                end_str = due_date.strftime("%Y%m%dT%H%M%S")
                
                uid = f"{start_str}-{hash(title)}-{assignment.get('id', 0)}@dersly.app"
                dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
                
                # Escape text
                event_title = f"{type_labels.get(assignment_type, 'Ödev')}: {title}".replace(',', '\\,').replace(';', '\\;')
                event_desc = description.replace(',', '\\,').replace(';', '\\;')
                
                # Alarm based on priority
                alarm_map = {'high': 120, 'medium': 60, 'low': 30}
                alarm_minutes = alarm_map.get(priority, 60)
                
                # Add event
                ics_content += f"""BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART:{start_str}
DTEND:{end_str}
SUMMARY:{event_title}
DESCRIPTION:{event_desc}
LOCATION:DERSLY
STATUS:CONFIRMED
SEQUENCE:0
BEGIN:VALARM
TRIGGER:-PT{alarm_minutes}M
ACTION:DISPLAY
DESCRIPTION:Hatırlatma: {event_title}
END:VALARM
END:VEVENT
"""
            except:
                # Skip invalid assignments
                continue
        
        # End calendar
        ics_content += "END:VCALENDAR"
        
        return ics_content
