# python video_rec.py

import cv2

# Open the default camera (usually the first available camera, index 0)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break
    
    # Write the frame to the output video file
    out.write(frame)
    
    # Display the resulting frame
    cv2.imshow('Webcam Recording', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
out.release()
cv2.destroyAllWindows()