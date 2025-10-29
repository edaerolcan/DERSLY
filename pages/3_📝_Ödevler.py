"""
Assignments page for DERSLY Streamlit application.
Manages assignments, exams, projects, and quizzes.
Enhanced with deadline warnings and modern UI design.
"""
import streamlit as st
from datetime import datetime, date, time, timedelta
from utils.storage_manager import StorageManager
from utils.user_manager import UserManager
from utils.assignment_manager import AssignmentManager
from utils.course_manager import CourseManager
from utils.input_validator import InputValidator
from utils.calendar_export import CalendarExport
from utils.ui_styles import apply_modern_style

# Page configuration
st.set_page_config(
    page_title="Ödevler - DERSLY",
    page_icon="📝",
    layout="wide"
)

# Apply modern styling
from utils.ui_styles import show_logo_in_sidebar
apply_modern_style()
show_logo_in_sidebar()

# Initialize storage
StorageManager.initialize_storage()


def get_deadline_badge(due_date: datetime, status: str) -> tuple:
    """
    Get deadline badge color and text based on due date.
    
    Returns:
        tuple: (badge_color, badge_text, urgency_level)
    """
    if status == 'completed':
        return "🟢", "Tamamlandı", 0
    
    now = datetime.now()
    time_diff = due_date - now
    
    # Overdue
    if time_diff.total_seconds() < 0:
        days_overdue = abs(time_diff.days)
        return "⚫", f"{days_overdue} gün gecikti", 5
    
    # Due today
    if time_diff.days == 0:
        hours_left = int(time_diff.total_seconds() / 3600)
        if hours_left < 3:
            return "🔴", f"{hours_left} saat kaldı!", 4
        return "🔴", "Bugün bitiyor!", 4
    
    # Due tomorrow
    if time_diff.days == 1:
        return "🟠", "Yarın bitiyor", 3
    
    # Due in 2-3 days
    if time_diff.days <= 3:
        return "🟡", f"{time_diff.days} gün kaldı", 2
    
    # Due in 4-7 days
    if time_diff.days <= 7:
        return "🔵", f"{time_diff.days} gün kaldı", 1
    
    # More than a week
    return "⚪", f"{time_diff.days} gün kaldı", 0


def get_priority_badge(priority: str) -> str:
    """Get priority badge emoji."""
    priority_map = {
        'high': '🔴 Yüksek',
        'medium': '🟡 Orta',
        'low': '🟢 Düşük'
    }
    return priority_map.get(priority, '🟡 Orta')


def get_type_emoji(assignment_type: str) -> str:
    """Get type emoji."""
    type_map = {
        'assignment': '�',
        'exam': '📄',
        'project': '💼',
        'quiz': '❓'
    }
    return type_map.get(assignment_type, '📝')


