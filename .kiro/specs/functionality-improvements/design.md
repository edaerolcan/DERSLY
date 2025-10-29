# Design Document

## Overview

This design document outlines improvements to ensure all DERSLY functionality works correctly, implements a functional reminder system, polishes the UI, and ensures mobile responsiveness. The focus is on creating a production-ready, polished application that works seamlessly across all devices.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DERSLY Application                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              UI Layer (Streamlit Pages)              │   │
│  │                                                        │   │
│  │  - Responsive Layout                                  │   │
│  │  - Mobile-First Design                                │   │
│  │  - Consistent Styling                                 │   │
│  │  - Touch-Friendly Controls                            │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│                            ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Functionality Layer                         │   │
│  │                                                        │   │
│  │  - Button Actions                                     │   │
│  │  - Navigation                                         │   │
│  │  - Form Handling                                      │   │
│  │  - Data Operations                                    │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│                            ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Reminder System                             │   │
│  │                                                        │   │
│  │  - ReminderManager                                    │   │
│  │  - Urgency Calculator                                 │   │
│  │  - Filter & Sort                                      │   │
│  │  - Notification Display                               │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│                            ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Mobile Responsive Utilities                 │   │
│  │                                                        │   │
│  │  - Responsive Helpers                                 │   │
│  │  - Touch Optimization                                 │   │
│  │  - Viewport Detection                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Reminder Manager Component

**Location**: `utils/reminder_manager.py`

**Purpose**: Manage reminders and calculate urgency for upcoming assignments

**Interface**:

```python
class ReminderManager:
    """Manages reminders for upcoming assignments."""
    
    @staticmethod
    def get_reminders(days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Get reminders for assignments due within specified days."""
        pass
    
    @staticmethod
    def get_urgent_reminders() -> List[Dict[str, Any]]:
        """Get urgent reminders (due today or overdue)."""
        pass
    
    @staticmethod
    def get_reminders_by_period(period: str) -> List[Dict[str, Any]]:
        """Get reminders by period (today, tomorrow, this_week, custom)."""
        pass
    
    @staticmethod
    def calculate_urgency(due_date: datetime) -> Tuple[str, str, int]:
        """
        Calculate urgency level for a reminder.
        Returns: (color, label, urgency_score)
        """
        pass
    
    @staticmethod
    def get_reminder_count() -> Dict[str, int]:
        """Get count of reminders by urgency level."""
        pass
```

### 2. Mobile Responsive Utilities

**Location**: `utils/mobile_utils.py`

**Purpose**: Helper functions for mobile-responsive design

**Interface**:

```python
class MobileUtils:
    """Utilities for mobile-responsive design."""
    
    @staticmethod
    def get_column_config(mobile_cols: int = 1, tablet_cols: int = 2, 
                         desktop_cols: int = 3) -> int:
        """Get appropriate column count based on viewport."""
        pass
    
    @staticmethod
    def is_mobile() -> bool:
        """Detect if user is on mobile device."""
        pass
    
    @staticmethod
    def get_button_size() -> str:
        """Get appropriate button size for device."""
        pass
    
    @staticmethod
    def get_spacing() -> Dict[str, str]:
        """Get responsive spacing values."""
        pass
```

### 3. UI Polish Utilities

**Location**: `utils/ui_polish.py`

**Purpose**: Consistent UI styling and polish

**Interface**:

```python
class UIPolish:
    """UI polish utilities for consistent styling."""
    
    # Color scheme
    COLORS = {
        'primary': '#667eea',
        'success': '#48bb78',
        'warning': '#ed8936',
        'danger': '#f56565',
        'info': '#4299e1',
        'urgent': '#fc8181',
        'soon': '#f6ad55',
        'later': '#68d391'
    }
    
    # Spacing scale
    SPACING = {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        'xxl': '48px'
    }
    
    @staticmethod
    def get_card_style(variant: str = 'default') -> str:
        """Get consistent card styling."""
        pass
    
    @staticmethod
    def get_button_style(variant: str = 'primary') -> str:
        """Get consistent button styling."""
        pass
    
    @staticmethod
    def get_status_badge(status: str) -> str:
        """Get styled status badge."""
        pass
    
    @staticmethod
    def get_urgency_badge(urgency: str) -> str:
        """Get styled urgency badge."""
        pass
```

## Data Models

### Reminder Model

```python
@dataclass
class Reminder:
    """Reminder data model."""
    id: int
    assignment_id: int
    title: str
    description: Optional[str]
    due_date: datetime
    type: str  # assignment, exam, project, quiz
    priority: str  # low, medium, high
    status: str  # pending, completed
    urgency_level: str  # urgent, soon, later
    urgency_color: str  # red, yellow, green
    urgency_score: int  # 0-5
    days_remaining: int
    hours_remaining: int
```

### Mobile Config Model

```python
@dataclass
class MobileConfig:
    """Mobile configuration model."""
    is_mobile: bool
    is_tablet: bool
    is_desktop: bool
    columns: int
    button_size: str
    font_size: str
    spacing: str
```

## Design Decisions

### 1. Reminder System Design

**Urgency Levels:**
- **Urgent (Red)**: Overdue or due today
- **Soon (Yellow)**: Due tomorrow or within 3 days
- **Later (Green)**: Due in 4-7 days

**Display Strategy:**
- Group reminders by urgency
- Show urgent reminders first
- Use color coding for visual hierarchy
- Display countdown (days/hours remaining)
- Show assignment type and priority

**Filtering Options:**
- Today: Due today
- Tomorrow: Due tomorrow
- This Week: Due within 7 days
- Custom: User-defined date range

### 2. Mobile Responsiveness Strategy

