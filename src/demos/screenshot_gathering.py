import logging
import time
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy

from src.settings import Settings
from src.windows import Window

__all__ = ("ScreenshotGathering",)

DatasetPath = Path("dataset/")
ImageExtension = "jpg"
TimeFormat = r"%Y_%m_%d__%H_%M_%S"


class ScreenshotGathering:
    @classmethod
    def run(cls, *, save_to: Path = DatasetPath, seconds_between_shots: int = 5) -> None:
        logger = logging.getLogger("DATASET")

        window = Window(Settings.game.name)
        session_folder = cls.__make_current_session_folder(save_to)

        logger.info(f"Saving screenshots every {seconds_between_shots} second(s)")
        logger.info(f"Find them here: {session_folder}")

        while True:
            cls.__save_screenshot(session_folder, window.frames_processed, window.last_frame)
            logger.info(f"\rScreenshots saved: {window.frames_processed}")

            time.sleep(seconds_between_shots)
            window.update()

    @classmethod
    def __make_current_session_folder(cls, dataset_folder: Path) -> Path:
        time_now = datetime.now(timezone.utc)
        folder_name = time_now.strftime(TimeFormat)

        session_folder = dataset_folder / folder_name
        session_folder.mkdir(parents=True, exist_ok=True)
        return session_folder

    @classmethod
    def __save_screenshot(cls, session_folder: Path, file_index: int, data: numpy.ndarray) -> None:
        file_name = f"{file_index}.{ImageExtension}"
        file_path = session_folder / file_name
        cv2.imwrite(str(file_path), data)
