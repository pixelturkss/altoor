import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
import hashlib
from datetime import datetime

# FIREBASE BAĞLANTISI (SECRETS ÜZERİNDEN)
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            # Secrets'tan JSON metnini al
            key_dict = json.loads(st.secrets["firebase_json"], strict=False)
            cred = credentials.Certificate(key_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
            return False
    return True

# SOSYAL MEDYA ARAYÜZÜ
if init_firebase():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🏔️ ALTOOR")
        tab1, tab2 = st.tabs(["Giriş", "Kayıt"])
        with tab1:
            u = st.text_input("Kullanıcı")
            p = st.text_input("Şifre", type="password")
            if st.button("Giriş"):
                h = hashlib.sha256(p.encode()).hexdigest()
                user = db.reference(f'users/{u}').get()
                if user and user.get('pw') == h:
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()
                else:
                    st.error("Hatalı!")
        with tab2:
            nu = st.text_input("Yeni Kullanıcı")
            np = st.text_input("Yeni Şifre", type="password")
            if st.button("Kayıt Ol"):
                if nu and np:
                    nh = hashlib.sha256(np.encode()).hexdigest()
                    db.reference(f'users/{nu}').set({"pw": nh})
                    st.success("Kayıt Başarılı!")
    else:
        st.title(f"Zirvedesin @{st.session_state.user}")
        msg = st.text_area("Mesajını yaz...")
        if st.button("Gönder"):
            if msg:
                db.reference('posts').push({
                    "u": st.session_state.user,
                    "t": msg,
                    "h": datetime.now().strftime("%H:%M")
                })
                st.rerun()
        
        posts = db.reference('posts').get()
        if posts:
            for pid in reversed(list(posts.keys())):
                p = posts[pid]
                st.info(f"@{p['u']}: {p['t']}")