**Breakpoints:**
- Mobile: < 768px (1 column)
- Tablet: 768px - 1024px (2 columns)
- Desktop: > 1024px (3+ columns)

**Touch Optimization:**
- Minimum button size: 44x44 pixels
- Minimum spacing: 8px between elements
- Large tap targets for all interactive elements
- Swipe gestures for navigation (where applicable)

**Layout Adaptations:**
- Stack columns vertically on mobile
- Collapsible sidebar on mobile
- Full-width forms on mobile
- Simplified navigation on mobile

### 3. UI Polish Strategy

**Consistency:**
- Use design tokens for colors, spacing, typography
- Consistent border radius (8px for cards, 4px for buttons)
- Consistent shadows (subtle elevation)
- Consistent animations (200ms transitions)

**Visual Hierarchy:**
- Clear heading hierarchy (h1, h2, h3)
- Emphasis on important information
- Subtle backgrounds for sections
- Color coding for status and urgency

**Micro-interactions:**
- Hover effects on buttons
- Loading states for actions
- Success/error animations
- Smooth transitions

### 4. Navigation Fix Strategy

**Page References:**
- Use correct file names with Turkish characters
- Handle navigation errors gracefully
- Maintain session state during navigation
- Add loading indicators for page transitions

**Correct Page Names:**
```python
PAGES = {
    'home': 'pages/1_🏠_Ana_Sayfa.py',
    'courses': 'pages/2_📚_Dersler.py',
    'assignments': 'pages/3_📝_Ödevler.py',
    'calendar': 'pages/4_📅_Takvim.py',
    'reminders': 'pages/5_🔔_Hatırlatıcılar.py',
    'gpa': 'pages/6_📊_Not_Ortalaması.py',
    'profile': 'pages/7_👤_Profil.py'
}
```

## Implementation Strategy

### Phase 1: Fix Navigation and Button Actions
1. Update all navigation button references
2. Test all button actions
3. Add error handling for failed actions
4. Add confirmation dialogs for destructive actions

### Phase 2: Implement Reminder System
1. Create ReminderManager class
2. Implement urgency calculation
3. Update Hatırlatıcılar page with full functionality
4. Add reminder count to sidebar

### Phase 3: Mobile Responsiveness
1. Create MobileUtils helper
2. Update all pages with responsive layouts
3. Test on different screen sizes
4. Optimize touch interactions

### Phase 4: UI Polish
1. Create UIPolish utilities
2. Apply consistent styling across all pages
3. Add animations and transitions
4. Improve visual hierarchy

### Phase 5: Performance Optimization
1. Add caching where appropriate
2. Optimize data queries
3. Add loading indicators
4. Test performance

## Testing Strategy

### Functional Testing
- Test all button actions
- Test all navigation links
- Test form submissions
- Test data operations (CRUD)
- Test reminder filtering and sorting

### Mobile Testing
- Test on mobile devices (iOS, Android)
- Test on tablets
- Test on different screen sizes
- Test touch interactions
- Test responsive layouts

### UI Testing
- Visual regression testing
- Consistency checks
- Accessibility testing
- Cross-browser testing

### Performance Testing
- Page load times
- Button response times
- Data query performance
- Memory usage

## Accessibility Considerations

1. **Keyboard Navigation**: All interactive elements accessible via keyboard
2. **Screen Readers**: Semantic HTML and ARIA labels
3. **Color Contrast**: WCAG AA compliance (4.5:1 for text)
4. **Focus Indicators**: Visible focus states
5. **Text Alternatives**: Alt text for icons and images
6. **Zoom Support**: Works up to 200% zoom

## Mobile-Specific Considerations

1. **Touch Targets**: Minimum 44x44 pixels
2. **Spacing**: Adequate spacing for fat fingers
3. **Viewport**: Proper viewport meta tag
4. **Orientation**: Support both portrait and landscape
5. **Performance**: Optimize for mobile networks
6. **Gestures**: Support common mobile gestures

## Error Handling

### Navigation Errors
```python
try:
    st.switch_page(page_path)
except Exception as e:
    st.error(f"❌ Sayfa yüklenemedi: {str(e)}")
    st.info("🔄 Lütfen sayfayı yenileyin veya ana sayfaya dönün")
```

### Button Action Errors
```python
try:
    result = perform_action()
    if result:
        st.success("✅ İşlem başarılı!")
    else:
        st.error("❌ İşlem başarısız oldu")
except Exception as e:
    st.error(f"❌ Hata: {str(e)}")
```

## Performance Optimizations

1. **Caching**: Use `@st.cache_data` for expensive operations
2. **Lazy Loading**: Load data only when needed
3. **Debouncing**: Debounce search and filter operations
4. **Pagination**: Paginate large lists
5. **Memoization**: Cache computed values

## Future Enhancements

1. **Push Notifications**: Browser push notifications for reminders
2. **Email Notifications**: Email reminders for upcoming deadlines
3. **Dark Mode**: Dark theme support
4. **Offline Support**: PWA with offline capabilities
5. **Sync**: Cloud sync across devices
6. **Widgets**: Dashboard widgets for quick access
7. **Shortcuts**: Keyboard shortcuts for power users
8. **Export**: Export reminders to calendar apps

## Security Considerations

1. **Input Validation**: Already implemented
2. **XSS Prevention**: Streamlit handles HTML escaping
3. **CSRF Protection**: Streamlit session management
4. **Data Privacy**: All data stored locally in browser

## Deployment Considerations

1. **Browser Compatibility**: Test on Chrome, Firefox, Safari, Edge
2. **Mobile Browsers**: Test on mobile Chrome, Safari
3. **Performance**: Optimize for production
4. **Monitoring**: Add error tracking
5. **Analytics**: Track usage patterns
