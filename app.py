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
        'format': 'best',
        'outtmpl': video_filename,
        'quiet': False,
        'nocheckcertificate': True,
        'cookiefile': cookie_file,
        # הגדרה שאומרת ל-yt-dlp להתחזות לאפליקציית אנדרואיד
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
            }
        },
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