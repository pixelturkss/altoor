import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import hashlib
from datetime import datetime

# Önbelleği tamamen temizle ki eski hatalı key silinsin
st.cache_resource.clear()

@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            # Doğrudan secrets içindeki sözlüğü kullan
            cred_dict = dict(st.secrets["firebase"])
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
    st.success("BAĞLANDI! Zirveye ulaşıldı.")
    # Giriş formu buraya gelecek...
