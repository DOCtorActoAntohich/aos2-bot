import cv2
import numpy

from emi.bot.vision.arena_vision_model import Yolo


class ArenaData:
    def __init__(self, colored_frame: numpy.ndarray) -> None:
        self.frame = colored_frame

        img = colored_frame.copy()
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = cv2.resize(img, Settings.yolo.train_image_sizes)
        # img = numpy.transpose(img, (2, 0, 1))
        img = numpy.array(img, dtype=numpy.float32) / 255.0
        results = Yolo.model(img)

        # labels = results.xyxyn[0][:, -1].cpu().numpy()
        # cord = results.xyxyn[0][:, :-1].cpu().numpy()
        out = colored_frame.copy()
        # n = len(labels)
        # cv2.rectangle(out, (10, 10), (50, 50), (0, 255, 0))
        results = results.pandas().xyxy[0]
        for _, result in results.iterrows():
            print(result)
            label = result['name']
            confidence = result['confidence']
            bbox = result[['xmin', 'ymin', 'xmax', 'ymax']].values
        # for i in range(n):
        #     print(f"iter {i}")
        #     row = cord[i]
        #     print(row[4])
        #     if row[4] >= 0.65:
        #         x1, y1, x2, y2 = int(row[0] * 1366), int(row[1] * 768), int(row[2] * 1366), int(row[3] * 768)
        #         bgr = (0, 255, 0)
        #         cv2.rectangle(out, (x1, y1), (x2, y2), bgr, 2)
        #         cv2.putText(out, Yolo.labels[int(labels[i])], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        self.__processed_screenshot = out

    def show(self) -> None:
        cv2.imshow("YOLOv5", self.__processed_screenshot)
