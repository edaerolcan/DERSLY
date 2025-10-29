"""
Profile page for DERSLY Streamlit application.
Manages user profile and data export/import.
"""
import streamlit as st
from utils.storage_manager import StorageManager
from utils.user_manager import UserManager
from utils.input_validator import InputValidator
from utils.export_import_ui import (
    show_export_button,
    show_import_button,
    show_clear_data_button,
    show_storage_info
)
from utils.ui_styles import apply_modern_style

# Page configuration
st.set_page_config(
    page_title="Profil - DERSLY",
    page_icon="👤",
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
    <h1>👤 Profil</h1>
    <p>Kullanıcı bilgilerinizi ve verilerinizi yönetin</p>
</div>
""", unsafe_allow_html=True)

# Get profile
profile = UserManager.get_profile()

# Check if profile exists
if not profile:
    # Show profile creation form
    st.info("✨ Profil oluşturarak DERSLY deneyiminizi kişiselleştirin!")
    
    with st.form("create_profile_form"):
        name = st.text_input(
            "👤 Ad Soyad *",
            placeholder="Ahmet Yılmaz",
            help="Tam adınızı girin"
        )
        
        email = st.text_input(
            "📧 E-posta *",
            placeholder="ornek@universite.edu.tr",
            help="E-posta adresiniz"
        )
        
        st.markdown("---")
        st.markdown("#### Opsiyonel Bilgiler")
        
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input(
                "🎓 Öğrenci No",
                placeholder="2020123456"
            )
            department = st.text_input(
                "🏫 Bölüm",
                placeholder="Bilgisayar Mühendisliği"
            )
        with col2:
            class_year = st.number_input(
                "📅 Sınıf",
                min_value=1,
                max_value=8,
                value=1,
                step=1
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("🎉 Profil Oluştur", use_container_width=True, type="primary")
        
        if submitted:
            # Prepare profile data for validation
            profile_data = {
                'name': name,
                'email': email,
                'student_id': student_id if student_id else None,
                'department': department if department else None,
                'class_year': class_year if class_year else None
            }
            
            # Validate profile data
            is_valid, error_message = InputValidator.validate_profile(profile_data)
            
            if not is_valid:
                st.error(error_message)
            else:
                # Create profile
                UserManager.create_profile(
                    name=name.strip(),
                    email=email.strip(),
                    student_id=student_id.strip() if student_id else None,
                    department=department.strip() if department else None,
                    class_year=class_year if class_year else None
                )
                
                st.success("✅ Profiliniz başarıyla oluşturuldu!")
                st.balloons()
                st.rerun()
    
    st.stop()

# Tabs
tab1, tab2, tab3 = st.tabs(["👤 Profil Bilgileri", "💾 Veri Yönetimi", "⚙️ Ayarlar"])

with tab1:
    st.subheader("Profil Bilgileri")
    
    # Display current profile
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 👤")
        st.markdown(f"**{profile.get('name', 'Kullanıcı')}**")
    
    with col2:
        st.write(f"**📧 E-posta:** {profile.get('email', 'Belirtilmemiş')}")
        if profile.get('student_id'):
            st.write(f"**🎓 Öğrenci No:** {profile.get('student_id')}")
        if profile.get('department'):
            st.write(f"**🏫 Bölüm:** {profile.get('department')}")
        if profile.get('class_year'):
            st.write(f"**📅 Sınıf:** {profile.get('class_year')}")
    
    st.markdown("---")
    
    # Edit profile
    st.subheader("Profili Düzenle")
    
    with st.form("edit_profile_form"):
        name = st.text_input("Ad Soyad *", value=profile.get('name', ''))
        email = st.text_input("E-posta *", value=profile.get('email', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input("Öğrenci No", value=profile.get('student_id', '') or '')
            department = st.text_input("Bölüm", value=profile.get('department', '') or '')
        with col2:
            class_year = st.number_input(
                "Sınıf",
                min_value=1,
                max_value=6,
                value=profile.get('class_year', 1) or 1,
                step=1
            )
        
        submitted = st.form_submit_button("💾 Kaydet", type="primary", use_container_width=True)
        
        if submitted:
            # Prepare profile data for validation
            profile_data = {
                'name': name,
                'email': email,
                'student_id': student_id if student_id else None,
                'department': department if department else None,
                'class_year': class_year if class_year else None
            }
            
            # Validate profile data
            is_valid, error_message = InputValidator.validate_profile(profile_data)
            
            if not is_valid:
                st.error(error_message)
            else:
                updates = {
                    'name': name,
                    'email': email,
                    'student_id': student_id if student_id else None,
                    'department': department if department else None,
                    'class_year': class_year if class_year else None
                }
                
                if UserManager.update_profile(updates):
                    st.success("✅ Profil güncellendi!")
                    st.rerun()
                else:
                    st.error("❌ Profil güncellenemedi!")

with tab2:
    st.subheader("Veri Yönetimi")
    
    st.info("""
    **💡 Önemli Bilgi:**
    Verileriniz tarayıcınızda saklanmaktadır. Tarayıcı önbelleğini temizlerseniz veya farklı bir cihaz kullanırsanız verileriniz kaybolabilir.
    
    **Öneriler:**
    - Düzenli olarak verilerinizi dışa aktararak yedekleyin
    - Farklı cihazlarda kullanmak için veri aktarımı yapın
    - Önemli değişikliklerden önce yedek alın
    """)
    
    st.markdown("---")
    
    # Storage info
    show_storage_info()
    
    st.markdown("---")
    
    # Export section
    show_export_button()
    
    st.markdown("---")
    
    # Import section
    show_import_button()

with tab3:
    st.subheader("Ayarlar")
    
    st.markdown("### 🗑️ Tehlikeli Bölge")
    st.warning("⚠️ Aşağıdaki işlemler geri alınamaz!")
    
    # Clear data section
    show_clear_data_button()
    
    st.markdown("---")
    
    # About section
    st.markdown("### ℹ️ Hakkında")
    st.info("""
    **DERSLY - Öğrenci Destek Platformu**
    
    Versiyon: 2.0.0 (Browser Storage)
    
    Bu uygulama, üniversite öğrencilerinin ders programlarını, ödevlerini ve notlarını yönetmelerine yardımcı olur.
    
    **Özellikler:**
    - 📚 Ders programı yönetimi
    - 📝 Ödev ve sınav takibi
    - 📊 GPA hesaplama
    - 📅 Takvim görünümü
    - 💾 Veri yedekleme ve geri yükleme
    
    **Veri Gizliliği:**
    Tüm verileriniz tarayıcınızda saklanır ve sunucuya gönderilmez.
    """)
    
    # Tips
    with st.expander("💡 İpuçları ve Püf Noktaları"):
        st.markdown("""
        **Veri Yönetimi:**
        - Her hafta verilerinizi dışa aktarın
        - Yedek dosyalarınızı güvenli bir yerde saklayın
        - Farklı cihazlarda kullanmak için veri aktarımı yapın
        
        **Performans:**
        - Çok fazla eski veri biriktirmeyin
        - Tamamlanan görevleri düzenli olarak silin
        - Tarayıcı önbelleğini temizlerken dikkatli olun
        
        **Güvenlik:**
        - Yedek dosyalarınızı şifreleyin (opsiyonel)
        - Paylaşımlı bilgisayarlarda oturumu kapatın
        - Hassas bilgileri not açıklamalarına yazmayın
        """)
