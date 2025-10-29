"""
Modern UI styles for DERSLY application.
Enhanced with glassmorphism, better animations, and improved UX.
"""

def get_modern_css(theme="light") -> str:
    """
    Returns enhanced modern CSS styling for the entire application.
    Uses soft, eye-friendly colors with glassmorphism effects.
    
    Args:
        theme: "light" or "dark"
    """
    
    # Soft color palette
    if theme == "light":
        bg_gradient = "linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%)"
        card_bg = "rgba(255, 255, 255, 0.95)"
        card_border = "rgba(155, 135, 245, 0.1)"
        text_primary = "#2d3748"
        text_secondary = "#718096"
        primary_color = "#9b87f5"
        primary_gradient = "linear-gradient(135deg, #9b87f5 0%, #b794f6 100%)"
        success_color = "#68d391"
        warning_color = "#f6ad55"
        danger_color = "#fc8181"
        info_color = "#63b3ed"
        sidebar_gradient = "linear-gradient(180deg, #9b87f5 0%, #b794f6 100%)"
        shadow_color = "rgba(0, 0, 0, 0.08)"
    else:
        bg_gradient = "linear-gradient(135deg, #1a202c 0%, #2d3748 100%)"
        card_bg = "rgba(45, 55, 72, 0.95)"
        card_border = "rgba(183, 148, 246, 0.2)"
        text_primary = "#e2e8f0"
        text_secondary = "#a0aec0"
        primary_color = "#b794f6"
        primary_gradient = "linear-gradient(135deg, #b794f6 0%, #d6bcfa 100%)"
        success_color = "#68d391"
        warning_color = "#f6ad55"
        danger_color = "#fc8181"
        info_color = "#63b3ed"
        sidebar_gradient = "linear-gradient(180deg, #6b46c1 0%, #805ad5 100%)"
        shadow_color = "rgba(0, 0, 0, 0.3)"
    
    return f"""
    <style>
        /* ============================================
           GLOBAL STYLES WITH GLASSMORPHISM
           ============================================ */
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        
        .main {{
            background: {bg_gradient};
            background-attachment: fixed;
        }}
        
        /* Sidebar with glassmorphism */
        [data-testid="stSidebar"] {{
            background: {sidebar_gradient};
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }}
        
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        /* Logo styling with animation */
        .sidebar-logo {{
            text-align: center;
            padding: 1.5rem 1rem;
            margin-bottom: 1.5rem;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            backdrop-filter: blur(10px);
            animation: fadeInDown 0.6s ease-out;
        }}
        
        .sidebar-logo img {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            margin-bottom: 0.75rem;
            transition: transform 0.3s ease;
        }}
        
        .sidebar-logo img:hover {{
            transform: scale(1.05) rotate(5deg);
        }}
        
        .sidebar-logo h2 {{
            margin: 0;
            font-size: 1.5rem;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        /* ============================================
           GLASSMORPHISM CARDS
           ============================================ */
        
        .custom-card {{
            background: {card_bg};
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid {card_border};
            border-radius: 20px;
            padding: 1.75rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 4px 12px {shadow_color};
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .custom-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: {primary_gradient};
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .custom-card:hover {{
            box-shadow: 0 12px 28px {shadow_color};
            transform: translateY(-4px);
        }}
        
        .custom-card:hover::before {{
            transform: scaleX(1);
        }}
        
        /* Urgent card with pulse animation */
        .urgent-card {{
            background: linear-gradient(135deg, rgba(252, 129, 129, 0.1) 0%, rgba(254, 215, 215, 0.1) 100%);
            border-left: 4px solid {danger_color};
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ box-shadow: 0 4px 12px {shadow_color}; }}
            50% {{ box-shadow: 0 4px 20px rgba(252, 129, 129, 0.3); }}
        }}
        
        .info-card {{
            background: linear-gradient(135deg, rgba(99, 179, 237, 0.1) 0%, rgba(190, 227, 248, 0.1) 100%);
            border-left: 4px solid {info_color};
            padding: 1.5rem;
            border-radius: 16px;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
        }}
        
        .success-card {{
            background: linear-gradient(135deg, rgba(104, 211, 145, 0.1) 0%, rgba(198, 246, 213, 0.1) 100%);
            border-left: 4px solid {success_color};
        }}
        
        .warning-card {{
            background: linear-gradient(135deg, rgba(246, 173, 85, 0.1) 0%, rgba(254, 235, 200, 0.1) 100%);
            border-left: 4px solid {warning_color};
        }}
        
        /* ============================================
           ENHANCED BADGES
           ============================================ */
        
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.5rem 1rem;
            border-radius: 24px;
            font-size: 0.875rem;
            font-weight: 600;
            margin: 0.25rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
        }}
        
        .badge:hover {{
            transform: translateY(-2px) scale(1.05);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
        }}
        
        .badge-overdue {{
            background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
            color: white;
            animation: shake 0.5s ease-in-out;
        }}
        
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            75% {{ transform: translateX(5px); }}
        }}
        
        .badge-today {{
            background: linear-gradient(135deg, {danger_color} 0%, #f56565 100%);
            color: white;
            animation: blink 1.5s infinite;
        }}
        
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}
        
        .badge-tomorrow {{
            background: linear-gradient(135deg, {warning_color} 0%, #ed8936 100%);
            color: white;
        }}
        
        .badge-week {{
            background: linear-gradient(135deg, #fbd38d 0%, #f6ad55 100%);
            color: #744210;
        }}
        
        .badge-later {{
            background: linear-gradient(135deg, {success_color} 0%, #48bb78 100%);
            color: white;
        }}
        
        .badge-completed {{
            background: linear-gradient(135deg, #81e6d9 0%, #4fd1c5 100%);
            color: white;
        }}
        
        /* ============================================
           MODERN HEADERS
           ============================================ */
        
        .page-header {{
            background: {primary_gradient};
            color: white;
            padding: 2.5rem 2.5rem;
            border-radius: 24px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 24px rgba(155, 135, 245, 0.25);
            position: relative;
            overflow: hidden;
            animation: fadeInDown 0.6s ease-out;
        }}
        
        .page-header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }}
        
        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        .page-header h1 {{
            margin: 0;
            font-size: 2.75rem;
            font-weight: 700;
            position: relative;
            z-index: 1;
        }}
        
        .page-header p {{
            margin: 0.75rem 0 0 0;
            opacity: 0.95;
            font-size: 1.15rem;
            position: relative;
            z-index: 1;
        }}
        
        .section-header {{
            background: {primary_gradient};
            color: white;
            padding: 1.25rem 1.75rem;
            border-radius: 16px;
            margin-bottom: 1.75rem;
            box-shadow: 0 4px 12px rgba(155, 135, 245, 0.2);
            animation: slideInLeft 0.5s ease-out;
        }}
        
        .section-header h2 {{
            margin: 0;
            font-size: 1.5rem;
            font-weight: 600;
        }}
        
        /* ============================================
           ENHANCED STATS CARDS
           ============================================ */
        
        .stats-card {{
            background: {card_bg};
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 1.75rem;
            text-align: center;
            box-shadow: 0 4px 12px {shadow_color};
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border-top: 4px solid transparent;
            position: relative;
            overflow: hidden;
        }}
        
        .stats-card::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: {primary_gradient};
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 0;
        }}
        
        .stats-card:hover {{
            box-shadow: 0 12px 32px {shadow_color};
            transform: translateY(-8px) scale(1.02);
        }}
        
        .stats-card:hover::after {{
            opacity: 0.05;
        }}
        
        .stats-card > * {{
            position: relative;
            z-index: 1;
        }}
        
        .stats-card-primary {{ border-top-color: {primary_color}; }}
        .stats-card-success {{ border-top-color: {success_color}; }}
        .stats-card-warning {{ border-top-color: {warning_color}; }}
        .stats-card-danger {{ border-top-color: {danger_color}; }}
        
        .stats-number {{
            font-size: 3rem;
            font-weight: 700;
            background: {primary_gradient};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            animation: countUp 0.8s ease-out;
        }}
        
        @keyframes countUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .stats-label {{
            color: {text_secondary};
            font-size: 0.95rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stats-icon {{
            font-size: 2.5rem;
            margin-bottom: 0.75rem;
            animation: bounce 2s infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        /* ============================================
           ENHANCED BUTTONS
           ============================================ */
        
        .stButton > button {{
            border-radius: 12px;
            font-weight: 600;
            padding: 0.75rem 1.75rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .stButton > button::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        
        .stButton > button:hover::before {{
            width: 300px;
            height: 300px;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }}
        
        .stButton > button:active {{
            transform: translateY(-1px);
        }}
        
        .stButton > button[kind="primary"] {{
            background: {primary_gradient};
        }}
        
        /* ============================================
           ENHANCED FORMS
           ============================================ */
        
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input,
        .stTimeInput > div > div > input {{
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            padding: 0.875rem;
            transition: all 0.3s ease;
            background: {card_bg};
            backdrop-filter: blur(10px);
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {{
            border-color: {primary_color};
            box-shadow: 0 0 0 4px rgba(155, 135, 245, 0.1);
            transform: translateY(-2px);
        }}
        
        /* ============================================
           MODERN TABS
           ============================================ */
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 16px;
            background: {card_bg};
            padding: 0.75rem;
            border-radius: 16px;
            box-shadow: 0 2px 8px {shadow_color};
            backdrop-filter: blur(10px);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 12px;
            padding: 0.875rem 1.75rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            background-color: rgba(155, 135, 245, 0.1);
            transform: translateY(-2px);
        }}
        
        .stTabs [aria-selected="true"] {{
            background: {primary_gradient};
            color: white !important;
            box-shadow: 0 4px 12px rgba(155, 135, 245, 0.3);
        }}
        
        /* ============================================
           ANIMATIONS
           ============================================ */
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes slideInLeft {{
            from {{ opacity: 0; transform: translateX(-30px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        @keyframes slideInRight {{
            from {{ opacity: 0; transform: translateX(30px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        .fade-in {{ animation: fadeIn 0.6s ease-out; }}
        .slide-in-left {{ animation: slideInLeft 0.6s ease-out; }}
        .slide-in-right {{ animation: slideInRight 0.6s ease-out; }}
        
        /* ============================================
           SCROLLBAR
           ============================================ */
        
        ::-webkit-scrollbar {{
            width: 12px;
            height: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.05);
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {primary_gradient};
            border-radius: 10px;
            border: 2px solid transparent;
            background-clip: padding-box;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, #b794f6 0%, #9b87f5 100%);
            background-clip: padding-box;
        }}
        
        /* ============================================
           RESPONSIVE DESIGN
           ============================================ */
        
        @media (max-width: 768px) {{
            .page-header h1 {{ font-size: 2rem; }}
            .stats-number {{ font-size: 2.25rem; }}
            .custom-card {{ padding: 1.25rem; }}
            .sidebar-logo img {{ width: 60px; height: 60px; }}
        }}
    </style>
    """


def apply_modern_style(theme="light"):
    """Apply enhanced modern CSS styling to the current page."""
    import streamlit as st
    st.markdown(get_modern_css(theme), unsafe_allow_html=True)


def show_logo_in_sidebar():
    """Display animated logo in sidebar."""
    import streamlit as st
    import os
    import base64
    
    logo_path = "logo-512x512.webp"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
        
        with st.sidebar:
            st.markdown(f"""
            <div class="sidebar-logo">
                <img src="data:image/webp;base64,{logo_base64}" alt="DERSLY Logo">
                <h2>DERSLY</h2>
            </div>
            """, unsafe_allow_html=True)
