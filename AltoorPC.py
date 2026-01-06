import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import hashlib
from datetime import datetime
import os

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(page_title="Altoor Zirve", page_icon="🏔️", layout="centered")

# 2. GÜVENLİ FIREBASE BAĞLANTISI (DOSYADAN OKUR)
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        # Dosya yolunu garantiye alıyoruz
        path = "serviceAccountKey.json"
        if os.path.exists(path):
            try:
                cred = credentials.Certificate(path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
                })
                return True
            except Exception as e:
                st.error(f"Kimlik Doğrulama Hatası: {e}")
                return False
        else:
            st.error("serviceAccountKey.json dosyası bulunamadı. Lütfen GitHub'a yükleyin.")
            return False
    return True

# 3. UYGULAMA MANTIĞI
if init_firebase():
    # Oturum kontrolü
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🏔️ ALTOOR")
        st.subheader("Zirveye hoş geldin.")
        
        tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
        
        with tab1:
            u = st.text_input("Kullanıcı Adı", key="l_user")
            p = st.text_input("Şifre", type="password", key="l_pass")
            if st.button("Giriş Yap"):
                if u and p:
                    h = hashlib.sha256(p.encode()).hexdigest()
                    user_data = db.reference(f'users/{u}').get()
                    if user_data and user_data.get('pw') == h:
                        st.session_state.logged_in = True
                        st.session_state.user = u
                        st.rerun()
                    else:
                        st.error("Kullanıcı adı veya şifre hatalı!")
        
        with tab2:
            nu = st.text_input("Yeni Kullanıcı Adı", key="r_user")
            np = st.text_input("Yeni Şifre", type="password", key="r_pass")
            if st.button("Hesap Oluştur"):
                if nu and np:
                    nh = hashlib.sha256(np.encode()).hexdigest()
                    db.reference(f'users/{nu}').set({"pw": nh})
                    st.success("Kayıt başarılı! Giriş sekmesine geçebilirsin.")

    else:
        # Ana Akış Ekranı
        st.sidebar.title(f"🏔️ @{st.session_state.user}")
        if st.sidebar.button("Güvenli Çıkış"):
            st.session_state.logged_in = False
            st.rerun()

        st.title("🏔️ Altoor Akış")
        
        # Mesaj Gönderme Alanı
        with st.form("message_form", clear_on_submit=True):
            content = st.text_area("Ne düşünüyorsun?", max_chars=280)
            submitted = st.form_submit_button("Zirveye Gönder")
            if submitted and content:
                db.reference('posts').push({
                    "u": st.session_state.user,
                    "t": content,
                    "h": datetime.now().strftime("%d/%m %H:%M")
                })
                st.rerun()

        st.divider()

        # Mesajları Görüntüleme
        posts = db.reference('posts').get()
        if posts:
            # En son mesajı en üstte göstermek için listeyi ters çeviriyoruz
            for pid in reversed(list(posts.keys())):
                post = posts[pid]
                with st.chat_message("user"):
                    st.write(f"**@{post['u']}**")
                    st.write(post['t'])
                    st.caption(post['h'])
        else:
            st.info("Henüz mesaj yok. İlk adımı sen at!")
