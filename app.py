## Streamlit UI to drag and drop multiple videos and one audio file to create a video with the audio file as the background music

import streamlit as st
import os
from streamlit.logger import get_logger
from src.app import run

logger = get_logger(__name__)

# Sreamlit UI
st.title("Video Editor")
st.write(
    "Drag and drop multiple videos and one audio file to create a video with the audio file as the background music"
)
st.write(
    "Note: The video files should be in the order you want them to be concatenated"
)
# Upload videos and audio file
uploaded_files = st.file_uploader("Upload your video files", accept_multiple_files=True)
st.write("Note: The audio file should be longer than the video files")
uploaded_audio = st.file_uploader("Upload your audio file", accept_multiple_files=False)

# Create a temporary directory to store the uploaded files
temp_dir = os.path.join(os.getcwd(), "temp")
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)
# Create a temporary directory to store the uploaded files
output_dir = os.path.join(os.getcwd(), "output")
if not os.path.exists(output_dir):
    logger.info("Creating output directory")
    os.mkdir(output_dir)
# Create a temporary directory to store the uploaded files
video_dir = os.path.join(os.getcwd(), "videos")
if not os.path.exists(video_dir):
    logger.info("Creating video directory")
    os.mkdir(video_dir)

# GET paths of all the uploaded videos
video_paths = []
for uploaded_file in uploaded_files:
    with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    video_paths.append(os.path.join(temp_dir, uploaded_file.name))

run(video_paths, os.path.join(temp_dir, uploaded_audio.name))
