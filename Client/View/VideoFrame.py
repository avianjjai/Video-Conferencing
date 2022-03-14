from tkinter import Canvas
from Model.Point import Point
from View.Camera import Camera
from View.Video import Video
from View.Mic import Mic
from View.Speaker import Speaker
import threading

class VideoFrame():
    def __init__(self, master, width: float, height: float, top_left: Point, bg, videoType, CAMERA_PORT = None, MIC_PORT = None, CALLER_CAMERA_PORT = None, CALLER_MIC_PORT = None, CALLER_IP = None, endCall = None) -> None:
        self.videoType = videoType
        self.endCall = endCall

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
        
        self.video = self.create(CAMERA_PORT, CALLER_IP, CALLER_CAMERA_PORT)
        self.video.start()

        self.sound = self.createSound(MIC_PORT, CALLER_IP, CALLER_MIC_PORT)
        self.sound.start()

    def __del__(self):
        self.video.stop()
        self.sound.stop()


    def create(self, CAMERA_PORT, CALLER_CAMERA_IP, CALLER_CAMERA_PORT):
        print(self.videoType)
        if self.videoType == 'Camera':
            return Camera(self.videoFrame, CAMERA_PORT, self.endCall)

        elif self.videoType == 'Video':
            return Video(self.videoFrame, CALLER_CAMERA_IP, CALLER_CAMERA_PORT, self.endCall)

    def createSound(self, MIC_PORT, CALLER_MIC_IP, CALLER_MIC_PORT):
        if self.videoType == 'Camera':
            return Mic(8000, 0.1, MIC_PORT, self.endCall)

        elif self.videoType == 'Video':
            return Speaker(8000, CALLER_MIC_IP, CALLER_MIC_PORT, self.endCall)