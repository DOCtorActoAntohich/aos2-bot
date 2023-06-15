from pathlib import Path

from pydantic import BaseSettings


class YoloSettings(BaseSettings):
    repository_name: str = "ultralytics/yolov5"
    weights_path: Path = Path("model/best.pt")
    labels_path: Path = Path("model/labels.txt")
    min_confidence: float = 0.6
    train_image_size: int = 640

    @property
    def train_image_sizes(self) -> tuple[int, int]:
        return self.train_image_size, self.train_image_size
