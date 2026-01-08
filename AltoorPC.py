import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

st.cache_resource.clear()

def fix_and_connect():
    if not firebase_admin._apps:
        try:
            # 1. Anahtarı al ve satır satır temizle
            raw_key = st.secrets["firebase"]["private_key"]
            lines = raw_key.split('\n')
            clean_lines = [l.strip() for l in lines if l.strip()]
            final_key = "\n".join(clean_lines)
            
            # 2. Sözlüğü manuel olarak burada kur (En güvenlisi)
            config = {
                "type": "service_account",
                "project_id": "altoor-a8df0",
                "private_key_id": "ca77f9ba4f9e35430ced92d4687cd13403b3022f",
                "private_key": final_key,
                "client_email": "firebase-adminsdk-fbsvc@altoor-a8df0.iam.gserviceaccount.com",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
            
            cred = credentials.Certificate(config)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
            return False
    return True

st.title("🏔️ ALTOOR")

if fix_and_connect():
    try:
        # TEST: Veritabanına ulaşmaya çalış
        db.reference('users').get()
        st.success("✅ İMZA KABUL EDİLDİ! Zirveye ulaşıldı.")
        st.balloons()
    except Exception as e:
        st.error(f"İmza Hatası Devam Ediyor: {e}")
