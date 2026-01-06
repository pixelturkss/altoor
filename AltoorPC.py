import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import hashlib
from datetime import datetime
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Altoor Sosyal Medya", page_icon="🏔️", layout="centered")

# --- CSS: ARAYÜZÜ GÜZELLEŞTİRELİM ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    .message-box { padding: 20px; border-radius: 15px; background-color: white; border-left: 5px solid #007bff; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- FIREBASE BAĞLANTISI ---
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        path = "serviceAccountKey.json"
        if os.path.exists(path):
            try:
                cred = credentials.Certificate(path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
                })
                return True
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")
                return False
        else:
            st.error("serviceAccountKey.json bulunamadı! Lütfen GitHub'a yükle.")
            return False
    return True

# --- ANA PROGRAM ---
if init_firebase():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # --- GİRİŞ / KAYIT EKRANI ---
    if not st.session_state.logged_in:
        st.title("🏔️ ALTOOR")
        st.write("Sosyal Medyanın Zirvesi")
        
        tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
        
        with tab1:
            u = st.text_input("Kullanıcı Adı", key="login_u")
            p = st.text_input("Şifre", type="password", key="login_p")
            if st.button("Giriş"):
                h = hashlib.sha256(p.encode()).hexdigest()
                user_data = db.reference(f'users/{u}').get()
                if user_data and user_data.get('pw') == h:
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()
                else:
                    st.error("Kullanıcı adı veya şifre yanlış!")
        
        with tab2:
            nu = st.text_input("Yeni Kullanıcı Adı", key="reg_u")
            np = st.text_input("Yeni Şifre", type="password", key="reg_p")
            if st.button("Hesap Oluştur"):
                if nu and np:
                    # Kullanıcı zaten var mı kontrolü
                    check_user = db.reference(f'users/{nu}').get()
                    if check_user:
                        st.warning("Bu kullanıcı adı alınmış.")
                    else:
                        nh = hashlib.sha256(np.encode()).hexdigest()
                        db.reference(f'users/{nu}').set({"pw": nh})
                        st.success("Kayıt başarılı! Giriş yapabilirsin.")

    # --- SOSYAL MEDYA AKIŞI ---
    else:
        # Üst Bar
        col1, col2 = st.columns([4, 1])
        with col1:
            st.title(f"🏔️ Hoş geldin @{st.session_state.user}")
        with col2:
            if st.button("Çıkış"):
                st.session_state.logged_in = False
                st.rerun()

        # Mesaj Paylaşma Alanı
        with st.container():
            msg = st.text_area("Ne düşünüyorsun?", placeholder="Zirveye bir not bırak...", max_chars=280)
            if st.button("Zirveye Gönder"):
                if msg:
                    db.reference('posts').push({
                        "u": st.session_state.user,
                        "t": msg,
                        "h": datetime.now().strftime("%d/%m %H:%M")
                    })
                    st.rerun()
                else:
                    st.warning("Boş mesaj gönderilemez.")

        st.divider()

        # Akış (Mesajları Listeleme)
        st.subheader("Son Paylaşımlar")
        posts = db.reference('posts').get()
        
        if posts:
            # Postları zaman sırasına göre ters çevir (en yeni en üstte)
            for pid in reversed(list(posts.keys())):
                p = posts[pid]
                st.markdown(f"""
                <div class="message-box">
                    <b style="color:#007bff;">@{p['u']}</b> <small style="float:right; color:gray;">{p['h']}</small><br>
                    <p style="margin-top:10px; font-size:18px;">{p['t']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Buralar henüz ıssız... İlk mesajı sen yaz!")
