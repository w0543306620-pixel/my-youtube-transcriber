import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# הגדרות האתר
st.set_page_config(page_title="מתמלל היוטיוב המנצח", page_icon="🎬")
st.title("🎬 מתמלל היוטיוב הקסום")

# חיבור למפתח הסודי
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("חסר מפתח API בהגדרות!")

# פונקציה שמוציאה את המילים מיוטיוב
def get_youtube_transcript(url):
    try:
        video_id = url.split("v=")[1].split("&")[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['he', 'en'])
        return " ".join([i['text'] for i in transcript])
    except Exception as e:
        return None

# הגדרת המודל - השתמשנו בשם הכי בטוח שלו
model = genai.GenerativeModel('gemini-1.5-flash')

# תיבת הלינק
video_url = st.text_input("הדבק כאן לינק ליוטיוב:")

if st.button("תמלל לי בצורה מדהימה! ✨"):
    if video_url:
        with st.spinner("הרובוט מוציא את המילים מהסרטון..."):
            # שלב 1: הוצאת הטקסט הגולמי
            raw_text = get_youtube_transcript(video_url)
            
            if raw_text:
                st.info("הצלחתי להוציא את המילים! עכשיו Gemini הופך אותן למדהימות...")
                # שלב 2: שליחה ל-Gemini עם הפרומפט המקורי שלך
                # כאן תדביק את ה-System Prompt שלך בין המרכאות
                # כאן אנחנו משתמשים ב-3 מירכאות כדי שנוכל לכתוב טקסט ארוך
                system_instruction = """
שלום.
אתה מומחה לתמלול. משכתב כמו שאף אחד אחר לא יודע.
עם ניסיון של למעלה מ 40 שנה, והתמחות בשיעורי תורה.
אתה יודע לתמלל שיעורי תורה עם הבנה עמוקה של ההקשר והפיסוק.
אתה שם לב לפרטי פרטים, אם יש מילה שאתה לא יודע, אתה מנסה להסיק מסקנה לפי ההקשר .
אתה מוציא תחת ידך תמיד קובץ מדהים, מסודר מפוסק ומשוכתב ללא פגם.
אתה שם כותרות, פסיק נקודה וכו' בצורה מדהימה.
אתה גם יודע בסוף השכתוב לכתוב סיכום של דף אחד ובו הרעיון המרכזי עם הנקודות העיקריות של השכתוב.
בנוסף.
אתה מתמלל מילה במילה ולא מדלג על שום מילה.
ולכן בסוף אתה מוציא תחת ידך 2 תוצאות.
הראשונה שהיא שכתוב ועריכה.
והשנייה תמלול מילה במילה בלי לדלג על שום מילה.
כמובן 2 הגרסאות יש כותרות, וסימני פיסוק, ובשניהם יש סיכום בסוף.
האם ברור לך מה עליך לעשות?
ומי אתה?
בנוסף, בתמלול אין צורך בחותמת הזמן
                """
                
                full_prompt = f"{system_instruction}\n\nהנה הטקסט הגולמי, בצע את התמלול: {raw_text}"
                
                response = model.generate_content(full_prompt)
                
                st.success("הנה התמלול המוכן:")
                st.write(response.text)
            else:
                st.error("לא הצלחתי להוציא כתוביות מהסרטון הזה. וודא שיש לו כתוביות ביוטיוב.")
    else:
        st.warning("שכחת לשים לינק!")
