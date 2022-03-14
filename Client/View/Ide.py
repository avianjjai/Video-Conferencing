from tkinter import Button, Canvas
from Model.Point import Point
from View.VideoFrame import VideoFrame
from Connection.Connection import makeCall

class IDE:
    def __init__(self, master, width: float, height: float, bg, SERVER_IP, SERVER_PORT) -> None:
        self.SERVER_PORT = SERVER_PORT
        self.SERVER_IP = SERVER_IP

        connection = makeCall(self.SERVER_IP, self.SERVER_PORT)
        print(connection)

        self.master = master
        self.master.title("Video Conferencing")
        dim = str(width) + 'x' + str(height)
        self.master.geometry(dim)

        # Complete IDE
        canvas = dict(
            master = self.master,
            # bg = bg,
            height = height,
            width = width
        )
        self.canvas = Canvas(**canvas)

        # Description Part: 8.20TOP
        descripttion = dict(
            master = self.canvas,
            bg = '#234561',
            height = height*.2,
            width = width
        )
        self.description = Canvas(**descripttion)
        self.description.pack()

        # Video Frame Part: Mid
        videoFrameOuter = dict(
            master = self.canvas,
            bg = '#876354',
            height = height*.6,
            width = width
        )
        self.videoFrameOuter = Canvas(**videoFrameOuter)

        border = dict(
            width = 10
        )

        # Insert Video Frame
        videoFrame1 = dict(
            master = self.videoFrameOuter,
            height = videoFrameOuter['height']-20,
            width = (videoFrameOuter['width']-30)/2,
            top_left = Point(x = border['width'], y = border['width']),
            bg = '#784628',
            videoType = 'Camera',
            CAMERA_PORT = connection['CAMERA_PORT'],
            MIC_PORT = connection['MIC_PORT'],
            endCall = self.endCall
        )
        self.videoFrame1 = VideoFrame(**videoFrame1)

        videoFrame2 = dict(
            master = self.videoFrameOuter,
            height = videoFrameOuter['height']-20,
            width = (videoFrameOuter['width']-30)/2,
            top_left = Point(x = videoFrame1['width'] + 2*border['width'], y = border['width']),
            bg = '#784628',
            videoType = 'Video',
            CALLER_CAMERA_PORT = connection['CALLER_CAMERA_PORT'],
            CALLER_MIC_PORT = connection['CALLER_MIC_PORT'],
            CALLER_IP = connection['CALLER_IP'],
            endCall = self.endCall
        )
        self.videoFrame2 = VideoFrame(**videoFrame2)

        self.videoFrameOuter.pack()

        # Control Panel Part: Bottom
        controlPanel = dict(
            master = self.canvas,
            bg = '#969754',
            height = height*.2,
            width = width
        )
        self.controlPanel = Canvas(**controlPanel)

        cutButton = dict(
            master = self.controlPanel,
            text = 'End',
            command = self.endCall
        )
        self.cutButton = Button(**cutButton)
        self.cutButton.pack()

        self.controlPanel.pack()

        self.canvas.pack()

    def endCall(self):
        try:
            del self.videoFrame1
        except:
            pass

        try:
            del self.videoFrame2
        except:
            pass