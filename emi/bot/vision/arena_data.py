from pathlib import Path

import cv2
import numpy
import torch


def _read_labels(labels_file: Path) -> list[str]:
    with labels_file.open() as file:
        raw_labels = file.readlines()
    labels = [line.strip() for line in raw_labels]
    return [label for label in labels if label]


model: torch.nn.Module = torch.hub.load("ultralytics/yolov5", "custom", path="model/best.pt")
model.conf = 0.5
model.classes = _read_labels(Path("model/labels.txt"))


class ArenaData:
    def __init__(self, colored_frame: numpy.ndarray) -> None:
        self.frame = colored_frame

        img = cv2.resize(colored_frame, (640, 640))
        tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).float() / 255.0
        model(tensor)

    def show(self) -> None:
        ...
