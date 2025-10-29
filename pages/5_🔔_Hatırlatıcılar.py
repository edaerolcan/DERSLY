"""
Reminders page for DERSLY Streamlit application.
Manages reminders for assignments and events.
"""
import streamlit as st
from utils.storage_manager import StorageManager
from utils.user_manager import UserManager
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
    <p>Önemli tarihler için hatırlatıcılar oluşturun</p>
</div>
""", unsafe_allow_html=True)

# Info message
st.info("""
**💡 Bilgi:**
Hatırlatıcı özelliği şu anda geliştirme aşamasındadır.

**Mevcut Alternatifler:**
- Ödevler sayfasından görevlerinizi takip edebilirsiniz
- Takvim sayfasından yaklaşan görevleri görebilirsiniz
- Ana sayfada yaklaşan görevler otomatik olarak gösterilir

**Gelecek Güncellemeler:**
- E-posta hatırlatıcıları
- Tarayıcı bildirimleri
- Özelleştirilebilir hatırlatma süreleri
""")

st.markdown("---")

# Quick links
st.subheader("⚡ Hızlı Erişim")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝 Ödevlere Git", use_container_width=True):
        st.switch_page("pages/3_📝_Assignments.py")

with col2:
    if st.button("📅 Takvime Git", use_container_width=True):
        st.switch_page("pages/4_📅_Calendar.py")

with col3:
    if st.button("🏠 Ana Sayfaya Git", use_container_width=True):
        st.switch_page("pages/1_🏠_Home.py")
