"""
Courses page for DERSLY Streamlit application.
Manages course schedule and information.
"""
import streamlit as st
from utils.storage_manager import StorageManager
from utils.user_manager import UserManager
from utils.course_manager import CourseManager
from utils.input_validator import InputValidator
from utils.calendar_export import CalendarExport
from utils.ui_styles import apply_modern_style

# Page configuration
st.set_page_config(
    page_title="Dersler - DERSLY",
    page_icon="📚",
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
    <h1>📚 Dersler</h1>
    <p>Ders programınızı yönetin ve haftalık takviminizi oluşturun</p>
</div>
""", unsafe_allow_html=True)

# Tabs for different views
tab1, tab2 = st.tabs(["📋 Ders Listesi", "➕ Yeni Ders Ekle"])

with tab1:
    st.subheader("Tüm Dersler")
    
    courses = CourseManager.get_all_courses()
    
    if courses:
        # Group by day
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_names_tr = {
            "Monday": "Pazartesi",
            "Tuesday": "Salı",
            "Wednesday": "Çarşamba",
            "Thursday": "Perşembe",
            "Friday": "Cuma",
            "Saturday": "Cumartesi",
            "Sunday": "Pazar"
        }
        
        for day in days:
            day_courses = CourseManager.get_courses_by_day(day)
            if day_courses:
                st.markdown(f"### {day_names_tr[day]}")
                
                for course in day_courses:
                    with st.expander(f"{course['course_code']} - {course['course_name']} ({course['start_time']} - {course['end_time']})"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Ders Kodu:** {course['course_code']}")
                            st.write(f"**Ders Adı:** {course['course_name']}")
                            st.write(f"**Gün:** {day_names_tr[day]}")
                            st.write(f"**Saat:** {course['start_time']} - {course['end_time']}")
                            st.write(f"**Kredi:** {course.get('credits', 3)}")
                        
                        with col2:
                            # Edit button
                            if st.button("✏️ Düzenle", key=f"edit_{course['id']}"):
                                st.session_state[f'editing_course_{course["id"]}'] = True
                                st.rerun()
                            
                            # Delete button
                            if st.button("🗑️ Sil", key=f"delete_{course['id']}"):
                                if CourseManager.delete_course(course['id']):
                                    st.success("✅ Ders silindi!")
                                    st.rerun()
                                else:
                                    st.error("❌ Ders silinemedi!")
                        
                        # Edit form (if editing)
                        if st.session_state.get(f'editing_course_{course["id"]}', False):
                            st.markdown("---")
                            st.markdown("**Dersi Düzenle:**")
                            
                            with st.form(f"edit_form_{course['id']}"):
                                new_name = st.text_input("Ders Adı", value=course['course_name'])
                                new_code = st.text_input("Ders Kodu", value=course['course_code'])
                                
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    new_start = st.time_input("Başlangıç Saati", value=None)
                                with col_b:
                                    new_end = st.time_input("Bitiş Saati", value=None)
                                
                                new_credits = st.number_input("Kredi", min_value=1, max_value=10, value=course.get('credits', 3))
                                
                                col_x, col_y = st.columns(2)
                                with col_x:
                                    if st.form_submit_button("💾 Kaydet", use_container_width=True):
                                        # Prepare update data for validation
                                        updates = {
                                            'course_name': new_name,
                                            'course_code': new_code,
                                            'credits': new_credits,
                                            'day': course['day'],  # Keep existing day
                                            'start_time': new_start.strftime("%H:%M") if new_start else course['start_time'],
                                            'end_time': new_end.strftime("%H:%M") if new_end else course['end_time']
                                        }
                                        
                                        # Validate updated course data
                                        is_valid, error_message = InputValidator.validate_course(updates)
                                        
                                        if not is_valid:
                                            st.error(error_message)
                                        else:
                                            # Remove day from updates (not needed for update)
                                            updates.pop('day')
                                            
                                            if CourseManager.update_course(course['id'], updates):
                                                st.success("✅ Ders güncellendi!")
                                                del st.session_state[f'editing_course_{course["id"]}']
                                                st.rerun()
                                            else:
                                                st.error("❌ Ders güncellenemedi!")
                                
                                with col_y:
                                    if st.form_submit_button("❌ İptal", use_container_width=True):
                                        del st.session_state[f'editing_course_{course["id"]}']
                                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("📚 Henüz ders eklenmemiş. Yeni ders eklemek için 'Yeni Ders Ekle' sekmesini kullanın.")

with tab2:
    st.subheader("Yeni Ders Ekle")
    
    with st.form("add_course_form"):
        course_name = st.text_input("Ders Adı *", placeholder="Veri Yapıları")
        course_code = st.text_input("Ders Kodu *", placeholder="CS201")
        
        day = st.selectbox(
            "Gün *",
            options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            format_func=lambda x: {
                "Monday": "Pazartesi",
                "Tuesday": "Salı",
                "Wednesday": "Çarşamba",
                "Thursday": "Perşembe",
                "Friday": "Cuma",
                "Saturday": "Cumartesi",
                "Sunday": "Pazar"
            }[x]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input("Başlangıç Saati *")
        with col2:
            end_time = st.time_input("Bitiş Saati *")
        
        credits = st.number_input("Kredi", min_value=1, max_value=10, value=3)
        
        color = st.color_picker("Renk", value="#FF5733")
        
        submitted = st.form_submit_button("➕ Ders Ekle", type="primary", use_container_width=True)
        
        if submitted:
            # Prepare course data for validation
            course_data = {
                'course_name': course_name,
                'course_code': course_code,
                'day': day,
                'start_time': start_time.strftime("%H:%M"),
                'end_time': end_time.strftime("%H:%M"),
                'credits': credits,
                'color': color
            }
            
            # Validate course data
            is_valid, error_message = InputValidator.validate_course(course_data)
            
            if not is_valid:
                st.error(error_message)
            else:
                course_id = CourseManager.add_course(course_data)
                st.success(f"✅ Ders başarıyla eklendi! (ID: {course_id})")
                
                # Offer calendar export for recurring course
                st.info("📅 **Dersi mobil takviminize eklemek ister misiniz?**")
                
                # Get the created course
                created_course = CourseManager.get_course(course_id)
                if created_course:
                    # Create recurring iCalendar content (14 weeks = 1 semester)
                    ics_content = CalendarExport.create_course_ics(created_course, weeks=14)
                    download_link = CalendarExport.create_download_link(
                        ics_content,
                        f"dersly-{course_code.replace(' ', '-')}"
                    )
                    st.markdown(download_link, unsafe_allow_html=True)
                    st.caption("💡 İndirilen .ics dosyası dersi 14 hafta boyunca takviminize ekler")
                
                st.balloons()
                st.rerun()

# Statistics
st.markdown("---")
st.subheader("📊 İstatistikler")
col1, col2 = st.columns(2)
with col1:
    st.metric("Toplam Ders", CourseManager.get_course_count())
with col2:
    total_credits = sum(c.get('credits', 3) for c in CourseManager.get_all_courses())
    st.metric("Toplam Kredi", total_credits)
