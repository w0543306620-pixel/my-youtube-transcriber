import streamlit as st
import google.generativeai as genai
import yt_dlp
import os
import time

st.set_page_config(page_title="מתמלל על-חלל", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ מתמלל היוטיוב החכם (גרסת העוקף)")

# חיבור ל-API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("חסר מפתח API ב-Secrets!")

# פונקציה להורדת אודיו בצורה חשאית
def download_audio(url):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

model = genai.GenerativeModel('gemini-1.5-flash')

video_url = st.text_input("הדבק לינק ליוטיוב:")

if st.button("תמלל עכשיו!"):
    if video_url:
        audio_file = None
        try:
            with st.spinner("מתחפש לדפדפן ומוריד את הסאונד... זה לוקח רגע..."):
                audio_file = download_audio(video_url)
            
            with st.spinner("שולח את האודיו ל-Gemini לניתוח עמוק..."):
                # העלאת הקובץ לגוגל
                sample_file = genai.upload_file(path=audio_file)
                
                # המתנה קצרה שהקובץ יעובד בגוגל
                while sample_file.state.name == "PROCESSING":
                    time.sleep(2)
                    sample_file = genai.get_file(sample_file.name)

                # כאן הפרומפט המקורי שלך
                system_prompt = """
                תדביק כאן את ה-System Instructions שלך מ-AI Studio.
                תשתמש ב-3 מירכאות כמו שלמדנו!
                """
                
                response = model.generate_content([sample_file, system_prompt])
                
                st.success("הנה התמלול המלא (מבוסס שמיעה):")
                st.markdown("---")
                st.write(response.text)
                
                # מחיקת הקובץ מהשרת של גוגל אחרי הסיום
                genai.delete_file(sample_file.name)

        except Exception as e:
            st.error(f"תקלה במבצע החשאי: {e}")
        
        finally:
            # מחיקת הקובץ הזמני מהמחשב שלנו
            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)
    else:
        st.warning("שים לינק!")
