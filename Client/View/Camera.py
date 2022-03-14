import pickle
import cv2
from PIL import Image, ImageTk
from tkinter import NW
import threading
import numpy as np
import time
import socket
import struct

class Camera(threading.Thread):
    def __init__(self, videoFrame, SERVER_PORT, endCall) -> None:
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.endCall = endCall
        self.SERVER_PORT = SERVER_PORT
        self.SERVER_IP = None
        self.SERVER_SOCKET = None

        self.CALLER_PORT = None
        self.CALLER_IP = None
        self.CALLER_SOCKET = None

        self.img = None
        self.videoFrame = videoFrame
        self.cap = cv2.VideoCapture(0)
        self.randomImg = None


    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        self.err = cv2.imread('Image/Network_ISSUE.jpg')
        cv2.imshow('test window', self.err)
        try:
            self.SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Caller Socket Created Successfully')
        except socket.error as err:
            print('Caller Socket creation failed with error %s' %(err))

        self.SERVER_SOCKET.bind(('', self.SERVER_PORT))
        print('socket binded to %s'%(self.SERVER_PORT))

        self.SERVER_SOCKET.listen(5)
        print('Camera socket is listening')

        self.CALLER_SOCKET, addr = self.SERVER_SOCKET.accept()
        self.CALLER_IP = addr[0]
        self.CALLER_PORT = addr[1]
        ######################################################################

        print('Camera Connection Done.....')

        ######################################################################
        print('CALLER[IP] = ', self.CALLER_IP)
        print('CALLER[PORT] = ', self.CALLER_PORT)
        ######################################################################

        print('Present In Camera')
        while self.stopped() == False:
            try:
                if self.cap.isOpened():
                    print('Camera Opened')
                    ret, img = self.cap.read()
                else:
                    img = self.err
                    print('Camera Not Opened')

                img = cv2.resize(img, (int(self.videoFrame.cget('width')), int(self.videoFrame.cget('height'))))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                ###############################################
                send = pickle.dumps(dict(
                    type = 'Frame',
                    payload = img
                ))
                msg_size = struct.pack('L', len(send))
            
                self.CALLER_SOCKET.sendall(msg_size + send)
                ###############################################

                img = Image.fromarray(img)
                self.img = ImageTk.PhotoImage(image = img)

                self.videoFrame.create_image((0, 0), anchor=NW, image=self.img)
                # time.sleep(.03)
            except:
                self.endCall()

        self.cap.release()
        self.SERVER_SOCKET.close()