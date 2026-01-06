import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

st.cache_resource.clear()

def start_firebase():
    if not firebase_admin._apps:
        try:
            # Secrets'tan sadece anahtarı alıyoruz
            pk = st.secrets["firebase"]["private_key"]
            
            # Sözlüğü burada oluşturuyoruz
            cred_dict = {
                "type": "service_account",
                "project_id": "altoor-a8df0",
                "private_key_id": "ca77f9ba4f9e35430ced92d4687cd13403b3022f",
                "private_key": pk,
                "client_email": "firebase-adminsdk-fbsvc@altoor-a8df0.iam.gserviceaccount.com",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40altoor-a8df0.iam.gserviceaccount.com"
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Hata: {e}")
            return False
    return True

st.title("🏔️ ALTOOR")

if start_firebase():
    try:
        # Test amaçlı veri okumaya çalış
        db.reference('users').get()
        st.success("✅ BAŞARILI! Firebase kapıları açtı.")
        st.balloons()
    except Exception as e:
        st.error(f"Bağlantı var ama imza hatası: {e}")
