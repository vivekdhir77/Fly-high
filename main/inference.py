import cv2
from ultralytics import YOLO

# Initialize the YOLO model
model = YOLO('yolov8n.pt')

# Open the video file or capture device
cap = cv2.VideoCapture("/Users/vivekdhir77/Desktop/Fly-high/birds.mp4") 

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Get the boxes and scores
        boxes = results[0].boxes.xywh.cpu()
        print(boxes)
        scores = results[0].boxes.conf.cpu()

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Process detected objects
        if results[0].boxes.id is not None:
            track_ids = results[0].boxes.id.int().cpu().tolist()
            for box, track_id, score in zip(boxes, track_ids, scores):
                x, y, w, h = box
                cv2.putText(annotated_frame, f"ID: {track_id}, Conf: {score:.2f}", 
                            (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            for box, score in zip(boxes, scores):
                x, y, w, h = box
                cv2.putText(annotated_frame, f"Conf: {score:.2f}", 
                            (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()