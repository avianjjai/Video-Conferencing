import cv2
from PIL import Image, ImageTk
from tkinter import NW

class Video:
    def __init__(self, videoFrame) -> None:
        self.img = None
        self.videoFrame = videoFrame

    def capture(self):
        while True:
            img = cv2.imread('Image/Network_ISSUE.jpg')
            img = cv2.resize(img, (int(self.videoFrame.cget('width')), int(self.videoFrame.cget('height'))))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            self.img = ImageTk.PhotoImage(image = img)

            self.videoFrame.create_image((0, 0), anchor=NW, image=self.img)