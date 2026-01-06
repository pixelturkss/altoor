import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
import hashlib
from datetime import datetime

# FIREBASE ANAHTARI (DOĞRUDAN KODUN İÇİNDE)
firebase_dict = {
  "type": "service_account",
  "project_id": "altoor-a8df0",
  "private_key_id": "ca77f9ba4f9e35430ced92d4687cd13403b3022f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDKWybUBcmndHaV\nw+jRmNMzQ9czGlUTVUWoQq8mysAhLaow2YOYf7iQhhiem0C18ya/FjXysALKXuVi\npUgYMoKvjplz0ITRUYeIyK1s8reCkCT3Q4V1dAK2UnuD4kNPju994vpkB0ZKudw+\nCzfryc4EUMu8rwiOuGFwTGjOhxQijpliJo7xMmiaOnp6lq6GXj1zykIGw4BbWc7A\nB+eBs9NMjV284n5CRP1pU8/X0OJ1gzwKWErMDaW+pvXAvkNsmOCLL6zJPNPFteLY\n5N9QCqY0dhlcF2s06ZiDX9NtK+GZXM8iqJujWAKHo++9zntkVihNJdB4dUmSshVu\nD3pjgkn3AgMBAAECggEAGVZcgEPRQiR1DL+hEU1/dHXUJlPvvyH4PN9MqyDL+duL\n6d3yek/TvlTsFEAAVEgD2/1d9+tODiTfuABWDKGWd4D1eejsGIGK5Perr26cx75g\nwo0z0scZ59ZgHN1h7D5Lgom/LHM0u/qVtzcUY3O7VhL/z7pi6evwV21Z2jJTtRfI\n3uctJV6adGUgXqeRoAW8YYl/LkxKUQiPXOIcKjYpBhwTqJBV3aWlLFjog1RHU6WK\n+7vekQEKZ4y6xC4IwVqr9RsJPOCQNWB/pcdub96+OlmqT5XLrd4RQaWTaH6i9PM1\n91drQiJfjv9Vx7+4kLV6NqfUicyQ7oK3OwaRhXIv8QKBgQDn1n28TJ3WMgAb71Fh\nLTey059Rjgx2f1FaMu1hc4ZSyuN2BE+i977EnepB1kgyjRAVCr4eviBw+Nja5vaF\nb6IE6/LYSOIrgnzsxSJa6DebSsBT+qiniaHuNc4nuFncs38xFjCpeuI3NQR+0XfL\nEOwsllZkf5sqY4FGHvcsjgmOdQKBgQDfchOjhNR329siF3h0uzDC7VomEufPmu3s\n/N3YN6jAs2tU86kOJGrOOhh6mCB4QWVIBvAkCnHfdmfFGAYbOREloKREgAxh0oSc\nyJrEEY9Xv1konARIJATeiQECjkKID8nvVH1a/is+ZVAdaDR8xodHhJUL9dKcn7Jo\nrhBc7sABOwKBgCpndfoB/YCXBqQVYsombiCcSnCtTaRC50tbM0X2zmPITlBgu3ww\nWkk2JQnDutLcMEvY+is/VUm0il2HjyGa6ISD75gVxKB2rojUCdOc08bopkL1/vEd\n4Gtklf933Z/biPEegOoO2t+EJ/1WLNYMk1YYbVbWbDgVmSiNM2KH3EGdAoGAJ0YG\nu6P6MEL9ZiWX73SDYo+TW8PQ6MWDcjcTyxAlYhFnGRxmp2yxNSQy70FT268q3RkT\nFlKbpzpJjPPnBtvl7qYomT2kb4Ev+9qqkTHA7xxb0G5ztjZWgMK14bwdZ4rW5HEG\nQ3sPIL1v8mtBZnkCiAh+pgaECTFsi0ek6qCwMMcCgYBUIlTHrUmfs0pfDSwyuy+F\nfDNn2YfJM/Ravov6pcEiIsjNT8n2N25YM1F+YLgL08NilBrkrcwkJlPjbBwq2G+Z\nhJC64Mf06DborWYnoIGJ3DzVp4cNj8N2iStPjHkdoC6kHst2hCnDLx67QhoBRUs6\nOfaJcstLoFd4E2nymQruRA==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@altoor-a8df0.iam.gserviceaccount.com",
  "client_id": "101980292881823607852",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40altoor-a8df0.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# FIREBASE BAĞLANTISI
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(firebase_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
            return False
    return True

# ANA PROGRAM
if init_firebase():
    st.title("🏔️ ALTOOR")
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
        with tab1:
            u = st.text_input("Kullanıcı Adı", key="l_u")
            p = st.text_input("Şifre", type="password", key="l_p")
            if st.button("Giriş"):
                h = hashlib.sha256(p.encode()).hexdigest()
                user = db.reference(f'users/{u}').get()
                if user and user.get('pw') == h:
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()
                else:
                    st.error("Kullanıcı adı veya şifre yanlış!")
        with tab2:
            nu = st.text_input("Yeni Kullanıcı", key="r_u")
            np = st.text_input("Yeni Şifre", type="password", key="r_p")
            if st.button("Kayıt Ol"):
                if nu and np:
                    nh = hashlib.sha256(np.encode()).hexdigest()
                    db.reference(f'users/{nu}').set({"pw": nh})
                    st.success("Kayıt başarılı! Şimdi giriş yapabilirsin.")

    else:
        st.write(f"Zirvedesin @{st.session_state.user}")
        if st.button("Çıkış Yap"):
            st.session_state.logged_in = False
            st.rerun()
            
        txt = st.text_area("Ne düşünüyorsun?")
        if st.button("Gönder"):
            if txt:
                db.reference('posts').push({
                    "u": st.session_state.user,
                    "t": txt,
                    "h": datetime.now().strftime("%H:%M")
                })
                st.rerun()
        
        st.divider()
        posts = db.reference('posts').get()
        if posts:
            for pid in reversed(list(posts.keys())):
                p = posts[pid]
                st.info(f"@{p['u']}: {p['t']}")
