import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Önbelleği temizle
st.cache_resource.clear()

# JSON dosyasındaki verileri BURAYA elinle yaz (Kopyala-yapıştır hatasını önlemek için)
key_dict = {
  "type": "service_account",
  "project_id": "altoor-a8df0",
  "private_key_id": "ca77f9ba4f9e35430ced92d4687cd13403b3022f",
  "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
  "client_email": "firebase-adminsdk-fbsvc@altoor-a8df0.iam.gserviceaccount.com",
  "client_id": "101980292881823607852",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40altoor-a8df0.iam.gserviceaccount.com"
}

if not firebase_admin._apps:
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
    })

st.title("🏔️ ALTOOR")

try:
    # Veritabanına bir test verisi gönderelim (En kesin kanıt)
    db.reference('baglanti_testi').set({'durum': 'basarili', 'zaman': 'su an'})
    st.success("✅ OLDU! Firebase'e veri yazıldı.")
    st.balloons()
except Exception as e:
    st.error(f"Hala hata var: {e}")
