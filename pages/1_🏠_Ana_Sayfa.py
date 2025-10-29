"""
Home page for DERSLY Streamlit application.
Displays dashboard with statistics and upcoming assignments.
"""
import streamlit as st
from datetime import datetime, timedelta
from utils.storage_manager import StorageManager
from utils.user_manager import UserManager
from utils.course_manager import CourseManager
from utils.assignment_manager import AssignmentManager
from utils.grade_manager import GradeManager
from utils.ui_styles import apply_modern_style

# Page configuration
st.set_page_config(
    page_title="Ana Sayfa - DERSLY",
    page_icon="🏠",
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
    <h1>🏠 Ana Sayfa</h1>
    <p>Günlük özet ve yaklaşan görevleriniz</p>
</div>
""", unsafe_allow_html=True)

# Get dashboard data with caching
@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_dashboard_data():
    """Get dashboard statistics with caching for better performance."""
    courses = CourseManager.get_all_courses()
    assignments = AssignmentManager.get_all_assignments()
    pending_assignments = AssignmentManager.get_assignments_by_status('pending')
    upcoming_assignments = AssignmentManager.get_upcoming_assignments(7)
    gpa = GradeManager.calculate_gpa()
    
    return {
        'total_courses': len(courses),
        'total_assignments': len(assignments),
        'pending_assignments': len(pending_assignments),
        'gpa': gpa,
        'upcoming_assignments': upcoming_assignments[:5]  # Top 5
    }

try:
    data = get_dashboard_data()
    
    # Statistics row
    st.markdown("""
    <div class="section-header">
        <h2>📊 Genel Bakış</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stats-card stats-card-primary">
            <div class="stats-icon">📚</div>
            <div class="stats-number">{}</div>
            <div class="stats-label">Toplam Ders</div>
        </div>
        """.format(data['total_courses']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card stats-card-warning">
            <div class="stats-icon">📝</div>
            <div class="stats-number">{}</div>
            <div class="stats-label">Bekleyen Görev</div>
        </div>
        """.format(data['pending_assignments']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card stats-card-success">
            <div class="stats-icon">📋</div>
            <div class="stats-number">{}</div>
            <div class="stats-label">Toplam Görev</div>
        </div>
        """.format(data['total_assignments']), unsafe_allow_html=True)
    
    with col4:
        gpa_value = f"{data['gpa']:.2f}" if data['gpa'] > 0 else "N/A"
        st.markdown("""
        <div class="stats-card stats-card-danger">
            <div class="stats-icon">📊</div>
            <div class="stats-number">{}</div>
            <div class="stats-label">GNO</div>
        </div>
        """.format(gpa_value), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upcoming assignments
    st.subheader("📅 Yaklaşan Görevler (7 Gün)")
    
    if data['upcoming_assignments']:
        for assignment in data['upcoming_assignments']:
            # Create assignment card
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    # Assignment title and type
                    type_emoji = {
                        'assignment': '📝',
                        'exam': '📄',
                        'project': '💼',
                        'quiz': '❓'
                    }.get(assignment.get('type', 'assignment'), '📝')
                    
                    st.markdown(f"**{type_emoji} {assignment.get('title', 'Başlıksız')}**")
                    if assignment.get('description'):
                        st.caption(assignment['description'][:100] + "..." if len(assignment['description']) > 100 else assignment['description'])
                
                with col2:
                    # Due date
                    try:
                        due_date_str = assignment.get('due_date', '')
                        if 'T' in due_date_str:
                            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                        else:
                            due_date = datetime.fromisoformat(due_date_str)
                        
                        # Calculate days remaining
                        days_remaining = (due_date - datetime.now()).days
                        
                        if days_remaining < 0:
                            st.error(f"⏰ {abs(days_remaining)} gün gecikti")
                        elif days_remaining == 0:
                            st.warning("⏰ Bugün bitiyor!")
                        elif days_remaining == 1:
                            st.warning("⏰ Yarın bitiyor")
                        else:
                            st.info(f"⏰ {days_remaining} gün kaldı")
                        
                        st.caption(due_date.strftime("%d.%m.%Y %H:%M"))
                    except:
                        st.caption("Tarih belirtilmemiş")
                
                with col3:
                    # Priority badge
                    priority = assignment.get('priority', 'medium')
                    priority_colors = {
                        'high': '🔴',
                        'medium': '🟡',
                        'low': '🟢'
                    }
                    st.markdown(f"{priority_colors.get(priority, '🟡')} {priority.upper()}")
                
                st.markdown("---")
    else:
        st.info("🎉 Yaklaşan göreviniz yok!")
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("⚡ Hızlı İşlemler")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Yeni Ders Ekle", use_container_width=True):
            st.switch_page("pages/2_📚_Dersler.py")
    
    with col2:
        if st.button("➕ Yeni Ödev Ekle", use_container_width=True):
            st.switch_page("pages/3_📝_Ödevler.py")
    
    with col3:
        if st.button("📅 Takvim Görünümü", use_container_width=True):
            st.switch_page("pages/4_📅_Takvim.py")
    
    with col4:
        if st.button("📊 Not Gir", use_container_width=True):
            st.switch_page("pages/6_📊_Not_Ortalaması.py")

except Exception as e:
    st.error(f"❌ Bir hata oluştu: {str(e)}")
    st.exception(e)
