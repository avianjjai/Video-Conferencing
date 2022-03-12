from tkinter import Canvas
from Model.Point import Point
from View.VideoFrame import VideoFrame

class IDE:
    def __init__(self, master, width: float, height: float, bg) -> None:
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
            # bg = '#876354',
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
            videoType = 'Camera'
        )
        self.videoFrame1 = VideoFrame(**videoFrame1)
        self.videoFrame1.start()

        videoFrame2 = dict(
            master = self.videoFrameOuter,
            height = videoFrameOuter['height']-20,
            width = (videoFrameOuter['width']-30)/2,
            top_left = Point(x = videoFrame1['width'] + 2*border['width'], y = border['width']),
            bg = '#784628',
            videoType = 'Video'
        )
        self.videoFrame2 = VideoFrame(**videoFrame2)
        self.videoFrame2.start()

        self.videoFrameOuter.pack()

        # Control Panel Part: Bottom
        controlPanel = dict(
            master = self.canvas,
            bg = '#587354',
            height = height*.2,
            width = width
        )
        self.controlPanel = Canvas(**controlPanel)
        self.controlPanel.pack()

        self.canvas.pack()