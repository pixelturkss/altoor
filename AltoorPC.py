import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import hashlib
from datetime import datetime

# Önceki tüm denemeleri hafızadan sil
st.cache_resource.clear()

@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            # Secrets'ı sözlük olarak al
            cred_dict = dict(st.secrets["firebase"])
            
            # ANAHTARDAKİ GİZLİ HATALARI TEMİZLE
            # Bu satır, kopyalama sırasında oluşabilecek \n hatalarını onarır
            if "private_key" in cred_dict:
                pk = cred_dict["private_key"]
                # Eğer kullanıcı tırnakları yanlış koyduysa düzelt
                pk = pk.replace("\\n", "\n").replace('\\n', '\n')
                cred_dict["private_key"] = pk
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
            return False
    return True

# ARAYÜZ
st.title("🏔️ ALTOOR")

if init_firebase():
    st.success("Sistem hazır!")
    # Uygulama kodları buraya...
