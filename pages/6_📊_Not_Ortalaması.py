"""
GPA page for DERSLY Streamlit application.
Manages grade entries and calculates GPA.
"""
import streamlit as st
from utils.storage_manager import StorageManager
from utils.user_manager import UserManager
from utils.grade_manager import GradeManager
from utils.input_validator import InputValidator
from utils.ui_styles import apply_modern_style

# Page configuration
st.set_page_config(
    page_title="Not Ortalaması - DERSLY",
    page_icon="📊",
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
    <h1>📊 Not Ortalaması (GPA)</h1>
    <p>Notlarınızı girin ve GPA'nizi otomatik hesaplayın</p>
</div>
""", unsafe_allow_html=True)

# Display GPA
st.subheader("🎯 Genel Not Ortalaması (GNO)")

gpa = GradeManager.calculate_gpa()
total_credits = GradeManager.get_total_credits()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("GNO", f"{gpa:.2f}" if gpa > 0 else "N/A")
with col2:
    st.metric("Toplam Kredi", total_credits)
with col3:
    st.metric("Ders Sayısı", GradeManager.get_grade_count())

st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 Notlar", "➕ Not Ekle", "📈 Dönemlik GPA"])

with tab1:
    st.subheader("Tüm Notlar")
    
    grades = GradeManager.get_all_grades()
    
    if grades:
        # Sort by semester and year
        grades.sort(key=lambda x: (x.get('year', 0), x.get('semester', '')), reverse=True)
        
        for grade in grades:
            with st.expander(f"{grade.get('course_name', 'Ders')} - {grade.get('grade', 0):.2f}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Ders:** {grade.get('course_name', 'Belirtilmemiş')}")
                    st.write(f"**Not:** {grade.get('grade', 0):.2f} / 4.00")
                    st.write(f"**Kredi:** {grade.get('credits', 0)}")
                    st.write(f"**Dönem:** {grade.get('semester', '')} {grade.get('year', '')}")
                    
                    # Grade interpretation
                    grade_value = grade.get('grade', 0)
                    if grade_value >= 3.5:
                        st.success("🌟 Mükemmel!")
                    elif grade_value >= 3.0:
                        st.info("👍 İyi")
                    elif grade_value >= 2.5:
                        st.warning("📚 Orta")
                    else:
                        st.error("⚠️ Geliştirilmeli")
                
                with col2:
                    # Delete button
                    if st.button("🗑️ Sil", key=f"delete_grade_{grade['id']}"):
                        if GradeManager.delete_grade(grade['id']):
                            st.success("✅ Not silindi!")
                            st.rerun()
                        else:
                            st.error("❌ Not silinemedi!")
    else:
        st.info("📊 Henüz not girilmemiş. 'Not Ekle' sekmesinden not ekleyebilirsiniz.")

with tab2:
    st.subheader("Yeni Not Ekle")
    
    with st.form("add_grade_form"):
        course_name = st.text_input("Ders Adı *", placeholder="Veri Yapıları")
        
        col1, col2 = st.columns(2)
        with col1:
            grade = st.number_input(
                "Not (0.0 - 4.0) *",
                min_value=0.0,
                max_value=4.0,
                value=3.0,
                step=0.1,
                format="%.2f"
            )
        with col2:
            credits = st.number_input(
                "Kredi *",
                min_value=1,
                max_value=10,
                value=3,
                step=1
            )
        
        col3, col4 = st.columns(2)
        with col3:
            semester = st.selectbox(
                "Dönem *",
                options=["Fall", "Spring", "Summer"],
                format_func=lambda x: {"Fall": "Güz", "Spring": "Bahar", "Summer": "Yaz"}[x]
            )
        with col4:
            year = st.number_input(
                "Yıl *",
                min_value=2020,
                max_value=2030,
                value=2024,
                step=1
            )
        
        # Grade scale reference
        with st.expander("📖 Not Skalası Referansı - Tüm Sistemler"):
            tab1, tab2, tab3, tab4 = st.tabs(["4.0 Çift Harf", "4.0 Tek Harf", "4.0 Artı/Eksi", "5.0 Sistem"])
            
            with tab1:
                st.markdown("**4.0 Çift Harf Sistemi** (İTÜ, Hacettepe, vb.)")
                st.markdown("""
                | Harf Notu | Puan |
                |-----------|------|
                | AA        | 4.00 |
                | BA        | 3.50 |
                | BB        | 3.00 |
                | CB        | 2.50 |
                | CC        | 2.00 |
                | DC        | 1.50 |
                | DD        | 1.00 |
                | FD        | 0.50 |
                | FF        | 0.00 |
                """)
            
            with tab2:
                st.markdown("**4.0 Tek Harf Sistemi** (Boğaziçi, ODTÜ, vb.)")
                st.markdown("""
                | Harf Notu | Puan |
                |-----------|------|
                | A         | 4.00 |
                | B         | 3.00 |
                | C         | 2.00 |
                | D         | 1.00 |
                | F         | 0.00 |
                """)
            
            with tab3:
                st.markdown("**4.0 Artı/Eksi Sistemi** (Koç, Sabancı, Bahçeşehir, vb.)")
                st.markdown("""
                | Harf Notu | Puan |
                |-----------|------|
                | A+        | 4.00 |
                | A         | 4.00 |
                | A-        | 3.70 |
                | B+        | 3.30 |
                | B         | 3.00 |
                | B-        | 2.70 |
                | C+        | 2.30 |
                | C         | 2.00 |
                | C-        | 1.70 |
                | D+        | 1.30 |
                | D         | 1.00 |
                | F         | 0.00 |
                """)
            
            with tab4:
                st.markdown("**5.0 Sayısal Sistem**")
                st.markdown("""
                | Not | Puan |
                |-----|------|
                | 5   | 5.00 |
                | 4   | 4.00 |
                | 3   | 3.00 |
                | 2   | 2.00 |
                | 1   | 1.00 |
                | 0   | 0.00 |
                """)
        
        submitted = st.form_submit_button("➕ Not Ekle", type="primary", use_container_width=True)
        
        if submitted:
            # Prepare grade data for validation
            grade_data = {
                'course_name': course_name,
                'grade_value': grade,
                'credits': credits,
                'semester': semester,
                'year': year
            }
            
            # Validate grade data
            is_valid, error_message = InputValidator.validate_grade(grade_data)
            
            if not is_valid:
                st.error(error_message)
            else:
                # Rename grade_value back to grade for storage
                grade_data['grade'] = grade_data.pop('grade_value')
                
                grade_id = GradeManager.add_grade(grade_data)
                st.success(f"✅ Not başarıyla eklendi! (ID: {grade_id})")
                st.balloons()
                st.rerun()

with tab3:
    st.subheader("Dönemlik GPA Hesaplama")
    
    # Get unique semesters
    semesters = GradeManager.get_semesters()
    
    if semesters:
        st.write("**Dönemler:**")
        
        for semester, year in semesters:
            semester_gpa = GradeManager.calculate_semester_gpa(semester, year)
            semester_grades = GradeManager.get_grades_by_semester(semester, year)
            semester_credits = sum(g.get('credits', 0) for g in semester_grades)
            
            semester_name_tr = {"Fall": "Güz", "Spring": "Bahar", "Summer": "Yaz"}.get(semester, semester)
            
            with st.expander(f"{semester_name_tr} {year} - GPA: {semester_gpa:.2f}"):
                st.metric("Dönem GPA", f"{semester_gpa:.2f}")
                st.metric("Toplam Kredi", semester_credits)
                st.metric("Ders Sayısı", len(semester_grades))
                
                st.markdown("**Dersler:**")
                for g in semester_grades:
                    st.write(f"- {g.get('course_name')}: {g.get('grade'):.2f} ({g.get('credits')} kredi)")
    else:
        st.info("📊 Henüz not girilmemiş.")

# GPA Calculator Tool
st.markdown("---")
st.subheader("🧮 GPA Hesaplayıcı")

with st.expander("💡 Hızlı GPA Hesaplama"):
    st.markdown("Yeni notlarınızı eklemeden önce GPA'nizi tahmin edin:")
    
    num_courses = st.number_input("Ders Sayısı", min_value=1, max_value=10, value=3)
    
    total_points = 0
    total_credits_calc = 0
    
    for i in range(num_courses):
        col1, col2 = st.columns(2)
        with col1:
            grade_calc = st.number_input(f"Ders {i+1} Notu", min_value=0.0, max_value=4.0, value=3.0, step=0.1, key=f"calc_grade_{i}")
        with col2:
            credits_calc = st.number_input(f"Ders {i+1} Kredi", min_value=1, max_value=10, value=3, key=f"calc_credits_{i}")
        
        total_points += grade_calc * credits_calc
        total_credits_calc += credits_calc
    
    if total_credits_calc > 0:
        calculated_gpa = total_points / total_credits_calc
        st.success(f"**Hesaplanan GPA:** {calculated_gpa:.2f}")
