import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import hashlib
from datetime import datetime
import os

# FIREBASE BAĞLANTISI (DOSYADAN OKUMA)
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        # Dosya adı GitHub'dakiyle aynı olmalı
        if os.path.exists("key.json"):
            try:
                cred = credentials.Certificate("key.json")
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
                })
                return True
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")
                return False
        else:
            st.error("key.json dosyası bulunamadı! GitHub'a yüklediğinden emin ol.")
            return False
    return True

# UYGULAMA BAŞLIYOR
if init_firebase():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🏔️ ALTOOR")
        t1, t2 = st.tabs(["Giriş", "Kayıt"])
        with t1:
            u = st.text_input("Kullanıcı")
            p = st.text_input("Şifre", type="password")
            if st.button("Giriş Yap"):
                h = hashlib.sha256(p.encode()).hexdigest()
                res = db.reference(f'users/{u}').get()
                if res and res.get('pw') == h:
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Hatalı!")
        with t2:
            nu = st.text_input("Yeni Kullanıcı")
            np = st.text_input("Yeni Şifre", type="password")
            if st.button("Kayıt Ol"):
                if nu and np:
                    nh = hashlib.sha256(np.encode()).hexdigest()
                    db.reference(f'users/{nu}').set({"pw": nh})
                    st.success("Kayıt Başarılı!")
    else:
        st.title(f"Zirvedesin @{st.session_state.user}")
        if st.button("Çıkış"):
            st.session_state.logged_in = False
            st.rerun()
        
        msg = st.text_area("Mesaj yaz...")
        if st.button("Gönder"):
            if msg:
                db.reference('posts').push({
                    "u": st.session_state.user, "t": msg,
                    "h": datetime.now().strftime("%H:%M")
                })
                st.rerun()
        
        posts = db.reference('posts').get()
        if posts:
            for pid in reversed(list(posts.keys())):
                p = posts[pid]
                st.info(f"@{p['u']}: {p['t']}")
