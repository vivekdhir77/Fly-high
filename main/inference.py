import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

cap = cv2.VideoCapture("/Users/vivekdhir77/Desktop/Fly-high/birds.mp4") 

while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model.track(frame, persist=True)

        boxes = results[0].boxes.xywh.cpu()
        print(boxes)
        scores = results[0].boxes.conf.cpu()

        annotated_frame = results[0].plot()

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

        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()