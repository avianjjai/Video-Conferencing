from tkinter import Canvas
from Model.Point import Point
from View.Camera import Camera
from View.Video import Video
import threading

class VideoFrame():
    def __init__(self, master, width: float, height: float, top_left: Point, bg, videoType, CAMERA_PORT = None, CALLER_PORT = None, CALLER_IP = None) -> None:
        self.videoType = videoType

        # Name Frame
        nameFrame = dict(
            master = master,
            bg = bg,
            height = height*.2,
            width = width
        )
        self.nameFrame = Canvas(**nameFrame)
        self.nameFrame.place(x=top_left.x, y=top_left.y)
        
        # Video Frame
        videoFrame = dict(
            master = master,
            bg = bg,
            height = height*.8,
            width = width
        )
        self.videoFrame = Canvas(**videoFrame)
        self.videoFrame.place(x=top_left.x, y=top_left.y + nameFrame['height'])
        self.video = self.create(CAMERA_PORT, CALLER_IP, CALLER_PORT)
        self.video.start()

    def __del__(self):
        self.video.stop()


    def create(self, CAMERA_PORT, CALLER_IP, CALLER_PORT):
        if self.videoType == 'Camera':
            return Camera(self.videoFrame, CAMERA_PORT)

        elif self.videoType == 'Video':
            return Video(self.videoFrame, CALLER_IP, CALLER_PORT)