# MIT License
#
# Copyright (c) 2021 Mobotx
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import select
import termios
import tty
import threading

import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from mobot.brain.agent import Agent
from mobot.utils.rate import Rate

CTRL_PLUS_C = '\x03'


def get_key(key_timeout):
    settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


class TeleopAgent(Agent):

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.camera.register_callback(self.camera_cb)
        self.flashlight.enable()
        self.chassis.enable()
        self.keyboard_teleop_thread = threading.Thread(target=self.keyboard_teleop_thread)
        self.control_thread = threading.Thread(target=self.control_thread)

        self.cmd_v = 0.0
        self.cmd_w = 0.0

    def on_start(self):
        self.keyboard_teleop_thread.start()
        self.control_thread.start()
        self.ui.flashlight.toggled.connect(self.flashlight_cb)
        self.ui.joystick.pose.connect(self.joystick_cb)

    def flashlight_cb(self):
        self.flashlight.toggle()

    def joystick_cb(self, x, y):
        wmax = (self.chassis.WHEEL_DIAMETER * self.chassis.MAX_WHEEL_SPEED)/self.chassis.WHEEL_TO_WHEEL_SEPARATION
        vmax = (self.chassis.WHEEL_DIAMETER * self.chassis.MAX_WHEEL_SPEED)/2
        self.cmd_v = -(y/100) * vmax
        self.cmd_w = -(x/100) * wmax

    def keyboard_teleop_thread(self):
        self.bindings = {'w':( 0.07,  0.0),\
                         'a':( 0.0,  0.5),\
                         's':(-0.07,  0.0),\
                         'd':( 0.0, -0.5),\
                         ' ':( 0.0,  0.0)}
        self.help_msg = """Moving around:
                w
           a    s    d

        Spacebar to Stop!
        CTRL-C to quit
        """
        self.logger.info(self.help_msg)
        rate = Rate(50)
        while self.ok():
            key = get_key(0.1)
            if key in self.bindings:
                self.cmd_v=self.bindings[key][0]
                self.cmd_w=self.bindings[key][1]
            rate.sleep()
        print() ## Temp Fix for indentation in terminal

    def control_thread(self):
        rate = Rate(10)
        while self.ok():
            self.chassis.set_cmdvel(v=self.cmd_v, w=self.cmd_w)
            rate.sleep()

    def camera_cb(self, image, metadata):
        self.ui.set_image(image)


class Joystick(QWidget):

    pose = pyqtSignal(float,float)
    def __init__(self, parent=None):
        super(Joystick, self).__init__(parent)
        self.setMinimumSize(250, 250)
        self.movingOffset = QPointF(0, 0)
        self.grabCenter = False
        self.__maxDistance = 100

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawEllipse(self._bound())
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawEllipse(self._centerEllipse())

    def _bound(self):
        bounds = QRectF(
            -self.__maxDistance,
            -self.__maxDistance,
            self.__maxDistance * 2,
            self.__maxDistance * 2
        )
        return bounds.translated(self._center())

    def _centerEllipse(self):
        if self.grabCenter:
            return QRectF(-20, -20, 40, 40).translated(self.movingOffset)
        return QRectF(-20, -20, 40, 40).translated(self._center())

    def _center(self):
        return QPointF(self.width()/2, self.height()/2)

    def _boundJoystick(self, point):
        limitLine = QLineF(self._center(), point)
        if (limitLine.length() > self.__maxDistance):
            limitLine.setLength(self.__maxDistance)
        return limitLine.p2()

    def emit(self):
        offset = self.movingOffset - self._center() 
        self.pose.emit(offset.x(), offset.y())

    def mousePressEvent(self, event):
        self.grabCenter = self._bound().contains(event.pos())
        if self.grabCenter:
            self.movingOffset = self._boundJoystick(event.pos())
            self.update()
            self.emit()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.grabCenter:
            self.grabCenter = False
            self.movingOffset = self._center()
            self.update()
            self.emit()

    def mouseMoveEvent(self, event):
        if self.grabCenter:
            self.movingOffset = self._boundJoystick(event.pos())
            self.update()
            self.emit()

class Ui:

    def setupUi(self, main_window):
        main_window.setWindowTitle("Dashboard")
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.image = QLabel()
        self.flashlight = QCheckBox("Flashlight")
        self.flashlight.setChecked(False)
        self.joystick = Joystick()

        layout.addWidget(self.image)
        layout.addWidget(self.flashlight)
        layout.addWidget(self.joystick)
        central_widget.setLayout(layout)
        main_window.setCentralWidget(central_widget)

    def set_image(self, image):
        H, W, C = image.shape
        qImg = QImage(np.require(image, np.uint8, 'C'),
                W, H,
                QImage.Format_RGB888)

        pixmap = QPixmap(qImg)
        pixmap = pixmap.scaled(400,400, Qt.KeepAspectRatio)
        self.image.setPixmap(pixmap)


def main():
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Cleanlooks"))
    main_window = QMainWindow()
    ui = Ui()
    ui.setupUi(main_window)
    teleop_agent = TeleopAgent(ui)
    main_window.show()
    teleop_agent.start()
    if not app.exec():
        teleop_agent.terminate()


if __name__ == "__main__":
    main()
