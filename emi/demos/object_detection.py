import logging
import time

import cv2
import numpy

from emi.bot.vision import Yolo, YoloDetection
from emi.primitives import Color, Rectangle
from emi.settings import Settings
from emi.windows import Window


class ObjectDetection:
    @classmethod
    def run(cls) -> None:
        logging.getLogger("DETECTION")

        window = Window(Settings.game.name)

        while True:
            start_time = time.time()

            frame = window.update()
            detections = Yolo.detect_objects(frame)
            for detection in detections:
                cls.__render(frame, detection)

            end_time = time.time()
            fps = round(1 / (end_time - start_time), 1)
            cls.__render_text(frame, f"FPS={fps}", cls.__bottom_left_corner(frame))

            cv2.imshow("YOLOv5 detections", frame)
            cv2.waitKey(1)

    @classmethod
    def __render(cls, on_frame: numpy.ndarray, detection: YoloDetection) -> None:
        if detection.confidence <= Settings.yolo.min_confidence:
            return

        first_point, second_point = cls.__rectangle_as_screen_points(detection.bounding_box)
        label = Yolo.label(detection.label_id) or ""
        cls.__render_rectangle(on_frame, first_point, second_point)
        cls.__render_text(on_frame, label, first_point)

    @classmethod
    def __rectangle_as_screen_points(cls, bounding_box: Rectangle) -> tuple[tuple[int, int], tuple[int, int]]:
        x1, y1, x2, y2 = bounding_box.as_tuple
        return (int(x1), int(y1)), (int(x2), int(y2))

    @classmethod
    def __render_rectangle(
            cls, on_frame: numpy.ndarray, first_point: tuple[int, int], second_point: tuple[int, int]
    ) -> None:
        color = Color(r=0, g=255, b=0).as_tuple
        thickness = 5
        cv2.rectangle(on_frame, first_point, second_point, color, thickness)

    @classmethod
    def __render_text(cls, on_frame: numpy.ndarray, text: str, bottom_left_corner: tuple[int, int]) -> None:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = Color(r=0, g=0, b=0).as_tuple
        thickness = 3
        cv2.putText(on_frame, text, bottom_left_corner, font, font_scale, color, thickness)

    @classmethod
    def __bottom_left_corner(cls, image: numpy.ndarray) -> tuple[int, int]:
        height = image.shape[0]
        return 0, height - 5
