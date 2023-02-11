import time

import cv2

from emi.windows.window import Window
from emi.settings import Settings
from emi.aos2environment import AoS2Environment


def run_screencapture():
    window = Window(Settings.game_name)

    while True:
        window.update()
        screenshot = window.last_frame

        cv2.imshow("AoS2 view", screenshot)

        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break


def run_environment():
    environment = AoS2Environment()
    environment.reset()

    # stupid but i'm testing stuff lol
    i = 0
    while True:
        if i == 120:
            _ = environment.step([0, 0, 0, 1, 0])
        if i == 240:
            _ = environment.step([0, 0, 1, 0, 0])
            i = 0
        environment.render(mode="human")
        i += 1


if __name__ == "__main__":
    try:
        run_environment()
    except KeyboardInterrupt:
        print("Closed forcibly")
