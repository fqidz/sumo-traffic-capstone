from ultralytics import YOLO
import numpy as np
from shapely import box, intersects, Polygon
import cv2
from ultralytics.utils.plotting import Annotator


model = YOLO("yolov8m.pt")
cap = cv2.VideoCapture("/home/faidz-arante/Videos/2024-04-03_13-55-00.mkv")

def get_bounding_boxes(results, frame):
    annotator = Annotator(frame)
    bounding_boxes = []
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # get box coordinates in (left, top, right, bottom) format
            b = box.xyxy[0]
            c = box.cls
            if box.id:
                i = box.id.item()
            else:
                i = None

            annotator.box_label(b, f'{model.names[int(c)]} id: {i}')
            bounding_boxes.append(b)

    return annotator.result(), bounding_boxes


# def capture_mouse_xy(event, x, y, flags, param):
#     global mouseX, mouseY
#     if event == cv2.EVENT_LBUTTONDBLCLK:

#         mouseX, mouseY = x, y
#
#
# cv2.namedWindow('car')
# cv2.setMouseCallback('car', capture_mouse_xy)
class Lane:
    def __init__(self, points, color) -> None:
        self.points = points
        self.color = color


while cap.isOpened():
    success, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))

    if success:
        results = model.track(
            data="dataset/test2/data.yaml",
            source=frame,
            persist=True,
            conf=0.3,
            save=False,
            tracker="bytetrack.yaml",
            classes=[2, 3, 5, 7],
        )
        results_ = results[0].plot()
        lane1 = Lane(
            np.array([[215, 260],
                      [279, 257],
                      [304, 326],
                      [234, 337]],
                     np.int32),
            (0, 0, 255)
        )
        lane2 = Lane(
            np.array([[308, 248],
                      [370, 246],
                      [414, 316],
                      [351, 322]],
                     np.int32),
            (0, 0, 255)
        )
        lane3 = Lane(
            np.array([[420, 241],
                      [473, 231],
                      [537, 286],
                      [468, 302]],
                     np.int32),
            (0, 0, 255)
        )

        lanes = [lane1, lane2, lane3]

        img, boxes = get_bounding_boxes(results, frame)

        for i in boxes:
            coord = i.tolist()
            bounding_box = box(coord[0], coord[1], coord[2], coord[3])
            for lane in lanes:
                lane_poly = Polygon(lane.points)
                if intersects(bounding_box, lane_poly):
                    lane.color = (0, 255, 0)

        for lane in lanes:
            results_ = cv2.polylines(
                results_, [lane.points], True, lane.color, 2)

        cv2.imshow('car', results_)

        k = cv2.waitKey(20) & 0xFF
        if k == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
