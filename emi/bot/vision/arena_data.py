import cv2
import numpy

from emi.bot.vision.arena_vision_model import Yolo, YoloDetection
from emi.primitives import Rectangle
from emi.settings import Settings


class ArenaData:
    @classmethod
    def prepare_frame(cls, bgr_frame: numpy.ndarray) -> numpy.ndarray:
        rgb_frame: numpy.ndarray = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        return rgb_frame.astype(numpy.float32)

    def __init__(self, bgr_frame: numpy.ndarray) -> None:
        rgb_frame = self.prepare_frame(bgr_frame)

        self.detections = Yolo.detect_objects(rgb_frame)

        self.rendered = bgr_frame.copy()
        for detection in self.detections:
            self.__render(self.rendered, detection)

    def show(self) -> None:
        cv2.imshow("Detections", self.rendered)

    @classmethod
    def __render(cls, on_frame: numpy.ndarray, detection: YoloDetection) -> None:
        if detection.confidence <= Settings.yolo.min_confidence:
            return

        first_point, second_point = cls.__rectangle_as_screen_points(detection.bounding_box)
        label = Yolo.label(detection.label_id)
        box_color = (0, 255, 0)
        text_color = (0, 0, 0)
        box_thickness = 5
        text_thickness = 3
        font_scale = 1
        cv2.rectangle(on_frame, first_point, second_point, box_color, box_thickness)
        cv2.putText(on_frame, label, first_point, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, text_thickness)

    @classmethod
    def __rectangle_as_screen_points(cls, bounding_box: Rectangle) -> tuple[tuple[int, int], tuple[int, int]]:
        x1, y1, x2, y2 = bounding_box.as_tuple
        return (int(x1), int(y1)), (int(x2), int(y2))
