@echo off
chcp 65001 >nul
echo ========================================
echo 📚 DERSLY - Hızlı Başlatma
echo ========================================
echo.
echo [1/2] Bağımlılıklar kontrol ediliyor...
python -c "import streamlit; print('✅ Streamlit hazır')" 2>nul
if errorlevel 1 (
    echo ❌ Streamlit bulunamadı!
    echo.
    echo Yükleniyor...
    pip install -r requirements.txt
)
echo.
echo [2/2] Uygulama başlatılıyor...
echo.
echo 🌐 Tarayıcınızda http://localhost:8501 açılacak
echo 🔄 Durdurmak için Ctrl+C basın
echo.
echo ========================================
echo.
python -m streamlit run app.py
pause
