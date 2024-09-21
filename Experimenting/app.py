import streamlit as st
import cv2
import os
from streamlit_drawable_canvas import st_canvas

st.title("Bird Detection and Tracking")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    video_path = os.path.join("videos", uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    video_player = st.video(video_path)

    if st.button("Start Video"):
        video_player.play()

    if st.button("Stop Video"):
        video_player.stop()

    if st.button("Show Frames"):
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            st.title("Frame Annotation Tool")
            canvas_result = st_canvas(
                width=600, 
                height=400, 
                drawing_mode="rect", 
                stroke_width=2, 
                stroke_color="rgba(255, 0, 0, 1)", 
                fill_color="rgba(255, 255, 255, 0)", 
                background_image=frame if ret else None, 
                key="canvas",
            )

            if canvas_result.json_data is not None:
                bounding_boxes = canvas_result.json_data['objects']
                st.write("Bounding Boxes:", bounding_boxes)
