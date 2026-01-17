import streamlit as st
import yt_dlp
import zipfile
import os

# כותרת פשוטה
st.write("YouTube Downloader & Zipper")

# תיבת טקסט לקליטת הקישור
url = st.text_input("Paste YouTube URL here and press Enter:")

if url:
    # הגדרת שם הקבצים
    video_filename = "downloaded_video.mp4"
    zip_filename = "video_archive.zip"

    # --- השינוי נמצא כאן: הגדרות משופרות למניעת חסימות ---
    ydl_opts = {
        'format': 'best',
        'outtmpl': video_filename,
        'quiet': True,
        'nocheckcertificate': True,
        # הוספת כותרות כדי להיראות כמו דפדפן רגיל (Chrome)
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    }

    try:
        st.write("Downloading from YouTube to Server...")
        
        # שלב 1: הורדה מיוטיוב לשרת
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        st.write("Compressing to ZIP...")

        # שלב 2: יצירת קובץ ZIP והכנסת הסרטון לתוכו
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(video_filename)

        # שלב 3: קריאת הקובץ לזיכרון כדי לאפשר הורדה
        with open(zip_filename, "rb") as fp:
            btn = st.download_button(
                label="Download ZIP File",
                data=fp,
                file_name="my_video.zip",
                mime="application/zip"
            )
        
    except Exception as e:
        # הצגת שגיאה למשתמש אם משהו נכשל
        st.error(f"Error: {e}")

    # ניקוי קבצים זמניים (הוידאו המקורי) כדי לא לסתום את השרת
    if os.path.exists(video_filename):
        os.remove(video_filename)