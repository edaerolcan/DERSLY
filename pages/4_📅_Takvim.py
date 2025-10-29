"""
Calendar page for DERSLY Streamlit application.
Displays assignments in calendar view.
"""
import streamlit as st
from datetime import datetime, timedelta
from utils.storage_manager import StorageManager
from utils.user_manager import UserManager
from utils.assignment_manager import AssignmentManager
from utils.ui_styles import apply_modern_style
import calendar

# Page configuration
st.set_page_config(
    page_title="Takvim - DERSLY",
    page_icon="📅",
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
    <h1>📅 Takvim</h1>
    <p>Görevlerinizi takvim görünümünde inceleyin</p>
</div>
""", unsafe_allow_html=True)

# Month/Year selector
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    selected_month = st.selectbox(
        "Ay",
        options=list(range(1, 13)),
        index=datetime.now().month - 1,
        format_func=lambda x: calendar.month_name[x]
    )

with col2:
    selected_year = st.number_input(
        "Yıl",
        min_value=2020,
        max_value=2030,
        value=datetime.now().year,
        step=1
    )

with col3:
    if st.button("📅 Bugün", use_container_width=True):
        selected_month = datetime.now().month
        selected_year = datetime.now().year
        st.rerun()

st.markdown("---")

# Get assignments for the month
assignments = AssignmentManager.get_all_assignments()

# Filter assignments for selected month
month_assignments = {}
for assignment in assignments:
    try:
        due_date_str = assignment.get('due_date', '')
        if 'T' in due_date_str:
            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
        else:
            due_date = datetime.fromisoformat(due_date_str)
        
        if due_date.month == selected_month and due_date.year == selected_year:
            day = due_date.day
            if day not in month_assignments:
                month_assignments[day] = []
            month_assignments[day].append(assignment)
    except:
        continue

# Display calendar
st.subheader(f"{calendar.month_name[selected_month]} {selected_year}")

# Mobile-friendly calendar CSS
st.markdown("""
<style>
    /* Calendar mobile optimization */
    @media (max-width: 768px) {
        .row-widget.stHorizontalBlock {
            gap: 2px !important;
        }
        .row-widget.stHorizontalBlock > div {
            padding: 2px !important;
            min-width: 40px !important;
        }
        .element-container {
            font-size: 0.75rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Get calendar for the month
cal = calendar.monthcalendar(selected_year, selected_month)

# Day names
day_names = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
cols = st.columns(7)
for i, day_name in enumerate(day_names):
    with cols[i]:
        st.markdown(f"**{day_name}**")

# Display weeks
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        with cols[i]:
            if day == 0:
                st.markdown("")
            else:
                # Check if today
                today = datetime.now()
                is_today = (day == today.day and 
                           selected_month == today.month and 
                           selected_year == today.year)
                
                # Check if has assignments
                has_assignments = day in month_assignments
                
                # Display day
                if is_today:
                    st.markdown(f"**🔵 {day}**")
                elif has_assignments:
                    st.markdown(f"**🔴 {day}**")
                else:
                    st.markdown(f"{day}")
                
                # Show assignments for this day
                if has_assignments:
                    for assignment in month_assignments[day]:
                        status_emoji = '✅' if assignment.get('status') == 'completed' else '⏳'
                        type_emoji = {
                            'assignment': '📝',
                            'exam': '📄',
                            'project': '💼',
                            'quiz': '❓'
                        }.get(assignment.get('type', 'assignment'), '📝')
                        
                        st.caption(f"{status_emoji}{type_emoji} {assignment.get('title', '')[:15]}")

st.markdown("---")

# Legend
st.markdown("### 📖 Açıklama")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🔵 **Bugün**")
with col2:
    st.markdown("🔴 **Görev Var**")
with col3:
    st.markdown("⏳ **Bekleyen** | ✅ **Tamamlanan**")

# Upcoming assignments
st.markdown("---")
st.subheader("📋 Bu Ayki Görevler")

if month_assignments:
    # Sort by day
    sorted_days = sorted(month_assignments.keys())
    
    for day in sorted_days:
        st.markdown(f"**{day} {calendar.month_name[selected_month]}**")
        for assignment in month_assignments[day]:
            status_emoji = '✅' if assignment.get('status') == 'completed' else '⏳'
            type_emoji = {
                'assignment': '📝',
                'exam': '📄',
                'project': '💼',
                'quiz': '❓'
            }.get(assignment.get('type', 'assignment'), '📝')
            
            st.write(f"{status_emoji} {type_emoji} **{assignment.get('title', 'Başlıksız')}**")
            if assignment.get('description'):
                st.caption(assignment['description'][:100])
        st.markdown("---")
else:
    st.info("📅 Bu ay için görev bulunmuyor.")
