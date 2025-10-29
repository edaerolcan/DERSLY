"""
UI Polish Utilities for DERSLY Streamlit application.
Consistent styling and visual polish.
"""
from typing import Dict


class UIPolish:
    """UI polish utilities for consistent styling."""
    
    # Color scheme
    COLORS = {
        'primary': '#667eea',
        'primary_light': '#a5b4fc',
        'primary_dark': '#4c51bf',
        'success': '#48bb78',
        'success_light': '#9ae6b4',
        'success_dark': '#2f855a',
        'warning': '#ed8936',
        'warning_light': '#fbd38d',
        'warning_dark': '#c05621',
        'danger': '#f56565',
        'danger_light': '#fc8181',
        'danger_dark': '#c53030',
        'info': '#4299e1',
        'info_light': '#90cdf4',
        'info_dark': '#2c5282',
        'urgent': '#fc8181',
        'soon': '#f6ad55',
        'later': '#68d391',
        'gray_50': '#f7fafc',
        'gray_100': '#edf2f7',
        'gray_200': '#e2e8f0',
        'gray_300': '#cbd5e0',
        'gray_400': '#a0aec0',
        'gray_500': '#718096',
        'gray_600': '#4a5568',
        'gray_700': '#2d3748',
        'gray_800': '#1a202c',
        'gray_900': '#171923'
    }
    
    # Spacing scale (8px base)
    SPACING = {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        'xxl': '48px',
        'xxxl': '64px'
    }
    
    # Border radius
    RADIUS = {
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
        'full': '9999px'
    }
    
    # Shadows
    SHADOWS = {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)'
    }
    
    # Transitions
    TRANSITIONS = {
        'fast': '150ms',
        'base': '200ms',
        'slow': '300ms',
        'slower': '500ms'
    }
    
    @staticmethod
    def get_card_style(variant: str = 'default', elevated: bool = False) -> str:
        """
        Get consistent card styling.
        
        Args:
            variant: Card variant ('default', 'primary', 'success', 'warning', 'danger')
            elevated: Whether to add elevation shadow
        
        Returns:
            CSS style string
        """
        base_style = f"""
            background: linear-gradient(135deg, {UIPolish.COLORS['gray_50']} 0%, {UIPolish.COLORS['gray_100']} 100%);
            border-radius: {UIPolish.RADIUS['lg']};
            padding: {UIPolish.SPACING['lg']};
            margin-bottom: {UIPolish.SPACING['md']};
            transition: all {UIPolish.TRANSITIONS['base']} ease;
        """
        
        if elevated:
            base_style += f"box-shadow: {UIPolish.SHADOWS['md']};"
        else:
            base_style += f"box-shadow: {UIPolish.SHADOWS['sm']};"
        
        # Add variant-specific styling
        if variant == 'primary':
            base_style += f"border-left: 4px solid {UIPolish.COLORS['primary']};"
        elif variant == 'success':
            base_style += f"border-left: 4px solid {UIPolish.COLORS['success']};"
        elif variant == 'warning':
            base_style += f"border-left: 4px solid {UIPolish.COLORS['warning']};"
        elif variant == 'danger':
            base_style += f"border-left: 4px solid {UIPolish.COLORS['danger']};"
        else:
            base_style += f"border-left: 4px solid {UIPolish.COLORS['gray_300']};"
        
        return base_style
    
    @staticmethod
    def get_button_style(variant: str = 'primary', size: str = 'medium') -> str:
        """
        Get consistent button styling.
        
        Args:
            variant: Button variant ('primary', 'secondary', 'success', 'danger')
            size: Button size ('small', 'medium', 'large')
        
        Returns:
            CSS style string
        """
        # Size-based padding
        padding_map = {
            'small': f"{UIPolish.SPACING['sm']} {UIPolish.SPACING['md']}",
            'medium': f"{UIPolish.SPACING['md']} {UIPolish.SPACING['lg']}",
            'large': f"{UIPolish.SPACING['lg']} {UIPolish.SPACING['xl']}"
        }
        
        base_style = f"""
            padding: {padding_map.get(size, padding_map['medium'])};
            border-radius: {UIPolish.RADIUS['md']};
            font-weight: 600;
            transition: all {UIPolish.TRANSITIONS['base']} ease;
            cursor: pointer;
            border: none;
            min-height: 44px;
        """
        
        # Variant-specific colors
        if variant == 'primary':
            base_style += f"""
                background: {UIPolish.COLORS['primary']};
                color: white;
            """
        elif variant == 'secondary':
            base_style += f"""
                background: {UIPolish.COLORS['gray_200']};
                color: {UIPolish.COLORS['gray_700']};
            """
        elif variant == 'success':
            base_style += f"""
                background: {UIPolish.COLORS['success']};
                color: white;
            """
        elif variant == 'danger':
            base_style += f"""
                background: {UIPolish.COLORS['danger']};
                color: white;
            """
        
        return base_style
    
    @staticmethod
    def get_status_badge(status: str) -> str:
        """
        Get styled status badge HTML.
        
        Args:
            status: Status type ('pending', 'completed', 'overdue')
        
        Returns:
            HTML string for status badge
        """
        badge_styles = {
            'pending': {
                'bg': UIPolish.COLORS['warning_light'],
                'color': UIPolish.COLORS['warning_dark'],
                'icon': '⏳',
                'label': 'Bekliyor'
            },
            'completed': {
                'bg': UIPolish.COLORS['success_light'],
                'color': UIPolish.COLORS['success_dark'],
                'icon': '✅',
                'label': 'Tamamlandı'
            },
            'overdue': {
                'bg': UIPolish.COLORS['danger_light'],
                'color': UIPolish.COLORS['danger_dark'],
                'icon': '⚠️',
                'label': 'Gecikti'
            }
        }
        
        style = badge_styles.get(status, badge_styles['pending'])
        
        return f"""
        <span style="
            background-color: {style['bg']};
            color: {style['color']};
            padding: {UIPolish.SPACING['xs']} {UIPolish.SPACING['md']};
            border-radius: {UIPolish.RADIUS['full']};
            font-size: 0.875rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: {UIPolish.SPACING['xs']};
        ">
            {style['icon']} {style['label']}
        </span>
        """
    
    @staticmethod
    def get_urgency_badge(urgency: str, label: str = None) -> str:
        """
        Get styled urgency badge HTML.
        
        Args:
            urgency: Urgency level ('urgent', 'soon', 'later')
            label: Optional custom label
        
        Returns:
            HTML string for urgency badge
        """
        badge_styles = {
            'urgent': {
                'bg': UIPolish.COLORS['urgent'],
                'color': 'white',
                'icon': '🔴'
            },
            'soon': {
                'bg': UIPolish.COLORS['soon'],
                'color': 'white',
                'icon': '🟡'
            },
            'later': {
                'bg': UIPolish.COLORS['later'],
                'color': 'white',
                'icon': '🟢'
            }
        }
        
        style = badge_styles.get(urgency, badge_styles['later'])
        display_label = label if label else urgency.capitalize()
        
        return f"""
        <span style="
            background-color: {style['bg']};
            color: {style['color']};
            padding: {UIPolish.SPACING['sm']} {UIPolish.SPACING['md']};
            border-radius: {UIPolish.RADIUS['full']};
            font-size: 0.875rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: {UIPolish.SPACING['xs']};
            box-shadow: {UIPolish.SHADOWS['sm']};
        ">
            {style['icon']} {display_label}
        </span>
        """
    
    @staticmethod
    def get_priority_badge(priority: str) -> str:
        """
        Get styled priority badge HTML.
        
        Args:
            priority: Priority level ('low', 'medium', 'high')
        
        Returns:
            HTML string for priority badge
        """
        badge_styles = {
            'high': {
                'bg': UIPolish.COLORS['danger_light'],
                'color': UIPolish.COLORS['danger_dark'],
                'icon': '🔴',
                'label': 'Yüksek'
            },
            'medium': {
                'bg': UIPolish.COLORS['warning_light'],
                'color': UIPolish.COLORS['warning_dark'],
                'icon': '🟡',
                'label': 'Orta'
            },
            'low': {
                'bg': UIPolish.COLORS['success_light'],
                'color': UIPolish.COLORS['success_dark'],
                'icon': '🟢',
                'label': 'Düşük'
            }
        }
        
        style = badge_styles.get(priority, badge_styles['medium'])
        
        return f"""
        <span style="
            background-color: {style['bg']};
            color: {style['color']};
            padding: {UIPolish.SPACING['xs']} {UIPolish.SPACING['sm']};
            border-radius: {UIPolish.RADIUS['md']};
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: {UIPolish.SPACING['xs']};
        ">
            {style['icon']} {style['label']}
        </span>
        """
    
    @staticmethod
    def get_empty_state(icon: str, title: str, description: str) -> str:
        """
        Get styled empty state HTML.
        
        Args:
            icon: Emoji icon
            title: Title text
            description: Description text
        
        Returns:
            HTML string for empty state
        """
        return f"""
        <div style="
            text-align: center;
            padding: {UIPolish.SPACING['xxxl']};
            background: linear-gradient(135deg, {UIPolish.COLORS['gray_50']} 0%, {UIPolish.COLORS['gray_100']} 100%);
            border-radius: {UIPolish.RADIUS['xl']};
            margin: {UIPolish.SPACING['xl']} 0;
        ">
            <div style="font-size: 4rem; margin-bottom: {UIPolish.SPACING['lg']};">
                {icon}
            </div>
            <h3 style="
                color: {UIPolish.COLORS['gray_700']};
                margin-bottom: {UIPolish.SPACING['md']};
                font-size: 1.5rem;
            ">
                {title}
            </h3>
            <p style="
                color: {UIPolish.COLORS['gray_500']};
                font-size: 1rem;
                max-width: 500px;
                margin: 0 auto;
            ">
                {description}
            </p>
        </div>
        """
