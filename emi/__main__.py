import cv2

from emi.window import Window
from emi.settings import Settings


def main():
    window = Window(Settings.game_name)

    while True:
        window.update()
        screenshot = window.last_frame

        cv2.imshow("AoS2 view", screenshot)

        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
