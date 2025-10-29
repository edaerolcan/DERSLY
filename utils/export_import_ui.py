"""
Export/Import UI components for DERSLY Streamlit application.
Provides user interface for data backup and restore operations.
"""
import streamlit as st
import json
from datetime import datetime
from utils.storage_manager import StorageManager


def show_export_button() -> None:
    """
    Display export button and handle export operation.
    Generates JSON file with timestamp and triggers download.
    """
    st.markdown("### 📥 Verileri Dışa Aktar")
    st.markdown("Tüm verilerinizi JSON dosyası olarak indirin ve yedekleyin.")
    
    # Get storage info
    info = StorageManager.get_storage_info()
    
    # Show what will be exported
    st.info(f"""
    **Dışa aktarılacak veriler:**
    - 👤 Kullanıcı Profili: {'✅ Var' if info['has_profile'] else '❌ Yok'}
    - 📚 Dersler: {info['num_courses']} adet
    - 📝 Ödevler: {info['num_assignments']} adet
    - 📊 Notlar: {info['num_grades']} adet
    - 🔔 Hatırlatıcılar: {info['num_reminders']} adet
    """)
    
    # Export button
    if st.button("📥 Verileri İndir", type="primary", use_container_width=True):
        try:
            # Get export data
            export_data = StorageManager.export_data()
            
            # Convert to JSON
            json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"dersly_backup_{timestamp}.json"
            
            # Create download button
            st.download_button(
                label="💾 Dosyayı Kaydet",
                data=json_str,
                file_name=filename,
                mime="application/json",
                use_container_width=True
            )
            
            st.success("✅ Veriler başarıyla hazırlandı! Yukarıdaki butona tıklayarak indirebilirsiniz.")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Dışa aktarma hatası: {str(e)}")
    
    # Show last export info
    if info['last_export']:
        try:
            last_export = datetime.fromisoformat(info['last_export'])
            st.caption(f"Son dışa aktarma: {last_export.strftime('%d.%m.%Y %H:%M')}")
        except:
            pass


def show_import_button() -> None:
    """
    Display import button and handle import operation.
    Shows file uploader with validation and confirmation dialog.
    """
    st.markdown("### 📤 Verileri İçe Aktar")
    st.markdown("Daha önce dışa aktardığınız JSON dosyasını yükleyin.")
    
    # Warning about overwriting data
    has_data = StorageManager.has_data()
    if has_data:
        st.warning("⚠️ **Dikkat:** Veri içe aktarma işlemi mevcut tüm verilerinizin üzerine yazacaktır!")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "JSON dosyası seçin",
        type=['json'],
        help="Daha önce dışa aktardığınız DERSLY yedek dosyasını seçin"
    )
    
    if uploaded_file is not None:
        try:
            # Read and parse JSON
            json_str = uploaded_file.read().decode('utf-8')
            import_data = json.loads(json_str)
            
            # Show preview of data
            st.info(f"""
            **Dosyada bulunan veriler:**
            - 👤 Kullanıcı Profili: {'✅ Var' if import_data.get('user_profile') else '❌ Yok'}
            - 📚 Dersler: {len(import_data.get('courses', []))} adet
            - 📝 Ödevler: {len(import_data.get('assignments', []))} adet
            - 📊 Notlar: {len(import_data.get('grades', []))} adet
            - 🔔 Hatırlatıcılar: {len(import_data.get('reminders', []))} adet
            - 📅 Dışa aktarma tarihi: {import_data.get('exported_at', 'Bilinmiyor')}
            """)
            
            # Confirmation required if data exists
            if has_data:
                st.error("🚨 **UYARI:** Bu işlem geri alınamaz! Mevcut verileriniz silinecektir.")
                
                confirm = st.checkbox(
                    "Mevcut verilerimin silineceğini anlıyorum ve devam etmek istiyorum",
                    key="import_confirm"
                )
                
                if not confirm:
                    st.info("👆 Devam etmek için yukarıdaki onay kutusunu işaretleyin.")
                    return
            
            # Import button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📤 Verileri İçe Aktar", type="primary", use_container_width=True):
                    # Perform import
                    success, message = StorageManager.import_data(import_data)
                    
                    if success:
                        st.success(message)
                        st.balloons()
                        st.info("🔄 Sayfa yenileniyor...")
                        # Trigger rerun to refresh UI
                        st.rerun()
                    else:
                        st.error(message)
        
        except json.JSONDecodeError:
            st.error("❌ Geçersiz JSON dosyası. Lütfen geçerli bir DERSLY yedek dosyası seçin.")
        except Exception as e:
            st.error(f"❌ Dosya okuma hatası: {str(e)}")
    
    # Show last import info
    info = StorageManager.get_storage_info()
    if info['last_import']:
        try:
            last_import = datetime.fromisoformat(info['last_import'])
            st.caption(f"Son içe aktarma: {last_import.strftime('%d.%m.%Y %H:%M')}")
        except:
            pass


