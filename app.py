import streamlit as st
import google.generativeai as genai

# עיצוב בסיסי
st.set_page_config(page_title="מתמלל היוטיוב שלי")
st.title("🎥 מתמלל היוטיוב הקסום")

# חיבור למפתח
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("חסר מפתח API ב-Secrets!")

# שינינו את השם ל-gemini-1.5-flash (בלי ה-models/ ובלי שטויות)
model = genai.GenerativeModel('gemini-1.5-flash')

video_url = st.text_input("הדבק לינק ליוטיוב:")

if st.button("תמלל עכשיו!"):
    if video_url:
        with st.spinner("מנסה לקרוא את הסרטון..."):
            try:
                # כאן אנחנו מבקשים מהמודל לתמלל
                response = model.generate_content(f"Please transcribe this video: {video_url}")
                st.write(response.text)
            except Exception as e:
                st.error(f"אופס, שגיאה: {e}")
    else:
        st.warning("שכחת לינק!")
