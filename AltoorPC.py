import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64
import json

st.cache_resource.clear()

def connect_to_firebase():
    if not firebase_admin._apps:
        try:
            # Base64 metnini al ve çöz
            b64_str = st.secrets["FIREBASE_BASE64"]
            decoded_bytes = base64.b64decode(b64_str)
            key_dict = json.loads(decoded_bytes)
            
            # Bağlantıyı kur
            cred = credentials.Certificate(key_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Base64 Çözme Hatası: {e}")
            return False
    return True

st.title("🏔️ ALTOOR")

if connect_to_firebase():
    try:
        db.reference('users').get()
        st.success("✅ İNANILMAZ! SİSTEM SONUNDA ÇALIŞTI.")
        st.balloons()
    except Exception as e:
        st.error(f"Hata: {e}")
