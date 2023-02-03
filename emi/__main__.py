import cv2

from emi.window import Window
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

    while True:
        environment.render(mode="human")


if __name__ == "__main__":
    try:
        run_environment()
    except KeyboardInterrupt:
        print("Closed forcibly")
