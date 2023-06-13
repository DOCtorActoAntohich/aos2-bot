from __future__ import annotations

from pathlib import Path

import torch

from emi.settings import Settings

__all__ = ("Yolo",)


def _read_labels(labels_file: Path) -> list[str]:
    with labels_file.open() as file:
        raw_labels = file.readlines()
    labels = [line.strip() for line in raw_labels]
    return [label for label in labels if label]


def _create_model(labels: list[str]) -> torch.nn.Module:
    # model: torch.nn.Module = torch.hub.load(Settings.yolo.repository_name, "custom", path=Settings.yolo.weights_path)
    model = torch.hub.load(Settings.yolo.repository_name, "yolov5s")
    model.conf = Settings.yolo.min_confidence_score
    model.classes = labels
    return model


class Yolo:
    labels = _read_labels(Settings.yolo.labels_path)
    model = _create_model(labels)
