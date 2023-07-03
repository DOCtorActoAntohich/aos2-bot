from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import cv2
import numpy
import torch

from src.primitives import Rectangle
from src.settings import Settings

__all__ = ("Yolo", "YoloDetection")


def _create_model() -> torch.nn.Module:
    model: torch.nn.Module = torch.hub.load(
        Settings.yolo.repository_name,
        "custom",
        path=Settings.yolo.weights_path,
    )
    return model


@dataclass
class YoloDetection:
    bounding_box: Rectangle[float]
    confidence: float
    label_id: int

    @classmethod
    def __expected_tensor_length(cls) -> int:
        return 6

    @classmethod
    def from_tensor(cls, tensor: torch.Tensor) -> YoloDetection:
        if len(tensor) != cls.__expected_tensor_length():
            msg = f"Invalid tensor length: {cls.__expected_tensor_length()}"
            raise RuntimeError(msg)

        simpler_tensor: list[float] = [float(i) for i in tensor]
        x1, y1, x2, y2, confidence, label_id = simpler_tensor
        return cls(bounding_box=Rectangle(x1, y1, x2, y2), confidence=confidence, label_id=int(label_id))


class Yolo:
    __model = _create_model()

    @classmethod
    def detect_objects(cls, bgr_image: numpy.ndarray) -> list[YoloDetection]:
        rgb_image = cls.__prepare_frame(bgr_image)
        detections_for_single_image, *_ = cls.__model(rgb_image).pred
        return [YoloDetection.from_tensor(tensor) for tensor in detections_for_single_image]

    @classmethod
    def label(cls, label_id: int) -> str | None:
        return cls.__labels().get(label_id, None)

    @classmethod
    def __labels(cls) -> dict[int, str]:
        return cast(dict[int, str], cls.__model.names)

    @classmethod
    def __prepare_frame(cls, bgr_frame: numpy.ndarray) -> numpy.ndarray:
        rgb_frame: numpy.ndarray = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        return rgb_frame.astype(numpy.float32)
