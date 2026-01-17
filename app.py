import streamlit as st
import yt_dlp
import zipfile
import os
import time

# כותרת פשוטה
st.write("YouTube Downloader & Zipper")

# תיבת טקסט לקליטת הקישור
url = st.text_input("Paste YouTube URL here and press Enter:")

if url:
    # הגדרת שם הקבצים
    video_filename = "downloaded_video.mp4"
    zip_filename = "video_archive.zip"

    # הגדרות להורדה עם yt-dlp
    ydl_opts = {
        'format': 'best',  # האיכות הטובה ביותר
        'outtmpl': video_filename,  # שם הקובץ שיישמר בשרת
        'quiet': True
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

        # ניקוי: מחיקת הקבצים מהשרת לאחר יצירת כפתור ההורדה
        # הערה: ב-Streamlit זה טריקי, אז אנחנו מנקים אם הקבצים קיימים מהרצה קודמת
        
    except Exception as e:
        st.error(f"Error: {e}")

    # ניקוי קבצים זמניים כדי לא לסתום את השרת
    if os.path.exists(video_filename):
        os.remove(video_filename)
    # את ה-ZIP אנחנו משאירים עד שהמשתמש מוריד, או שהשרת יתנקה לבד