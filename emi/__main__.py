import argparse
import logging

import cv2

from emi.bot.aos2environment import AoS2Environment
from emi.dataset import ScreenshotGathering


def run_environment() -> None:
    environment = AoS2Environment()
    environment.reset()

    while True:
        environment.render(mode="human")


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    arguments = argparse.ArgumentParser()
    arguments.add_argument("--gather-screenshots", action="store_true")

    args = arguments.parse_args()

    if args.gather_screenshots:
        ScreenshotGathering.run(seconds_between_shots=1)
        return

    run_environment()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
