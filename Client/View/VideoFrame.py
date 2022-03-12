from tkinter import Canvas
from Model.Point import Point
from View.Camera import Camera
from View.Video import Video
import threading

class VideoFrame(threading.Thread):
    def __init__(self, master, width: float, height: float, top_left: Point, bg, videoType) -> None:
        threading.Thread.__init__(self)
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
        self.video = None


    def run(self):
        if self.videoType == 'Camera':
            self.video = Camera(self.videoFrame)
            self.video.capture()

        elif self.videoType == 'Video':
            self.video = Video(self.videoFrame)
            self.video.capture()