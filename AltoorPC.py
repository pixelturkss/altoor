import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

st.cache_resource.clear()

def start_firebase():
    if not firebase_admin._apps:
        try:
            # Secrets'tan ham metni al
            raw_pk = st.secrets["firebase"]["private_key"]
            
            # --- CERRAHİ TEMİZLİK OPERASYONU ---
            # 1. Satırları parçala
            lines = raw_pk.split('\n')
            # 2. Her satırın başındaki ve sonundaki gizli boşlukları sil
            clean_lines = [line.strip() for line in lines if line.strip()]
            # 3. Google'ın beklediği formatta (satır sonu karakteriyle) birleştir
            formatted_pk = "\n".join(clean_lines)
            # ----------------------------------

            cred_dict = {
                "type": "service_account",
                "project_id": "altoor-a8df0",
                "private_key_id": "ca77f9ba4f9e35430ced92d4687cd13403b3022f",
                "private_key": formatted_pk,
                "client_email": "firebase-adminsdk-fbsvc@altoor-a8df0.iam.gserviceaccount.com",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://altoor-a8df0-default-rtdb.asia-southeast1.firebasedatabase.app'
            })
            return True
        except Exception as e:
            st.error(f"Başlatma Hatası: {e}")
            return False
    return True

st.title("🏔️ ALTOOR")

if start_firebase():
    try:
        # Kapıyı gerçekten çalalım
        db.reference('users').get()
        st.success("✅ SONUNDA! İmza kabul edildi, içerideyiz.")
        st.balloons()
    except Exception as e:
        st.error(f"Hala İmza Hatası (JWT): {e}")
        st.info("Eğer bu da olmadıysa, tek yol Firebase'den yeni bir JSON alıp kopyalarken asla metin düzenleyiciye (Notepad vb.) yapıştırmadan direkt Secrets'a atmaktır.")
