from ultralytics import YOLO
import cv2

model = YOLO("yolov8m.pt")
# results = model.track(source="2", show=True, conf=0.4,
#                       save=False, tracker="bytetrack.yaml", classes=[2, 3, 5, 7])
cap = cv2.VideoCapture(2)

while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model.track(
            source=frame,
            show=True,
            persist=True,
            conf=0.3,
            save=False,
            tracker="bytetrack.yaml",
            classes=[2, 3, 5, 7]
        )
