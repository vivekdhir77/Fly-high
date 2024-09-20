import cv2
from ultralytics import YOLO
import logging
logging.getLogger("ultralytics").setLevel(logging.ERROR)
import numpy as np
import time
from direction import direction



# Initialize the YOLO model
model = YOLO('yolov8n.pt')

# Open the video file or capture device
cap = cv2.VideoCapture("/Users/sansh/Documents/visual_ai/Fly-high-main/fast_birds.mp4")

# Get video FPS
fps = cap.get(cv2.CAP_PROP_FPS)

# Initialize variables
start_time = time.time()
centroids = []
overall_centroids_counts_directions = []
frame_count = 0
last_overall_centroid = None

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        frame_count += 1
        
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Get the boxes as a numpy array
        boxes = results[0].boxes.xywh.cpu().numpy()

        # Calculate centroids for this frame (vectorized)
        if len(boxes) > 0:
            frame_centroids = boxes[:, :2] + boxes[:, 2:4] / 2
            centroids.append(frame_centroids)

        # Update bird count
        bird_count = len(boxes)

        # Calculate overall centroid and store count every 3 seconds or on the first frame
        elapsed_time = time.time() - start_time
        if frame_count == 1 or elapsed_time >= 3:
            if centroids:
                all_centroids = np.concatenate(centroids)
                overall_centroid = np.mean(all_centroids, axis=0)
                
                # Calculate direction starting from the second interval
                if last_overall_centroid is not None:
                    current_direction = direction(overall_centroid, last_overall_centroid)
                else:
                    current_direction = None
                
                overall_centroids_counts_directions.append((overall_centroid, bird_count, current_direction))
                print(f"Frame {frame_count}: Overall centroid: {overall_centroid}, Bird count: {bird_count}, Direction: {current_direction}")
                
                # Update last_overall_centroid for the next interval
                last_overall_centroid = overall_centroid
            
            # Reset for the next 3-second interval
            start_time = time.time()
            centroids = []

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Process detected objects
        if results[0].boxes.id is not None:
            track_ids = results[0].boxes.id.int().cpu().tolist()
            scores = results[0].boxes.conf.cpu().numpy()
            for box, track_id, score in zip(boxes, track_ids, scores):
                x, y, w, h = box
                cv2.putText(annotated_frame, f"ID: {track_id}, Conf: {score:.2f}", 
                            (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            scores = results[0].boxes.conf.cpu().numpy()
            for box, score in zip(boxes, scores):
                x, y, w, h = box
                cv2.putText(annotated_frame, f"Conf: {score:.2f}", 
                            (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the annotated frame
        # cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        # if cv2.waitKey(1) & 0xFF == ord("q"):
            # break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

print("Overall centroids, bird counts, and directions:")
for centroid, count, dir in overall_centroids_counts_directions:
    print(f"Centroid: {centroid}, Bird count: {count}, Direction: {dir}")