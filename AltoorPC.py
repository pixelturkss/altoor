import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import hashlib

# Önbelleği temizle
st.cache_resource.clear()

@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets["firebase"])
            
            # --- KRİTİK TEMİZLİK BÖLGESİ ---
            pk = cred_dict["private_key"]
            # 1. Önce tüm gizli kaçış karakterlerini temizle
            pk = pk.replace("\\n", "\n")
            # 2. Eğer çift tırnaklar arasında kaldıysa onları temizle
            pk = pk.strip('"').strip("'")
            cred_dict["private_key"] = pk
            # ------------------------------

            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
            return False
    return True

st.title("🏔️ ALTOOR")

if init_firebase():
    # TEST: Veritabanından veri çekmeyi dene (Hata buradaysa hemen görelim)
    try:
        test_get = db.reference('users').get()
        st.success("✅ VERİ TABANI BAĞLANTISI TAMAM!")
        
        # Giriş/Kayıt kodlarını buraya ekle (Bir önceki mesajdaki gibi)
        st.info("Şimdi kayıt olup mesaj atabilirsin.")
    except Exception as e:
        st.error(f"Bağlantı kuruldu ama veri çekilemiyor: {e}")
