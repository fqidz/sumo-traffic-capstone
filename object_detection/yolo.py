from ultralytics import YOLO
import pybboxes as pb
import numpy as np
import cv2
from ultralytics.utils.plotting import Annotator


model = YOLO("yolov8m.pt")
print(model.names)
# results = model.track(
#     data="./dataset/data.yaml",
#     source="2",
#     show=True,
#     persist=True,
#     conf=0.3,
#     save=False,
#     tracker="bytetrack.yaml",
#     classes=[2, 3, 5, 7],
# )
cap = cv2.VideoCapture(2)


def get_bounding_boxes(results, frame):
    annotator = Annotator(frame)
    bounding_boxes = []
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # get box coordinates in (left, top, right, bottom) format
            b = box.xyxy[0]
            c = box.cls

            annotator.box_label(b, model.names[int(c)])
            bounding_boxes.append(b)

    return annotator.result(), bounding_boxes


while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model.track(
            data="./dataset/data.yaml",
            source=frame,
            persist=True,
            conf=0.3,
            save=False,
            tracker="bytetrack.yaml",
            # classes=[2, 3, 5, 7],
        )

        img, boxes = get_bounding_boxes(results, frame)
        lane_1 = np.array([[25, 70], [25, 160],
                           [150, 200], [20, 200]],
                          np.int32)
        lane_1 = lane_1.reshape((-1, 1, 2))

        img = cv2.polylines(img, lane_1, True, (255, 0, 0), 2)

        print(boxes)
        cv2.imshow('car', img)

        if cv2.waitKey(40) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
