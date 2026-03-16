import streamlit as st
import google.generativeai as genai

# כותרת יפה לאתר
st.set_page_config(page_title="מתמלל היוטיוב שלי", page_icon="🎥")
st.title("🎥 מתמלל היוטיוב הקסום")

# חיבור למפתח הסודי
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("אופס! חסר המפתח הסודי (API Key) בהגדרות של Streamlit")

# כאן שמנו את השם המלא והמדויק של המודל
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash"
)

# תיבת טקסט למשתמש
video_url = st.text_input("הדבק כאן לינק ליוטיוב (URL):", placeholder="https://www.youtube.com/watch?v=...")

if st.button("התחל תמלול! ✨"):
    if video_url:
        with st.spinner("הרובוט בדרך ליוטיוב, מיד מתחיל לכתוב..."):
            try:
                # הוספנו הנחיה קטנה למודל שיבין שמדובר בלינק
                prompt = f"Please transcribe this YouTube video: {video_url}. If you can't access it directly, explain what you see."
                
                response = model.generate_content(prompt)
                
                st.success("סיימתי! הנה התוצאה:")
                st.markdown("---")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"קרתה תקלה קטנה: {e}")
    else:
        st.warning("בבקשה שים לינק כדי שאוכל להתחיל.")
