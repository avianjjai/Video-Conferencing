from tkinter import *
from View.Ide import IDE

def main():
    root = Tk()
    root.resizable(width=False, height=False)
    attr = dict(
        master = root,
        width = 800,
        height = 600,
        bg = '#B49D98',
        # SERVER_IP='127.0.0.1',
        # SERVER_IP='192.168.39.126',
        # SERVER_IP = '106.208.155.209',
        SERVER_IP = '3.22.15.135',
        # SERVER_PORT=30000
        SERVER_PORT = 18004
    )
    application = IDE(**attr)
    root.mainloop()