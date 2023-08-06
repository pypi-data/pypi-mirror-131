import threading

import numpy as np
import cv2

from mobot.brain.agent import Agent

def _do_nothing(x):
    pass


class ImageGrid:
    """Simple wrapper around cv2 high level gui

    Features:
        1. Grid of images of fixed size.
        2. Trackbars
    """

    def __init__(self, agent, name="Image Grid", size=(1,1), image_size=(640,480,3)):
        self.__agent = agent
        self.__name = name

        self.__size = size
        self.__image_size = image_size
        self.__image_grid_size = (self.__image_size[0] * self.__size[0],\
                                  self.__image_size[1] * self.__size[1],\
                                  self.__image_size[2])
        self.__image_grid = np.zeros(self.__image_grid_size, dtype=np.uint8)

        self.__is_start = False
        self.__thread = threading.Thread(target=self.__thread)

        self.__trackbars = []

    def create_trackbar(self, name, default, max, on_change=_do_nothing):
        self.__trackbars.append((name, default, max, on_change))

    def __thread(self):
        cv2.namedWindow(self.__name, cv2.WINDOW_NORMAL)
        for trackbar in self.__trackbars:
            cv2.createTrackbar(trackbar[0], self.__name, trackbar[1], trackbar[2], trackbar[3])
        while self.__agent.ok():
            cv2.imshow(self.__name, np.flip(self.__image_grid, axis=-1))
            cv2.waitKey(100)

    def __start(self):
        self.__is_start = True
        self.__thread.start()

    def new_image(self, image, index=(0,0)):
        if not self.__is_start:
            self.__start()
        self.__image_grid[index[0] * self.__image_size[0]:(index[0]+1) * self.__image_size[0],\
                          index[1] * self.__image_size[1]:(index[1]+1) * self.__image_size[1],\
                          :] = image


class CameraTestAgent(Agent):

    def __init__(self):
        super().__init__()
        self.seq = 0
        self.camera.register_callback(self.camera_cb)
        self.image_grid = ImageGrid(self)

    def camera_cb(self, image, metadata):
        self.seq += 1
        print(f"Frame {self.seq}")
        self.image_grid.new_image(image)


def main():
    camera_test_agent = CameraTestAgent()
    camera_test_agent.start()


if __name__ == "__main__":
    main()
