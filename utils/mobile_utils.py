"""
Mobile Utilities for DERSLY Streamlit application.
Helper functions for mobile-responsive design.
"""
import streamlit as st
from typing import Dict


class MobileUtils:
    """Utilities for mobile-responsive design."""
    
    # Breakpoints (in pixels)
    MOBILE_MAX = 768
    TABLET_MAX = 1024
    
    @staticmethod
    def get_column_config(mobile_cols: int = 1, tablet_cols: int = 2, 
                         desktop_cols: int = 3) -> int:
        """
        Get appropriate column count based on viewport.
        
        Args:
            mobile_cols: Number of columns for mobile (default: 1)
            tablet_cols: Number of columns for tablet (default: 2)
            desktop_cols: Number of columns for desktop (default: 3)
        
        Returns:
            Number of columns to use
        
        Note:
            Streamlit doesn't provide direct viewport detection,
            so we return desktop_cols by default and rely on CSS
            for responsive behavior.
        """
        # Streamlit doesn't provide viewport width detection
        # Return desktop columns and rely on CSS media queries
        return desktop_cols
    
    @staticmethod
    def is_mobile() -> bool:
        """
        Detect if user is on mobile device.
        
        Returns:
            True if mobile, False otherwise
        
        Note:
            Streamlit doesn't provide direct device detection.
            This is a placeholder that always returns False.
            Use CSS media queries for actual responsive behavior.
        """
        # Streamlit doesn't provide device detection
        # Return False and rely on CSS media queries
        return False
    
    @staticmethod
    def get_button_size() -> str:
        """
        Get appropriate button size for device.
        
        Returns:
            Button size class ('small', 'medium', 'large')
        """
        # Return medium by default
        # CSS will handle responsive sizing
        return 'medium'
    
    @staticmethod
    def get_spacing() -> Dict[str, str]:
        """
        Get responsive spacing values.
        
        Returns:
            Dictionary of spacing values
        """
        return {
            'xs': '4px',
            'sm': '8px',
            'md': '16px',
            'lg': '24px',
            'xl': '32px',
            'xxl': '48px'
        }
    
    @staticmethod
    def get_responsive_css() -> str:
        """
        Get CSS for mobile responsiveness.
        
        Returns:
            CSS string with media queries
        """
        return """
        <style>
        /* Mobile Responsive Styles */
        
        /* Base styles for all devices */
        * {
            box-sizing: border-box;
        }
        
        /* Ensure minimum touch target size */
        button, a, input, select, textarea {
            min-height: 44px;
            min-width: 44px;
        }
        
        /* Responsive typography */
        body {
            font-size: 16px;
            line-height: 1.6;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        h3 {
            font-size: 1.25rem;
        }
        
        /* Mobile styles (< 768px) */
        @media (max-width: 768px) {
            /* Stack columns */
            .row-widget.stHorizontalBlock {
                flex-direction: column !important;
            }
            
            .row-widget.stHorizontalBlock > div {
                width: 100% !important;
                margin-bottom: 1rem;
            }
            
            /* Full width buttons */
            button {
                width: 100% !important;
                margin-bottom: 0.5rem;
            }
            
            /* Larger text for readability */
            body {
                font-size: 14px;
            }
            
            h1 {
                font-size: 1.75rem;
            }
            
            h2 {
                font-size: 1.25rem;
            }
            
            h3 {
                font-size: 1.1rem;
            }
            
            /* Adjust padding */
            .main .block-container {
                padding: 1rem !important;
            }
            
            /* Cards stack */
            .custom-card, .stats-card {
                margin-bottom: 1rem;
            }
            
            /* Forms */
            input, select, textarea {
                font-size: 16px !important; /* Prevent zoom on iOS */
            }
        }
        
        /* Tablet styles (768px - 1024px) */
        @media (min-width: 768px) and (max-width: 1024px) {
            /* 2 columns on tablet */
            .row-widget.stHorizontalBlock > div {
                width: 48% !important;
            }
            
            h1 {
                font-size: 1.875rem;
            }
            
            h2 {
                font-size: 1.375rem;
            }
        }
        
        /* Desktop styles (> 1024px) */
        @media (min-width: 1024px) {
            /* Default desktop styles */
        }
        
        /* Touch-friendly spacing */
        @media (hover: none) and (pointer: coarse) {
            /* Increase spacing for touch devices */
            button, a {
                padding: 12px 24px !important;
                margin: 8px 0 !important;
            }
            
            .stButton button {
                min-height: 48px !important;
            }
        }
        
        /* Landscape orientation on mobile */
        @media (max-width: 768px) and (orientation: landscape) {
            /* Adjust for landscape */
            .main .block-container {
                padding: 0.5rem !important;
            }
        }
        </style>
        """
    
    @staticmethod
    def apply_mobile_styles():
        """Apply mobile-responsive styles to the page."""
        st.markdown(MobileUtils.get_responsive_css(), unsafe_allow_html=True)
