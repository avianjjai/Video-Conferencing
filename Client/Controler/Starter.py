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
        # SERVER_IP = '54.144.245.22',
        SERVER_IP='192.168.211.30',
        SERVER_PORT = 4455
    )
    application = IDE(**attr)
    root.mainloop()