# Page header with modern styling
st.markdown("""
<div class="page-header">
    <h1>📝 Ödevler & Sınavlar</h1>
    <p>Ödev, sınav, proje ve quizlerinizi modern arayüzle yönetin</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 Görev Listesi", "➕ Yeni Görev Ekle", "📊 Analiz"])

with tab1:
    st.subheader("Görevleriniz")
    
    # Filter and sort options
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox(
            "Durum Filtresi",
            options=["all", "pending", "completed"],
            format_func=lambda x: {"all": "Tümü", "pending": "Bekleyen", "completed": "Tamamlanan"}[x]
        )
    
    with col2:
        type_filter = st.selectbox(
            "Tür Filtresi",
            options=["all", "assignment", "exam", "project", "quiz"],
            format_func=lambda x: {
                "all": "Tümü",
                "assignment": "Ödev",
                "exam": "Sınav",
                "project": "Proje",
                "quiz": "Quiz"
            }[x]
        )
    
    with col3:
        sort_option = st.selectbox(
            "Sıralama",
            options=["deadline", "priority", "created", "alphabetical"],
            format_func=lambda x: {
                "deadline": "⏰ Deadline",
                "priority": "🔴 Öncelik",
                "created": "📅 Oluşturulma",
                "alphabetical": "🔤 Alfabetik"
            }[x]
        )
    
    # Get assignments
    if status_filter == "all":
        assignments = AssignmentManager.get_all_assignments()
    else:
        assignments = AssignmentManager.get_assignments_by_status(status_filter)
    
    # Apply type filter
    if type_filter != "all":
        assignments = [a for a in assignments if a.get('type') == type_filter]
    
    # Sort assignments
    if sort_option == "deadline":
        assignments.sort(key=lambda x: x.get('due_date', ''))
    elif sort_option == "priority":
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        assignments.sort(key=lambda x: priority_order.get(x.get('priority', 'medium'), 1))
    elif sort_option == "created":
        assignments.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    elif sort_option == "alphabetical":
        assignments.sort(key=lambda x: x.get('title', '').lower())
    
    # Show urgent assignments first (if sorting by deadline)
    if sort_option == "deadline" and status_filter != "completed":
        # Separate by urgency
        urgent_assignments = []
        normal_assignments = []
        
        for assignment in assignments:
            try:
                due_date_str = assignment.get('due_date', '')
                if 'T' in due_date_str:
                    due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                else:
                    due_date = datetime.fromisoformat(due_date_str)
                
                _, _, urgency = get_deadline_badge(due_date, assignment.get('status', 'pending'))
                
                if urgency >= 3:  # Urgent (today, tomorrow, overdue)
                    urgent_assignments.append(assignment)
                else:
                    normal_assignments.append(assignment)
            except:
                normal_assignments.append(assignment)
        
        # Show urgent section if exists
        if urgent_assignments:
            st.markdown("### 🚨 Acil Görevler")
            for assignment in urgent_assignments:
                display_assignment_card(assignment, urgent=True)
            st.markdown("---")
        
        # Show normal assignments
        if normal_assignments:
            st.markdown("### 📋 Diğer Görevler")
            assignments = normal_assignments
    
    # Display assignments
    if assignments:
        for assignment in assignments:
            display_assignment_card(assignment)
    else:
        st.info("📝 Görev bulunamadı.")


def display_assignment_card(assignment: dict, urgent: bool = False):
    """Display assignment card with deadline warnings."""
    # Parse due date
    try:
        due_date_str = assignment.get('due_date', '')
        if 'T' in due_date_str:
            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
        else:
            due_date = datetime.fromisoformat(due_date_str)
        
        badge_emoji, badge_text, urgency = get_deadline_badge(due_date, assignment.get('status', 'pending'))
    except:
        due_date = None
        badge_emoji, badge_text, urgency = "⚪", "Tarih yok", 0
    
    # Card styling based on urgency
    if urgent or urgency >= 3:
        card_style = "background-color: #fff3cd; border-left: 4px solid #ff6b6b; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;"
    else:
        card_style = "background-color: #f8f9fa; border-left: 4px solid #dee2e6; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;"
    
    with st.container():
        st.markdown(f'<div style="{card_style}">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            # Title with status
            status_emoji = '✅' if assignment.get('status') == 'completed' else '⏳'
            type_emoji = get_type_emoji(assignment.get('type', 'assignment'))
            st.markdown(f"**{status_emoji} {type_emoji} {assignment.get('title', 'Başlıksız')}**")
            
            # Description
            if assignment.get('description'):
                desc = assignment['description']
                if len(desc) > 100:
                    st.caption(desc[:100] + "...")
                else:
                    st.caption(desc)
        
        with col2:
            # Deadline badge
            st.markdown(f"**{badge_emoji} {badge_text}**")
            
            # Due date
            if due_date:
                st.caption(f"📅 {due_date.strftime('%d.%m.%Y %H:%M')}")
            
            # Priority
            priority_badge = get_priority_badge(assignment.get('priority', 'medium'))
            st.caption(f"**Öncelik:** {priority_badge}")
        
        with col3:
            # Action buttons
            if assignment.get('status') == 'pending':
                if st.button("✅", key=f"complete_{assignment['id']}", help="Tamamla"):
                    if AssignmentManager.update_assignment(assignment['id'], {'status': 'completed'}):
                        st.success("✅ Görev tamamlandı!")
                        st.rerun()
            else:
                if st.button("↩️", key=f"reopen_{assignment['id']}", help="Geri Al"):
                    if AssignmentManager.update_assignment(assignment['id'], {'status': 'pending'}):
                        st.success("✅ Görev yeniden açıldı!")
                        st.rerun()
            
            # Calendar export button
            if st.button("📅", key=f"calendar_{assignment['id']}", help="Takvime Ekle"):
                ics_content = CalendarExport.create_assignment_ics(assignment)
                download_link = CalendarExport.create_download_link(
                    ics_content,
                    f"dersly-{assignment.get('title', 'odev').replace(' ', '-')}"
                )
                st.markdown(download_link, unsafe_allow_html=True)
                st.caption("💡 İndirilen dosyayı açarak takviminize ekleyin")
            
            if st.button("🗑️", key=f"delete_{assignment['id']}", help="Sil"):
                if AssignmentManager.delete_assignment(assignment['id']):
                    st.success("✅ Görev silindi!")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)


with tab2:
    st.subheader("Yeni Görev Ekle")
    
    with st.form("add_assignment_form"):
        title = st.text_input("Başlık *", placeholder="Ödev 1", help="Görev başlığı")
        
        description = st.text_area("Açıklama", placeholder="Görev detayları...", help="Opsiyonel açıklama")
        
        assignment_type = st.selectbox(
            "Tür *",
            options=["assignment", "exam", "project", "quiz"],
            format_func=lambda x: {
                "assignment": "📝 Ödev",
                "exam": "📄 Sınav",
                "project": "💼 Proje",
                "quiz": "❓ Quiz"
            }[x],
            help="Görev türü"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            due_date = st.date_input("Bitiş Tarihi *", value=date.today(), help="Teslim tarihi")
        with col2:
            due_time = st.time_input("Bitiş Saati *", value=time(23, 59), help="Teslim saati")
        
        priority = st.selectbox(
            "Öncelik",
            options=["low", "medium", "high"],
            index=1,
            format_func=lambda x: {"low": "🟢 Düşük", "medium": "🟡 Orta", "high": "🔴 Yüksek"}[x],
            help="Görev önceliği"
        )
        
        # Optional: Link to course
        courses = CourseManager.get_all_courses()
        if courses:
            course_options = [None] + [c['id'] for c in courses]
            course_names = ["Ders seçilmedi"] + [f"{c['course_code']} - {c['course_name']}" for c in courses]
            
            selected_course_idx = st.selectbox(
                "Ders (Opsiyonel)",
                options=range(len(course_options)),
                format_func=lambda x: course_names[x],
                help="Görevi bir derse bağlayın"
            )
            course_id = course_options[selected_course_idx]
        else:
            course_id = None
        
        submitted = st.form_submit_button("➕ Görev Ekle", type="primary", use_container_width=True)
        
        if submitted:
            # Combine date and time
            due_datetime = datetime.combine(due_date, due_time)
            
            # Prepare assignment data for validation
            assignment_data = {
                'title': title,
                'description': description if description else None,
                'type': assignment_type,
                'due_date': due_datetime.isoformat(),
                'priority': priority,
                'status': 'pending',
                'course_id': course_id
            }
            
            # Validate assignment data
            is_valid, error_message, warning_message = InputValidator.validate_assignment(assignment_data)
            
            if not is_valid:
                st.error(error_message)
            else:
                # Show warning if exists (but still allow submission)
                if warning_message:
                    st.warning(warning_message)
                
                assignment_id = AssignmentManager.add_assignment(assignment_data)
                st.success(f"✅ Görev başarıyla eklendi! (ID: {assignment_id})")
                
                # Offer calendar export
                st.info("📅 **Mobil takviminize eklemek ister misiniz?**")
                
                # Get the created assignment
                created_assignment = AssignmentManager.get_assignment(assignment_id)
                if created_assignment:
                    # Create iCalendar content
                    ics_content = CalendarExport.create_assignment_ics(created_assignment)
                    download_link = CalendarExport.create_download_link(
                        ics_content,
                        f"dersly-{title.replace(' ', '-')}"
                    )
                    st.markdown(download_link, unsafe_allow_html=True)
                    st.caption("💡 İndirilen .ics dosyasını açarak görevi takviminize ekleyebilirsiniz")
                
                st.balloons()
                st.rerun()

with tab3:
    st.subheader("📊 Görev Analizi")
    
    # Get all assignments
    all_assignments = AssignmentManager.get_all_assignments()
    pending_assignments = AssignmentManager.get_assignments_by_status('pending')
    completed_assignments = AssignmentManager.get_assignments_by_status('completed')
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Toplam Görev", len(all_assignments))
    
    with col2:
        st.metric("Bekleyen", len(pending_assignments))
    
    with col3:
        st.metric("Tamamlanan", len(completed_assignments))
    
    with col4:
        if len(all_assignments) > 0:
            completion_rate = (len(completed_assignments) / len(all_assignments)) * 100
            st.metric("Tamamlanma", f"{completion_rate:.0f}%")
        else:
            st.metric("Tamamlanma", "0%")
    
    st.markdown("---")
    
    # Urgency breakdown
    st.markdown("### ⏰ Aciliyet Durumu")
    
    overdue = 0
    today = 0
    tomorrow = 0
    this_week = 0
    later = 0
    
    for assignment in pending_assignments:
        try:
            due_date_str = assignment.get('due_date', '')
            if 'T' in due_date_str:
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            else:
                due_date = datetime.fromisoformat(due_date_str)
            
            _, _, urgency = get_deadline_badge(due_date, 'pending')
            
            if urgency == 5:
                overdue += 1
            elif urgency == 4:
                today += 1
            elif urgency == 3:
                tomorrow += 1
            elif urgency == 2:
                this_week += 1
            else:
                later += 1
        except:
            later += 1
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("⚫ Gecikmiş", overdue)
    with col2:
        st.metric("🔴 Bugün", today)
    with col3:
        st.metric("🟠 Yarın", tomorrow)
    with col4:
        st.metric("🟡 Bu Hafta", this_week)
    with col5:
        st.metric("⚪ Sonra", later)
    
    st.markdown("---")
    
    # Type breakdown
    st.markdown("### 📝 Tür Dağılımı")
    
    type_counts = {}
    for assignment in all_assignments:
        atype = assignment.get('type', 'assignment')
        type_counts[atype] = type_counts.get(atype, 0) + 1
    
    if type_counts:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Ödev", type_counts.get('assignment', 0))
        with col2:
            st.metric("📄 Sınav", type_counts.get('exam', 0))
        with col3:
            st.metric("💼 Proje", type_counts.get('project', 0))
        with col4:
            st.metric("❓ Quiz", type_counts.get('quiz', 0))
    
    st.markdown("---")
    
    # Priority breakdown
    st.markdown("### 🎯 Öncelik Dağılımı")
    
    priority_counts = {'high': 0, 'medium': 0, 'low': 0}
    for assignment in pending_assignments:
        priority = assignment.get('priority', 'medium')
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔴 Yüksek", priority_counts['high'])
    with col2:
        st.metric("🟡 Orta", priority_counts['medium'])
    with col3:
        st.metric("🟢 Düşük", priority_counts['low'])

# Bottom statistics
st.markdown("---")
st.subheader("📊 Hızlı İstatistikler")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Toplam Görev", AssignmentManager.get_assignment_count())
with col2:
    st.metric("Bekleyen", AssignmentManager.get_pending_count())
with col3:
    upcoming = len(AssignmentManager.get_upcoming_assignments(7))
    st.metric("Yaklaşan (7 gün)", upcoming)

# Bulk calendar export
st.markdown("---")
st.subheader("📅 Toplu Takvim Aktarımı")
st.info("💡 **Tüm bekleyen görevlerinizi bir seferde takviminize ekleyin!**")

col1, col2 = st.columns(2)

with col1:
    if st.button("📅 Tüm Bekleyen Görevleri Takvime Aktar", use_container_width=True, type="primary"):
        pending = AssignmentManager.get_assignments_by_status('pending')
        if pending:
            ics_content = CalendarExport.create_multiple_events_ics(pending)
            download_link = CalendarExport.create_download_link(
                ics_content,
                f"dersly-tum-gorevler-{datetime.now().strftime('%Y%m%d')}"
            )
            st.markdown(download_link, unsafe_allow_html=True)
            st.success(f"✅ {len(pending)} görev takvim dosyasına eklendi!")
            st.caption("💡 İndirilen dosyayı açarak tüm görevleri takviminize ekleyebilirsiniz")
        else:
            st.warning("⚠️ Bekleyen görev bulunamadı")

with col2:
    if st.button("📅 Yaklaşan Görevleri Takvime Aktar (7 gün)", use_container_width=True):
        upcoming_assignments = AssignmentManager.get_upcoming_assignments(7)
        if upcoming_assignments:
            ics_content = CalendarExport.create_multiple_events_ics(upcoming_assignments)
            download_link = CalendarExport.create_download_link(
                ics_content,
                f"dersly-yaklasan-gorevler-{datetime.now().strftime('%Y%m%d')}"
            )
            st.markdown(download_link, unsafe_allow_html=True)
            st.success(f"✅ {len(upcoming_assignments)} yaklaşan görev takvim dosyasına eklendi!")
            st.caption("💡 İndirilen dosyayı açarak yaklaşan görevleri takviminize ekleyebilirsiniz")
        else:
            st.info("ℹ️ Yaklaşan görev bulunamadı")
