import numpy

from emi.bot.vision.arena_vision_model import Yolo


class ArenaData:
    def __init__(self, colored_frame: numpy.ndarray) -> None:
        self.detections = Yolo.detect_objects(colored_frame)
