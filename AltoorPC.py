import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import hashlib
import json

# Sayfa Ayarları
st.set_page_config(page_title="Altoor Web", page_icon="🏔️", layout="centered")

# CSS ile Kutu Tasarımı (Senin istediğin o şık görünüm)
st.markdown("""
    <style>
    .post-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007BFF;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .user-name { color: #007BFF; font-weight: bold; }
    .post-date { color: gray; font-size: 0.8em; float: right; }
    </style>
    """, unsafe_allow_html=True)

# Firebase Bağlantısı (Hata almamak için cache kullanıyoruz)
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        # ÖNEMLİ: Streamlit Cloud'da json dosyasını "Secrets" kısmına koyacağız
        # Şimdilik yerel dosyanı okur:
        try:
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
        except:
            st.error("Firebase dosyası bulunamadı!")

init_firebase()

# --- GİRİŞ SİSTEMİ ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏔️ ALTOOR")
    tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
    
    with tab1:
        u = st.text_input("Kullanıcı Adı", key="login_u")
        p = st.text_input("Şifre", type="password", key="login_p")
        if st.button("Giriş"):
            h = hashlib.sha256(p.encode()).hexdigest()
            user_data = db.reference(f'users/{u}').get()
            if user_data and user_data['pw'] == h:
                st.session_state.logged_in = True
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Hatalı giriş!")
    
    with tab2:
        nu = st.text_input("Yeni Kullanıcı Adı")
        np = st.text_input("Yeni Şifre", type="password")
        if st.button("Kayıt Ol"):
            nh = hashlib.sha256(np.encode()).hexdigest()
            db.reference(f'users/{nu}').set({"pw": nh})
            st.success("Kayıt başarılı, şimdi giriş yapabilirsin!")

# --- ANA AKIŞ ---
else:
    st.sidebar.title(f"Selam, @{st.session_state.user}")
    if st.sidebar.button("Çıkış Yap"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("ALTOOR Akış")
    
    # Mesaj Yazma
    with st.container():
        msg = st.text_input("Zirvede neler oluyor?", placeholder="Bir şeyler yaz...")
        if st.button("Paylaş"):
            if msg:
                db.reference('posts').push({
                    "u": st.session_state.user,
                    "t": msg,
                    "h": datetime.now().strftime("%d.%m %H:%M")
                })
                st.rerun()

    st.divider()

    # Mesajları Listele
    posts = db.reference('posts').get()
    if posts:
        for pid in reversed(list(posts.keys())):
            p = posts[pid]
            st.markdown(f"""
                <div class="post-card">
                    <span class="user-name">@{p['u']}</span>
                    <span class="post-date">{p['h']}</span>
                    <p style="margin-top:10px;">{p['t']}</p>
                </div>
                """, unsafe_allow_html=True)