import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import hashlib
from datetime import datetime
import os
import json

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Altoor Sosyal Medya", page_icon="🏔️")

# --- FIREBASE BAĞLANTISI ---
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        # GitHub'a yüklediğin dosyanın adının bu olduğundan emin ol
        key_path = "serviceAccountKey.json"
        
        if os.path.exists(key_path):
            try:
                # Dosyayı ham haliyle okuyup Firebase'e veriyoruz
                cred = credentials.Certificate(key_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
                })
                return True
            except Exception as e:
                st.error(f"Anahtar Okuma Hatası: {e}")
                return False
        else:
            st.error("Dosya bulunamadı! Lütfen GitHub'da 'serviceAccountKey.json' olduğundan emin ol.")
            return False
    return True

# --- PROGRAM BAŞLIYOR ---
if init_firebase():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🏔️ ALTOOR")
        tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
        
        with tab1:
            u = st.text_input("Kullanıcı Adı", key="l_u")
            p = st.text_input("Şifre", type="password", key="l_p")
            if st.button("Giriş"):
                h = hashlib.sha256(p.encode()).hexdigest()
                # Hata buradaki 'get()' işleminde oluyordu, şimdi düzelmesi lazım
                user_data = db.reference(f'users/{u}').get()
                if user_data and user_data.get('pw') == h:
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()
                else:
                    st.error("Hatalı kullanıcı veya şifre!")
        
        with tab2:
            nu = st.text_input("Yeni Kullanıcı", key="r_u")
            np = st.text_input("Yeni Şifre", type="password", key="r_p")
            if st.button("Kayıt Ol"):
                if nu and np:
                    nh = hashlib.sha256(np.encode()).hexdigest()
                    db.reference(f'users/{nu}').set({"pw": nh})
                    st.success("Kaydoldun!")
    else:
        st.title(f"Selam @{st.session_state.user}")
        msg = st.text_area("Ne düşünüyorsun?")
        if st.button("Zirveye Gönder"):
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
