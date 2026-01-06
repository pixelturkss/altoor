import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Önbelleği temizle
st.cache_resource.clear()

# JSON dosyasını not defteriyle aç ve değerleri TEK TEK buraya yapıştır
# Kopyalarken başında sonunda boşluk kalmadığından emin ol!
service_account_info = {
  "type": "service_account",
  "project_id": "altoor-a8df0",
  "private_key_id": "ca77f9ba4f9e35430ced92d4687cd13403b3022f",
  "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
  "client_email": "firebase-adminsdk-fbsvc@altoor-a8df0.iam.gserviceaccount.com",
  "token_uri": "https://oauth2.googleapis.com/token",
}

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
        })
        st.success("Bağlantı Teknik Olarak Kuruldu!")
    except Exception as e:
        st.error(f"Başlatma Hatası: {e}")

try:
    # Veritabanını oku
    db.reference('users').get()
    st.balloons()
    st.success("ZİRVE TAMAM! UYUYABİLİRSİN.")
except Exception as e:
    st.error(f"Hata: {e}")
