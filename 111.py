import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import cv2


class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update frame every 30 ms
        self.cap = cv2.VideoCapture(0)  # Use the default camera

        # Load the face detection classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def initUI(self):
        self.setWindowTitle('多路采集监视软件')
        self.setGeometry(100, 100, 640, 480)
        self.showMaximized()
        self.layout = QVBoxLayout()

        # Create a QLabel for displaying the video stream
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        # Create a button for starting/stopping the camera
        self.start_button = QPushButton('Stop Camera', self)
        self.start_button.clicked.connect(self.toggle_camera)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def toggle_camera(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText('Start Camera')
            self.cap.release()
        else:
            self.timer.start(30)  # Restart the timer
            self.start_button.setText('Stop Camera')
            self.cap = cv2.VideoCapture(0)  # Restart the camera

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = QPixmap.fromImage(q_img)
            self.video_label.setPixmap(p)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraApp()
    sys.exit(app.exec_())