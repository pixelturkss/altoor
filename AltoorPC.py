import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import hashlib
from datetime import datetime

# --- FIREBASE BAĞLANTISI (SENİN ÇALIŞAN YÖNTEMİN) ---
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            firebase_info = dict(st.secrets["firebase"])
            firebase_info["private_key"] = firebase_info["private_key"].replace("\\n", "\n")
            cred = credentials.Certificate(firebase_info)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
            return False
    return True

# --- UYGULAMA MANTIĞI ---
st.set_page_config(page_title="Altoor", page_icon="🏔️")

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
                user_data = db.reference(f'users/{u}').get()
                if user_data and user_data.get('pw') == h:
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()
                else:
                    st.error("Hatalı giriş!")
        
        with tab2:
            nu = st.text_input("Yeni Kullanıcı", key="r_u")
            np = st.text_input("Yeni Şifre", type="password", key="r_p")
            if st.button("Hesap Oluştur"):
                if nu and np:
                    nh = hashlib.sha256(np.encode()).hexdigest()
                    db.reference(f'users/{nu}').set({"pw": nh})
                    st.success("Kayıt Başarılı! Şimdi giriş yapabilirsin.")

    else:
        st.sidebar.title(f"🏔️ @{st.session_state.user}")
        if st.sidebar.button("Çıkış Yap"):
            st.session_state.logged_in = False
            st.rerun()

        st.title("🏔️ Zirve Akışı")
        
        # Mesaj Yazma
        with st.form("msg_form", clear_on_submit=True):
            msg = st.text_area("Ne düşünüyorsun?", max_chars=280)
            if st.form_submit_button("Paylaş"):
                if msg:
                    db.reference('posts').push({
                        "u": st.session_state.user,
                        "t": msg,
                        "h": datetime.now().strftime("%H:%M")
                    })
                    st.rerun()

        st.divider()

        # Mesajları Listeleme
        posts = db.reference('posts').get()
        if posts:
            for pid in reversed(list(posts.keys())):
                p = posts[pid]
                with st.chat_message("user"):
                    st.write(f"**@{p['u']}**")
                    st.write(p['t'])
                    st.caption(p['h'])
