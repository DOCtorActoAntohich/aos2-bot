import cv2
import numpy

from emi.bot.vision.arena_vision_model import Yolo


class ArenaData:
    @classmethod
    def prepare_frame(cls, bgr_frame: numpy.ndarray) -> numpy.ndarray:
        rgb_frame: numpy.ndarray = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        return rgb_frame.astype(numpy.float32)

    def __init__(self, bgr_frame: numpy.ndarray) -> None:
        rgb_frame = self.prepare_frame(bgr_frame)

        self.results = Yolo.detect_objects(rgb_frame)

    def show(self) -> None:
        ...
