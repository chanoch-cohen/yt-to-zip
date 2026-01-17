import streamlit as st
import yt_dlp
import zipfile
import os

st.write("YouTube Downloader & Zipper (Server-Side)")

url = st.text_input("Paste YouTube URL here and press Enter:")

if url:
    video_filename = "downloaded_video.mp4"
    zip_filename = "video_archive.zip"
    cookie_file = "cookies.txt" # שם הקובץ שהעלית לגיטהאב

    ydl_opts = {
        # מחפש קובץ MP4 מוכן כדי לא להסתבך עם חיבורים
        'format': 'best[ext=mp4]/best', 
        'outtmpl': video_filename,
        'quiet': False, # שיניתי ל-False כדי שתוכל לראות לוגים בשרת אם זה נכשל
        'nocheckcertificate': True,
        'cookiefile': cookie_file,
        # הגדרות לעקיפת החידה של יוטיוב
        'extract_flat': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Connection': 'keep-alive',
        }
    }

    try:
        st.write("🔄 Downloading to server...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        st.write("📦 Zipping file...")
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(video_filename)

        with open(zip_filename, "rb") as fp:
            st.download_button(
                label="Click here to download ZIP to your PC",
                data=fp,
                file_name="video_archive.zip",
                mime="application/zip"
            )
        
        st.success("Ready! Click the button above.")

    except Exception as e:
        st.error(f"Error: {e}")

    # ניקוי קבצים מהשרת
    if os.path.exists(video_filename):
        os.remove(video_filename)