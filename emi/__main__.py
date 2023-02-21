import cv2

from emi.bot.aos2environment import AoS2Environment


def run_environment():
    environment = AoS2Environment()
    environment.reset()

    while True:
        environment.render(mode="human")


if __name__ == "__main__":
    try:
        run_environment()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        print("Closed forcibly")
