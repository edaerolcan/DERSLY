"""
Main entry point for DERSLY Streamlit application.
Simplified version using browser storage instead of database.
"""
import streamlit as st
from utils.storage_manager import StorageManager
from utils.user_manager import UserManager
from utils.ui_styles import apply_modern_style, show_logo_in_sidebar

# Page configuration
st.set_page_config(
    page_title="DERSLY - Öğrenci Destek Platformu",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "DERSLY - Üniversite Öğrenci Destek Platformu v2.0"
    }
)

# Apply modern styling
apply_modern_style()

# Show logo in sidebar
show_logo_in_sidebar()


def show_profile_setup():
    """Display profile setup page for first-time users."""
    st.markdown("""
    <div class="page-header">
        <h1>📚 DERSLY</h1>
        <p>Üniversite Öğrenci Destek Platformu</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header">
        <h2>👤 Profil Oluştur</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("✨ Başlamak için profilinizi oluşturun ve DERSLY'nin tüm özelliklerinden yararlanın!")
    
    with st.form("profile_setup_form"):
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
                max_value=6,
                value=1,
                step=1
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit = st.form_submit_button("🎉 Profil Oluştur", use_container_width=True, type="primary")
        
        if submit:
            if not name or not email:
                st.error("❌ Lütfen ad soyad ve e-posta alanlarını doldurun.")
            elif len(name.strip()) < 2:
                st.error("👤 Ad Soyad en az 2 karakter olmalıdır")
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


def show_main_app():
    """Display the main application."""
    # Get user profile (optional)
    profile = UserManager.get_profile()
    
    # Sidebar - only show profile if it exists
    with st.sidebar:
        if profile:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 12px; margin-bottom: 1rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">👤</div>
                <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">{}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">📧 {}</div>
                {} {}
            </div>
            """.format(
                profile.get('name', 'Kullanıcı'),
                profile.get('email', ''),
                f"<div style='font-size: 0.9rem; opacity: 0.9;'>🎓 {profile.get('student_id')}</div>" if profile.get('student_id') else "",
                f"<div style='font-size: 0.9rem; opacity: 0.9;'>🏫 {profile.get('department')}</div>" if profile.get('department') else ""
            ), unsafe_allow_html=True)
        else:
            # Show a simple message when no profile exists
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 12px; margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👋</div>
                <div style="font-size: 0.9rem; opacity: 0.7;">Profil oluşturmak için Profil sayfasını ziyaret edin</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Main content
    st.markdown("""
    <div class="page-header">
        <h1>📚 DERSLY</h1>
        <p>Hoş Geldiniz! Üniversite hayatınızı kolaylaştırmak için buradayız.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <p style="margin: 0; font-size: 1.1rem;">
            <strong>👈 Sol menüden</strong> sayfalar arasında gezinebilir ve tüm özelliklerimizi keşfedebilirsiniz!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick navigation cards
    st.markdown("""
    <div class="section-header">
        <h2>🚀 Hızlı Erişim</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="custom-card" style="text-align: center; cursor: pointer;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📚</div>
            <h3 style="margin-bottom: 0.5rem;">Dersler</h3>
            <p style="color: #666; margin: 0;">Ders programınızı yönetin</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card" style="text-align: center; cursor: pointer;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
            <h3 style="margin-bottom: 0.5rem;">Ödevler</h3>
            <p style="color: #666; margin: 0;">Ödev ve sınavlarınızı takip edin</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="custom-card" style="text-align: center; cursor: pointer;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h3 style="margin-bottom: 0.5rem;">Not Ortalaması</h3>
            <p style="color: #666; margin: 0;">GNO ve DNO hesaplayın</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features overview
    st.markdown("### ✨ Özellikler")
    
    features = [
        "🏠 **Ana Sayfa**: Genel istatistikler ve yaklaşan görevler",
        "📚 **Dersler**: Haftalık ders programı yönetimi",
        "📝 **Ödevler**: Ödev, sınav, proje ve quiz takibi",
        "📅 **Takvim**: Aylık takvim görünümü",
        "🔔 **Hatırlatıcılar**: Önemli tarihler için hatırlatıcılar",
        "📊 **Not Ortalaması**: GNO ve DNO hesaplama",
        "👤 **Profil**: Kullanıcı bilgileri ve veri yönetimi"
    ]
    
    for feature in features:
        st.markdown(feature)
    
    # Storage info
    st.markdown("---")
    st.markdown("### 💾 Veri Yönetimi")
    st.info("""
    **Önemli:** Verileriniz tarayıcınızda saklanmaktadır. 
    - Düzenli olarak verilerinizi dışa aktararak yedekleyin
    - Farklı cihazlarda kullanmak için Profil sayfasından veri aktarımı yapabilirsiniz
    """)


def main():
    """Main application entry point."""
    # Initialize storage
    StorageManager.initialize_storage()
    
    # Always show main app - profile is optional
    show_main_app()


if __name__ == "__main__":
    main()