def show_clear_data_button() -> None:
    """
    Display clear data button with strong warning and confirmation.
    Allows user to delete all data and start fresh.
    """
    st.markdown("### 🗑️ Tüm Verileri Temizle")
    st.markdown("Tüm verilerinizi silmek ve sıfırdan başlamak için bu seçeneği kullanın.")
    
    # Check if data exists
    has_data = StorageManager.has_data()
    
    if not has_data:
        st.info("ℹ️ Temizlenecek veri bulunmuyor.")
        return
    
    # Show what will be deleted
    info = StorageManager.get_storage_info()
    st.warning(f"""
    **⚠️ Silinecek veriler:**
    - 👤 Kullanıcı Profili: {'✅ Var' if info['has_profile'] else '❌ Yok'}
    - 📚 Dersler: {info['num_courses']} adet
    - 📝 Ödevler: {info['num_assignments']} adet
    - 📊 Notlar: {info['num_grades']} adet
    - 🔔 Hatırlatıcılar: {info['num_reminders']} adet
    """)
    
    # Strong warning
    st.error("🚨 **UYARI:** Bu işlem geri alınamaz! Tüm verileriniz kalıcı olarak silinecektir.")
    st.error("💡 **Öneri:** Devam etmeden önce verilerinizi dışa aktararak yedekleyin.")
    
    # Confirmation checkboxes
    confirm1 = st.checkbox(
        "Tüm verilerimin silineceğini anlıyorum",
        key="clear_confirm1"
    )
    
    confirm2 = st.checkbox(
        "Bu işlemin geri alınamayacağını kabul ediyorum",
        key="clear_confirm2"
    )
    
    # Clear button (only enabled if both confirmations checked)
    if confirm1 and confirm2:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🗑️ TÜM VERİLERİ SİL", type="secondary", use_container_width=True):
                # Clear all data
                StorageManager.clear_all_data()
                st.success("✅ Tüm veriler başarıyla silindi!")
                st.info("🔄 Sayfa yenileniyor...")
                # Trigger rerun to refresh UI
                st.rerun()
    else:
        st.info("👆 Devam etmek için yukarıdaki onay kutularını işaretleyin.")


def show_storage_info() -> None:
    """
    Display storage usage information and statistics.
    Shows current data counts and estimated storage size.
    """
    st.markdown("### 💾 Depolama Bilgileri")
    
    # Get storage info
    info = StorageManager.get_storage_info()
    
    # Display statistics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Dersler", info['num_courses'])
    
    with col2:
        st.metric("📝 Ödevler", info['num_assignments'])
    
    with col3:
        st.metric("📊 Notlar", info['num_grades'])
    
    with col4:
        st.metric("🔔 Hatırlatıcılar", info['num_reminders'])
    
    # Total items
    st.info(f"**Toplam Kayıt:** {info['total_items']} adet")
    
    # Storage size estimation
    if info['size_kb'] < 1:
        size_str = f"{info['size_bytes']} bytes"
    elif info['size_mb'] < 1:
        size_str = f"{info['size_kb']} KB"
    else:
        size_str = f"{info['size_mb']} MB"
    
    st.caption(f"Tahmini depolama boyutu: {size_str}")
    
    # Storage warning (if approaching limits)
    # Assuming 5MB limit for session state (conservative estimate)
    max_size_mb = 5.0
    usage_percent = (info['size_mb'] / max_size_mb) * 100
    
    if usage_percent > 80:
        st.warning(f"""
        ⚠️ **Depolama Uyarısı:** Depolama alanınızın %{int(usage_percent)}'i kullanılıyor.
        
        Verilerinizi dışa aktararak yedeklemenizi ve gereksiz kayıtları silmenizi öneririz.
        """)
    elif usage_percent > 50:
        st.info(f"ℹ️ Depolama kullanımı: %{int(usage_percent)}")
    
    # Data version info
    st.caption(f"Veri formatı versiyonu: {info['version']}")
    
    # Profile status
    if info['has_profile']:
        st.success("✅ Kullanıcı profili mevcut")
    else:
        st.warning("⚠️ Kullanıcı profili oluşturulmamış")
    
    # Tips
    with st.expander("💡 İpuçları"):
        st.markdown("""
        - **Düzenli Yedekleme:** Verilerinizi düzenli olarak dışa aktararak yedekleyin
        - **Tarayıcı Değişikliği:** Farklı tarayıcı veya cihaz kullanıyorsanız, verilerinizi içe aktarın
        - **Veri Kaybı:** Tarayıcı önbelleğini temizlerseniz verileriniz kaybolabilir
        - **Depolama Limiti:** Çok fazla veri eklerseniz performans sorunları yaşayabilirsiniz
        - **Gizlilik:** Verileriniz sadece tarayıcınızda saklanır, sunucuya gönderilmez
        """)
