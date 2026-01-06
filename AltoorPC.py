import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import hashlib
from datetime import datetime

# --- FIREBASE BAĞLANTISI (ÇALIŞAN SİSTEMİN) ---
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets["firebase"])
            # Anahtardaki olası karakter hatalarını onarır
            if "private_key" in cred_dict:
                cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n").replace('\\n', '\n')
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
            return False
    return True

# --- UYGULAMA AYARLARI ---
st.set_page_config(page_title="Altoor", page_icon="🏔️")

if init_firebase():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # --- GİRİŞ VE KAYIT EKRANI ---
    if not st.session_state.logged_in:
        st.title("🏔️ ALTOOR")
        st.subheader("Sosyal Medyanın Zirvesi")
        
        tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
        
        with tab1:
            u = st.text_input("Kullanıcı Adı", key="l_u").lower().strip()
            p = st.text_input("Şifre", type="password", key="l_p")
            if st.button("Giriş"):
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
            nu = st.text_input("Yeni Kullanıcı", key="r_u").lower().strip()
            np = st.text_input("Yeni Şifre", type="password", key="r_p")
            if st.button("Zirveye Katıl"):
                if nu and np:
                    check = db.reference(f'users/{nu}').get()
                    if check:
                        st.warning("Bu kullanıcı adı zaten alınmış!")
                    else:
                        nh = hashlib.sha256(np.encode()).hexdigest()
                        db.reference(f'users/{nu}').set({"pw": nh})
                        st.success("Kayıt Başarılı! Şimdi Giriş sekmesine geçebilirsin.")

    # --- SOSYAL MEDYA AKIŞI ---
    else:
        st.sidebar.title(f"🏔️ @{st.session_state.user}")
        if st.sidebar.button("Güvenli Çıkış"):
            st.session_state.logged_in = False
            st.rerun()

        st.title("🏔️ Zirve Akışı")
        
        # Mesaj Gönderme
        with st.form("mesaj_form", clear_on_submit=True):
            mesaj = st.text_area("Zirvedekilere ne söylemek istersin?", max_chars=280)
            if st.form_submit_button("Paylaş"):
                if mesaj:
                    db.reference('posts').push({
                        "u": st.session_state.user,
                        "t": mesaj,
                        "h": datetime.now().strftime("%d/%m %H:%M")
                    })
                    st.rerun()

        st.divider()

        # Mesajları Firebase'den Çek
        posts = db.reference('posts').get()
        if posts:
            # Postları sözlükten listeye çevirip ters çevir (en yeni üstte)
            for pid in reversed(list(posts.keys())):
                p = posts[pid]
                with st.container():
                    st.markdown(f"**@{p['u']}**")
                    st.write(p['t'])
                    st.caption(f"🕒 {p['h']}")
                    st.divider()
        else:
            st.info("Henüz kimse bir şey yazmamış. İlk mesajı sen at!")
