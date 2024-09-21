import cv2
from ultralytics import YOLO
import logging
logging.getLogger("ultralytics").setLevel(logging.ERROR)
import numpy as np
import time
from direction import direction

model = YOLO('yolov8n.pt')

cap = cv2.VideoCapture("./birds.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)

start_time = time.time()
centroids = []
overall_centroids_counts_directions = []
frame_count = 0
last_overall_centroid = None

while cap.isOpened():
    success, frame = cap.read()

    if success:
        frame_count += 1
        
        results = model.track(frame, persist=True)

        boxes = results[0].boxes.xywh.cpu().numpy()

        if len(boxes) > 0:
            frame_centroids = boxes[:, :2] + boxes[:, 2:4] / 2
            centroids.append(frame_centroids)

        bird_count = len(boxes)

        elapsed_time = time.time() - start_time
        if frame_count == 1 or elapsed_time >= 3:
            if centroids:
                all_centroids = np.concatenate(centroids)
                overall_centroid = np.mean(all_centroids, axis=0)
                
                if last_overall_centroid is not None:
                    current_direction = direction(overall_centroid, last_overall_centroid)
                else:
                    current_direction = None
                
                overall_centroids_counts_directions.append((overall_centroid, bird_count, current_direction))
                print(f"Frame {frame_count}: Overall centroid: {overall_centroid}, Bird count: {bird_count}, Direction: {current_direction}")
                
                last_overall_centroid = overall_centroid
            
            start_time = time.time()
            centroids = []

        annotated_frame = results[0].plot()

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

        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()

print("Overall centroids, bird counts, and directions:")
for centroid, count, dir in overall_centroids_counts_directions:
    print(f"Centroid: {centroid}, Bird count: {count}, Direction: {dir}")