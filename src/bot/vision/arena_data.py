import numpy

from src.bot.vision.arena_vision_model import Yolo, YoloDetection


class ArenaData:
    def __init__(self, colored_frame: numpy.ndarray) -> None:
        self.__detections = Yolo.detect_objects(colored_frame)

    @property
    def detections(self) -> list[YoloDetection]:
        return self.__detections
