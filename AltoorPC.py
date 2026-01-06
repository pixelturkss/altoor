import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
import hashlib
from datetime import datetime

# FIREBASE BAĞLANTISI (SADECE SECRETS KULLANIR)
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            # Burası Streamlit Secrets kutusundaki "firebase_json"u okur
            secret_content = st.secrets["firebase_json"]
            info = json.loads(secret_content)
            cred = credentials.Certificate(info)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
            return False
    return True

# UYGULAMAYI BAŞLAT
if init_firebase():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🏔️ ALTOOR")
        u = st.text_input("Kullanıcı Adı")
        p = st.text_input("Şifre", type="password")
        if st.button("Giriş Yap"):
            h = hashlib.sha256(p.encode()).hexdigest()
            user_data = db.reference(f'users/{u}').get()
            if user_data and user_data['pw'] == h:
                st.session_state.logged_in = True
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Hatalı giriş!")
    else:
        st.title(f"Selam @{st.session_state.user}")
        msg = st.text_area("Mesajın...")
        if st.button("Paylaş"):
            if msg:
                db.reference('posts').push({
                    "u": st.session_state.user,
                    "t": msg,
                    "h": datetime.now().strftime("%H:%M")
                })
                st.rerun()
        
        # Mesajları Listele
        posts = db.reference('posts').get()
        if posts:
            for pid in reversed(list(posts.keys())):
                p = posts[pid]
                st.info(f"@{p['u']}: {p['t']}")
