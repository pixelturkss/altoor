import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import hashlib
import os

# 1. SAYFA AYARLARI VE TASARIM
st.set_page_config(page_title="Altoor Zirve", page_icon="🏔️")

st.markdown("""
    <style>
    .post-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #007BFF;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #1a1a1a;
    }
    .user-name { color: #007BFF; font-weight: bold; font-size: 1.1em; }
    .post-date { color: #888; font-size: 0.8em; float: right; }
    .stButton>button { width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. FIREBASE BAĞLANTISI (HATA KORUMALI)
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        # Önce GitHub'daki dosyayı kontrol et
        json_file = "serviceAccountKey.json"
        
        if os.path.exists(json_file):
            try:
                cred = credentials.Certificate(json_file)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
                })
                return True
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")
                return False
        else:
            st.error("serviceAccountKey.json dosyası GitHub deposunda bulunamadı!")
            return False
    return True

if init_firebase():
    # 3. OTURUM YÖNETİMİ
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🏔️ ALTOOR")
        st.subheader("Zirvedekilerin Sosyal Medyası")
        
        tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
        
        with tab1:
            u = st.text_input("Kullanıcı Adı", key="l_user")
            p = st.text_input("Şifre", type="password", key="l_pass")
            if st.button("Giriş Yap", bootstyle="primary"):
                if u and p:
                    h = hashlib.sha256(p.encode()).hexdigest()
                    user_ref = db.reference(f'users/{u}').get()
                    if user_ref and user_ref.get('pw') == h:
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
                    st.success("Kayıt başarılı! Şimdi giriş yapabilirsin.")

    # 4. ANA AKIŞ EKRANI
    else:
        # Üst Bar
        col1, col2 = st.columns([3, 1])
        col1.title("🏔️ Altoor Akış")
        if col2.button("Çıkış Yap"):
            st.session_state.logged_in = False
            st.rerun()

        # Mesaj Gönderimi
        with st.expander("Yeni Bir Şey Paylaş", expanded=True):
            content = st.text_area("Ne düşünüyorsun?", max_chars=280)
            if st.button("Zirveye Gönder"):
                if content:
                    db.reference('posts').push({
                        "u": st.session_state.user,
                        "t": content,
                        "h": datetime.now().strftime("%d/%m %H:%M")
                    })
                    st.success("Paylaşıldı!")
                    st.rerun()

        st.divider()

        # Mesajları Görüntüle
        try:
            posts = db.reference('posts').get()
            if posts:
                # En yeni mesaj en üstte
                for pid in reversed(list(posts.keys())):
                    post = posts[pid]
                    st.markdown(f"""
                        <div class="post-card">
                            <span class="user-name">@{post['u']}</span>
                            <span class="post-date">{post['h']}</span>
                            <div style="margin-top:15px; font-size:1.1em;">{post['t']}</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Henüz buralar çok sessiz... İlk mesajı sen yaz!")
        except Exception as e:
            st.error("Mesajlar yüklenirken bir sorun oluştu.")

else:
    st.warning("Firebase bağlantısı bekleniyor...")
