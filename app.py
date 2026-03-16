import streamlit as st
import google.generativeai as genai
import time
import os

st.set_page_config(page_title="מתמלל העל שלי", page_icon="🎙️")
st.title("🎙️ מתמלל הקבצים המקצועי")
st.write("מכיוון שיוטיוב חוסמת לינקים, כאן פשוט מעלים את הקובץ וזה עובד 100%!")

# חיבור ל-API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("חסר מפתח API ב-Secrets!")

# תיבת העלאת קובץ
uploaded_file = st.file_uploader("בחר קובץ וידאו או אודיו (MP3, MP4, WAV)", type=['mp3', 'mp4', 'wav', 'm4a'])

if uploaded_file is not None:
    if st.button("התחל תמלול קסום! ✨"):
        try:
            with st.spinner("מעלה את הקובץ ל-Gemini..."):
                # שמירה זמנית של הקובץ אצלנו כדי לשלוח לגוגל
                with open("temp_file", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # שליחה לגוגל
                google_file = genai.upload_file(path="temp_file")
                
                # המתנה לעיבוד
                while google_file.state.name == "PROCESSING":
                    time.sleep(2)
                    google_file = genai.get_file(google_file.name)
                
                st.info("הקובץ מוכן! Gemini מתחיל לתמלל...")

                # הפרומפט שלך
                system_prompt = """
                כאן תדביק את ה-System Instructions שלך מ-AI Studio.
                להשתמש ב-3 מירכאות!
                """
                
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([google_file, system_prompt])
                
                st.success("הנה התמלול המלא:")
                st.markdown("---")
                st.write(response.text)
                
                # ניקיון
                genai.delete_file(google_file.name)
                os.remove("temp_file")
                
        except Exception as e:
            st.error(f"קרתה תקלה: {e}")
