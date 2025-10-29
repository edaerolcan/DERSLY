"""
UI helper utilities for DERSLY Streamlit application.
Provides reusable UI components and functions.
"""
import streamlit as st
from typing import Optional, Callable
import time


def show_success(message: str, duration: int = 3):
    """
    Show success message with auto-dismiss.
    
    Args:
        message: Success message to display
        duration: Duration in seconds (default: 3)
    """
    success_placeholder = st.empty()
    success_placeholder.success(f"✅ {message}")
    time.sleep(duration)
    success_placeholder.empty()


def show_error(message: str, duration: Optional[int] = None):
    """
    Show error message.
    
    Args:
        message: Error message to display
        duration: Duration in seconds (None = permanent)
    """
    if duration:
        error_placeholder = st.empty()
        error_placeholder.error(f"❌ {message}")
        time.sleep(duration)
        error_placeholder.empty()
    else:
        st.error(f"❌ {message}")


def show_warning(message: str, duration: Optional[int] = None):
    """
    Show warning message.
    
    Args:
        message: Warning message to display
        duration: Duration in seconds (None = permanent)
    """
    if duration:
        warning_placeholder = st.empty()
        warning_placeholder.warning(f"⚠️ {message}")
        time.sleep(duration)
        warning_placeholder.empty()
    else:
        st.warning(f"⚠️ {message}")


def show_info(message: str, duration: Optional[int] = None):
    """
    Show info message.
    
    Args:
        message: Info message to display
        duration: Duration in seconds (None = permanent)
    """
    if duration:
        info_placeholder = st.empty()
        info_placeholder.info(f"ℹ️ {message}")
        time.sleep(duration)
        info_placeholder.empty()
    else:
        st.info(f"ℹ️ {message}")


def confirm_dialog(
    message: str,
    confirm_text: str = "Evet",
    cancel_text: str = "Hayır",
    key: str = "confirm"
) -> bool:
    """
    Show confirmation dialog.
    
    Args:
        message: Confirmation message
        confirm_text: Text for confirm button
        cancel_text: Text for cancel button
        key: Unique key for the dialog
    
    Returns:
        True if confirmed, False otherwise
    """
    if f"{key}_show" not in st.session_state:
        st.session_state[f"{key}_show"] = False
    
    if f"{key}_confirmed" not in st.session_state:
        st.session_state[f"{key}_confirmed"] = False
    
    if st.session_state[f"{key}_show"]:
        st.warning(message)
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button(confirm_text, key=f"{key}_yes", type="primary"):
                st.session_state[f"{key}_confirmed"] = True
                st.session_state[f"{key}_show"] = False
                return True
        
        with col2:
            if st.button(cancel_text, key=f"{key}_no"):
                st.session_state[f"{key}_show"] = False
                st.session_state[f"{key}_confirmed"] = False
                return False
    
    return False


def loading_spinner(message: str = "Yükleniyor..."):
    """
    Context manager for loading spinner.
    
    Usage:
        with loading_spinner("Veriler yükleniyor..."):
            # Your code here
            pass
    """
    return st.spinner(message)


def progress_bar(current: int, total: int, message: str = ""):
    """
    Show progress bar.
    
    Args:
        current: Current progress value
        total: Total value
        message: Optional message to display
    """
    progress = current / total if total > 0 else 0
    st.progress(progress, text=message)


def empty_state(
    icon: str = "📭",
    title: str = "Henüz veri yok",
    description: str = "Başlamak için yukarıdaki butonu kullanın.",
    action_text: Optional[str] = None,
    action_callback: Optional[Callable] = None
):
    """
    Show empty state UI.
    
    Args:
        icon: Emoji icon
        title: Empty state title
        description: Empty state description
        action_text: Optional action button text
        action_callback: Optional action button callback
    """
    st.markdown(f"""
    <div style='
        text-align: center;
        padding: 3rem 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin: 2rem 0;
    '>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>{icon}</div>
        <h3 style='color: #666; margin-bottom: 0.5rem;'>{title}</h3>
        <p style='color: #999;'>{description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if action_text and action_callback:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button(action_text, use_container_width=True):
                action_callback()


def info_card(title: str, value: str, icon: str = "📊", color: str = "#FF5733"):
    """
    Display an info card.
    
    Args:
        title: Card title
        value: Card value
        icon: Emoji icon
        color: Card color
    """
    st.markdown(f"""
    <div style='
        padding: 1.5rem;
        background: linear-gradient(135deg, {color}22 0%, {color}11 100%);
        border-left: 4px solid {color};
        border-radius: 8px;
        margin-bottom: 1rem;
    '>
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <div style='font-size: 2rem;'>{icon}</div>
            <div>
                <div style='font-size: 0.9rem; color: #666; text-transform: uppercase;'>{title}</div>
                <div style='font-size: 1.8rem; font-weight: bold; color: {color};'>{value}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, subtitle: Optional[str] = None, icon: Optional[str] = None):
    """
    Display a section header.
    
    Args:
        title: Section title
        subtitle: Optional subtitle
        icon: Optional emoji icon
    """
    icon_html = f"<span style='margin-right: 0.5rem;'>{icon}</span>" if icon else ""
    subtitle_html = f"<p style='color: #666; margin-top: 0.5rem;'>{subtitle}</p>" if subtitle else ""
    
    st.markdown(f"""
    <div style='margin: 2rem 0 1rem 0;'>
        <h2 style='margin: 0;'>{icon_html}{title}</h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def badge(text: str, color: str = "#FF5733", background: str = None):
    """
    Display a badge.
    
    Args:
        text: Badge text
        color: Text color
        background: Background color (auto-generated if None)
    """
    if background is None:
        background = f"{color}22"
    
    st.markdown(f"""
    <span style='
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background-color: {background};
        color: {color};
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.25rem;
    '>{text}</span>
    """, unsafe_allow_html=True)


def divider(text: Optional[str] = None):
    """
    Display a divider with optional text.
    
    Args:
        text: Optional text to display in the middle
    """
    if text:
        st.markdown(f"""
        <div style='
            display: flex;
            align-items: center;
            margin: 2rem 0;
            color: #999;
        '>
            <div style='flex: 1; height: 1px; background-color: #ddd;'></div>
            <div style='padding: 0 1rem; font-size: 0.9rem;'>{text}</div>
            <div style='flex: 1; height: 1px; background-color: #ddd;'></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #ddd;'>", 
                   unsafe_allow_html=True)


def password_strength_indicator(password: str) -> tuple[str, str, int]:
    """
    Calculate password strength.
    
    Args:
        password: Password to check
    
    Returns:
        Tuple of (strength_text, color, score)
    """
    score = 0
    
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    
    if score <= 2:
        return "Zayıf", "#F44336", score
    elif score <= 4:
        return "Orta", "#FFC107", score
    else:
        return "Güçlü", "#4CAF50", score


def show_password_strength(password: str):
    """
    Display password strength indicator.
    
    Args:
        password: Password to check
    """
    if password:
        strength, color, score = password_strength_indicator(password)
        progress = score / 6
        
        st.markdown(f"""
        <div style='margin: 0.5rem 0;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 0.25rem;'>
                <span style='font-size: 0.85rem; color: #666;'>Şifre Gücü:</span>
                <span style='font-size: 0.85rem; color: {color}; font-weight: bold;'>{strength}</span>
            </div>
            <div style='
                width: 100%;
                height: 4px;
                background-color: #e0e0e0;
                border-radius: 2px;
                overflow: hidden;
            '>
                <div style='
                    width: {progress * 100}%;
                    height: 100%;
                    background-color: {color};
                    transition: width 0.3s ease;
                '></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
