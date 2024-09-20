# make a streamlit app to show the recorded video from the folder and then on clicking it show the frames to annotate the bounding boxes for the birds

import streamlit as st
import cv2
import os
from streamlit_drawable_canvas import st_canvas

# Set the title of the Streamlit app
st.title("Bird Detection and Tracking")

# Create a file uploader widget
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Read the video file
    video_path = os.path.join("videos", uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Read the video file
    cap = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create a video player widget
    video_player = st.video(video_path)

    # Create a button to start the video
    if st.button("Start Video"):
        video_player.play()

    # Create a button to stop the video
    if st.button("Stop Video"):
        video_player.stop()

    # Create a button to show the frames
    if st.button("Show Frames"):
        # Capture a frame from the video
        ret, frame = cap.read()
        if ret:
            # Convert the frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Set up the canvas
            st.title("Frame Annotation Tool")
            canvas_result = st_canvas(
                width=600,  # Width of the canvas
                height=400,  # Height of the canvas
                drawing_mode="rect",  # Rectangle mode for bounding boxes
                stroke_width=2,  # Width of the bounding box lines
                stroke_color="rgba(255, 0, 0, 1)",  # Red bounding box
                fill_color="rgba(255, 255, 255, 0)",  # Transparent fill
                background_image=frame if ret else None,  # Initial drawing on the canvas
                key="canvas",
            )

            # Get bounding box data
            if canvas_result.json_data is not None:
                bounding_boxes = canvas_result.json_data['objects']
                st.write("Bounding Boxes:", bounding_boxes)
