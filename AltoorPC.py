import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import hashlib

# 1. FIREBASE BAĞLANTISI (EN GÜVENLİ YOL)
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            # Secrets içindeki [firebase] bölümünü sözlüğe çevir
            firebase_info = dict(st.secrets["firebase"])
            # ÖNEMLİ: Ters slash hatasını burada kökten çözüyoruz
            firebase_info["private_key"] = firebase_info["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(firebase_info)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
            return False
    return True

# 2. GİRİŞ EKRANI
st.title("🏔️ ALTOOR")
if init_firebase():
    st.success("Zirveye bağlantı sağlandı!")
    # Buraya giriş formunu ekleyebilirsin
