from ultralytics import YOLO
import numpy as np
from shapely import box, intersects, Polygon
import cv2
from ultralytics.utils.plotting import Annotator


model = YOLO("yolov8m.pt")
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
        self.is_car = False


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
        results_ = results[0].plot()
        lane1 = Lane(
            np.array([[100, 200],
                      [200, 200],
                      [200, 100],
                      [100, 100]],
                     np.int32),
            (0, 0, 255)
        )
        lane2 = Lane(
            np.array([[300, 400],
                      [400, 400],
                      [400, 300],
                      [300, 300]],
                     np.int32),
            (0, 0, 255)
        )
        lane3 = Lane(
            np.array([[250, 150],
                      [250, 250],
                      [150, 250],
                      [150, 150]],
                     np.int32),
            (0, 0, 255)
        )

        lanes = [lane1, lane2, lane3]

        # lanes = [
        #     np.array([[100, 200],
        #               [200, 200],
        #               [200, 100],
        #               [100, 100]],
        #              np.int32),
        #     np.array([[300, 400],
        #               [400, 400],
        #               [400, 300],
        #               [300, 300]],
        #              np.int32),
        #     np.array([[250, 150],
        #               [250, 250],
        #               [150, 250],
        #               [150, 150]],
        #              np.int32),
        # ]

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
