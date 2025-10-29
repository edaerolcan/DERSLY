"""
Reminders page for DERSLY Streamlit application.
Displays upcoming assignment reminders with urgency indicators.
"""
import streamlit as st
from datetime import datetime
from utils.storage_manager import StorageManager
from utils.reminder_manager import ReminderManager
from utils.ui_styles import apply_modern_style

# Page configuration
st.set_page_config(
    page_title="Hatırlatıcılar - DERSLY",
    page_icon="🔔",
    layout="wide"
)

# Apply modern styling
from utils.ui_styles import show_logo_in_sidebar
apply_modern_style()
show_logo_in_sidebar()

# Initialize storage
StorageManager.initialize_storage()

# Page header
st.markdown("""
<div class="page-header">
    <h1>🔔 Hatırlatıcılar</h1>
    <p>Yaklaşan görevleriniz ve önemli tarihler</p>
</div>
""", unsafe_allow_html=True)

# Get reminder statistics
reminder_counts = ReminderManager.get_reminder_count()

# Statistics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stats-card stats-card-danger">
        <div class="stats-icon">🔴</div>
        <div class="stats-number">{reminder_counts['urgent']}</div>
        <div class="stats-label">Acil</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stats-card stats-card-warning">
        <div class="stats-icon">🟡</div>
        <div class="stats-number">{reminder_counts['soon']}</div>
        <div class="stats-label">Yakında</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stats-card stats-card-success">
        <div class="stats-icon">🟢</div>
        <div class="stats-number">{reminder_counts['later']}</div>
        <div class="stats-label">Sonra</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stats-card stats-card-primary">
        <div class="stats-icon">📋</div>
        <div class="stats-number">{reminder_counts['total']}</div>
        <div class="stats-label">Toplam</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Filter options
st.subheader("🔍 Filtrele")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📅 Bugün", use_container_width=True, type="primary" if st.session_state.get('reminder_filter') == 'today' else "secondary"):
        st.session_state['reminder_filter'] = 'today'
        st.rerun()

with col2:
    if st.button("🌅 Yarın", use_container_width=True, type="primary" if st.session_state.get('reminder_filter') == 'tomorrow' else "secondary"):
        st.session_state['reminder_filter'] = 'tomorrow'
        st.rerun()

with col3:
    if st.button("📆 Bu Hafta", use_container_width=True, type="primary" if st.session_state.get('reminder_filter') == 'this_week' else "secondary"):
        st.session_state['reminder_filter'] = 'this_week'
        st.rerun()

with col4:
    if st.button("📋 Tümü", use_container_width=True, type="primary" if st.session_state.get('reminder_filter') == 'all' else "secondary"):
        st.session_state['reminder_filter'] = 'all'
        st.rerun()

# Get current filter
current_filter = st.session_state.get('reminder_filter', 'this_week')

# Get reminders based on filter
reminders = ReminderManager.get_reminders_by_period(current_filter)

st.markdown("---")

# Display reminders
if reminders:
    # Group by urgency
    urgent_reminders = [r for r in reminders if r['urgency_score'] >= 4]
    soon_reminders = [r for r in reminders if 2 <= r['urgency_score'] < 4]
    later_reminders = [r for r in reminders if r['urgency_score'] < 2]
    
    # Display urgent reminders
    if urgent_reminders:
        st.markdown("### 🔴 Acil Hatırlatıcılar")
        for reminder in urgent_reminders:
            display_reminder_card(reminder, urgent=True)
        st.markdown("---")
    
    # Display soon reminders
    if soon_reminders:
        st.markdown("### 🟡 Yaklaşan Hatırlatıcılar")
        for reminder in soon_reminders:
            display_reminder_card(reminder)
        st.markdown("---")
    
    # Display later reminders
    if later_reminders:
        st.markdown("### 🟢 Diğer Hatırlatıcılar")
        for reminder in later_reminders:
            display_reminder_card(reminder)
else:
    # Empty state
    filter_labels = {
        'today': 'Bugün',
        'tomorrow': 'Yarın',
        'this_week': 'Bu Hafta',
        'all': 'Tüm Hatırlatıcılar'
    }
    filter_label = filter_labels.get(current_filter, 'Bu Hafta')
    
    st.info(f"""
    🎉 **{filter_label} için hatırlatıcı yok!**
    
    Farklı bir zaman dilimi seçerek diğer hatırlatıcıları görebilirsiniz.
    """)
    
    # Quick links
    st.markdown("---")
    st.subheader("⚡ Hızlı Erişim")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Ödevlere Git", use_container_width=True):
            st.switch_page("pages/3_📝_Ödevler.py")
    
    with col2:
        if st.button("📅 Takvime Git", use_container_width=True):
            st.switch_page("pages/4_📅_Takvim.py")
    
    with col3:
        if st.button("🏠 Ana Sayfaya Git", use_container_width=True):
            st.switch_page("pages/1_🏠_Ana_Sayfa.py")


def display_reminder_card(reminder: dict, urgent: bool = False):
    """Display a reminder card with all details."""
    # Card styling based on urgency
    if urgent:
        card_style = "background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%); border-left: 4px solid #fc8181; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(252, 129, 129, 0.2);"
    else:
        card_style = "background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%); border-left: 4px solid #cbd5e0; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);"
    
    with st.container():
        st.markdown(f'<div style="{card_style}">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([4, 2, 1])
        
        with col1:
            # Title with type emoji
            type_emoji = {
                'assignment': '📝',
                'exam': '📄',
                'project': '💼',
                'quiz': '❓'
            }.get(reminder.get('type', 'assignment'), '📝')
            
            st.markdown(f"**{type_emoji} {reminder.get('title', 'Başlıksız')}**")
            
            # Description
            if reminder.get('description'):
                desc = reminder['description']
                if len(desc) > 150:
                    st.caption(desc[:150] + "...")
                else:
                    st.caption(desc)
        
        with col2:
            # Urgency badge
            urgency_color = reminder['urgency_color']
            urgency_label = reminder['urgency_label']
            st.markdown(f"""
            <div style="background-color: {urgency_color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; text-align: center; font-weight: 600; margin-bottom: 0.5rem;">
                {urgency_label}
            </div>
            """, unsafe_allow_html=True)
            
            # Due date
            try:
                due_date = reminder['due_date_obj']
                st.caption(f"📅 {due_date.strftime('%d.%m.%Y %H:%M')}")
            except:
                st.caption("📅 Tarih belirtilmemiş")
            
            # Priority
            priority_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(reminder.get('priority', 'medium'), '🟡')
            priority_label = {
                'high': 'Yüksek',
                'medium': 'Orta',
                'low': 'Düşük'
            }.get(reminder.get('priority', 'medium'), 'Orta')
            st.caption(f"**Öncelik:** {priority_emoji} {priority_label}")
        
        with col3:
            # Action button
            if st.button("👁️", key=f"view_{reminder['id']}", help="Detayları Gör"):
                st.switch_page("pages/3_📝_Ödevler.py")
        
        st.markdown('</div>', unsafe_allow_html=True)

