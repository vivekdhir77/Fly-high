from ultralytics import YOLO
import cv2
import numpy as np
from collections import defaultdict
model = YOLO('yolov8n.pt')
results = model.train(data="/Users/vivekdhir77/Desktop/Fly-high/bird detection/data.yaml", epochs=10, imgsz=640, batch=8, lr0=0.01)
