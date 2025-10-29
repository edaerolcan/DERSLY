"""
Courses page for DERSLY Streamlit application.
Manages course schedule and information.
"""
import streamlit as st
from datetime import datetime, date, time
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
tab1, tab2, tab3 = st.tabs(["📋 Ders Listesi", "➕ Yeni Ders Ekle", "📅 Haftalık Program"])

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
                                        start_time_str = new_start.strftime("%H:%M") if new_start else course['start_time']
                                        end_time_str = new_end.strftime("%H:%M") if new_end else course['end_time']
                                        
                                        updates = {
                                            'course_name': new_name,
                                            'course_code': new_code,
                                            'credits': new_credits,
                                            'day': course['day'],  # Keep existing day
                                            'start_time': start_time_str,
                                            'end_time': end_time_str
                                        }
                                        
                                        # Check for time conflicts (exclude current course)
                                        has_conflict, conflicting_course = CourseManager.check_time_conflict(
                                            course['day'],
                                            start_time_str,
                                            end_time_str,
                                            exclude_course_id=course['id']
                                        )
                                        
                                        if has_conflict:
                                            st.error(f"⚠️ **Ders Çakışması!** Bu saatte zaten başka bir ders var:")
                                            st.warning(f"📚 **{conflicting_course['course_code']}** - {conflicting_course['course_name']}")
                                            st.info(f"⏰ {conflicting_course['start_time']} - {conflicting_course['end_time']}")
                                        else:
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
        
        # Time input
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input(
                "⏰ Başlangıç Saati *",
                value=datetime.strptime("09:00", "%H:%M").time(),
                help="Saati tıklayıp klavyeden yazabilirsiniz (örn: 10:20)"
            )
        with col2:
            end_time = st.time_input(
                "⏰ Bitiş Saati *",
                value=datetime.strptime("10:30", "%H:%M").time(),
                help="Saati tıklayıp klavyeden yazabilirsiniz (örn: 11:10)"
            )
        
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
            
            # Check for time conflicts
            has_conflict, conflicting_course = CourseManager.check_time_conflict(
                day, 
                start_time.strftime("%H:%M"), 
                end_time.strftime("%H:%M")
            )
            
            if has_conflict:
                st.error(f"⚠️ **Ders Çakışması!** Bu saatte zaten başka bir ders var:")
                st.warning(f"📚 **{conflicting_course['course_code']}** - {conflicting_course['course_name']}")
                st.info(f"⏰ {conflicting_course['start_time']} - {conflicting_course['end_time']}")
            else:
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

with tab3:
    st.subheader("📅 Haftalık Ders Programı")
    
    # Get weekly schedule
    schedule = CourseManager.get_weekly_schedule()
    
    # Day names in Turkish
    day_names_tr = {
        "Monday": "Pazartesi",
        "Tuesday": "Salı",
        "Wednesday": "Çarşamba",
        "Thursday": "Perşembe",
        "Friday": "Cuma",
        "Saturday": "Cumartesi",
        "Sunday": "Pazar"
    }
    
    # Check if there are any courses
    total_courses = sum(len(courses) for courses in schedule.values())
    
    if total_courses == 0:
        st.info("📚 Henüz ders eklenmemiş. Haftalık programınızı oluşturmak için ders ekleyin.")
    else:
        # Display schedule in grid format
        st.markdown("### 📊 Haftalık Görünüm")
        
        # Create columns for each day
        days_to_show = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        cols = st.columns(5)
        
        for idx, day in enumerate(days_to_show):
            with cols[idx]:
                st.markdown(f"**{day_names_tr[day]}**")
                
                day_courses = schedule[day]
                
                if day_courses:
                    for course in day_courses:
                        # Create course card
                        st.markdown(f"""
                        <div style="
                            background-color: {course['color']}20;
                            border-left: 4px solid {course['color']};
                            padding: 8px;
                            margin: 8px 0;
                            border-radius: 4px;
                        ">
                            <div style="font-weight: bold; font-size: 0.9em;">{course['course_code']}</div>
                            <div style="font-size: 0.8em; margin-top: 4px;">{course['course_name'][:20]}...</div>
                            <div style="font-size: 0.75em; color: #666; margin-top: 4px;">
                                ⏰ {course['start_time']} - {course['end_time']}
                            </div>
                            <div style="font-size: 0.75em; color: #666;">
                                📚 {course['credits']} Kredi
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("Ders yok")
        
        # Weekend courses if any
        weekend_courses = schedule["Saturday"] + schedule["Sunday"]
        if weekend_courses:
            st.markdown("---")
            st.markdown("### 📅 Hafta Sonu Dersleri")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**{day_names_tr['Saturday']}**")
                for course in schedule["Saturday"]:
                    st.markdown(f"""
                    <div style="
                        background-color: {course['color']}20;
                        border-left: 4px solid {course['color']};
                        padding: 8px;
                        margin: 8px 0;
                        border-radius: 4px;
                    ">
                        <div style="font-weight: bold;">{course['course_code']} - {course['course_name']}</div>
                        <div style="font-size: 0.9em; color: #666; margin-top: 4px;">
                            ⏰ {course['start_time']} - {course['end_time']} | 📚 {course['credits']} Kredi
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**{day_names_tr['Sunday']}**")
                for course in schedule["Sunday"]:
                    st.markdown(f"""
                    <div style="
                        background-color: {course['color']}20;
                        border-left: 4px solid {course['color']};
                        padding: 8px;
                        margin: 8px 0;
                        border-radius: 4px;
                    ">
                        <div style="font-weight: bold;">{course['course_code']} - {course['course_name']}</div>
                        <div style="font-size: 0.9em; color: #666; margin-top: 4px;">
                            ⏰ {course['start_time']} - {course['end_time']} | 📚 {course['credits']} Kredi
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Weekly statistics
        st.markdown("---")
        st.markdown("### 📊 Haftalık İstatistikler")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Toplam Ders", total_courses)
        
        with col2:
            total_credits = sum(c.get('credits', 3) for c in CourseManager.get_all_courses())
            st.metric("Toplam Kredi", total_credits)
        
        with col3:
            # Calculate total hours per week
            total_minutes = 0
            for day_courses in schedule.values():
                for course in day_courses:
                    start_h, start_m = map(int, course['start_time'].split(':'))
                    end_h, end_m = map(int, course['end_time'].split(':'))
                    duration = (end_h * 60 + end_m) - (start_h * 60 + start_m)
                    total_minutes += duration
            total_hours = total_minutes / 60
            st.metric("Haftalık Ders Saati", f"{total_hours:.1f}")
        
        with col4:
            # Find busiest day
            busiest_day = max(schedule.items(), key=lambda x: len(x[1]))
            if busiest_day[1]:
                st.metric("En Yoğun Gün", day_names_tr[busiest_day[0]])
            else:
                st.metric("En Yoğun Gün", "-")

# Statistics
st.markdown("---")
st.subheader("📊 İstatistikler")
col1, col2 = st.columns(2)
with col1:
    st.metric("Toplam Ders", CourseManager.get_course_count())
with col2:
    total_credits = sum(c.get('credits', 3) for c in CourseManager.get_all_courses())
    st.metric("Toplam Kredi", total_credits)
