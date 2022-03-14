import cv2
from PIL import Image, ImageTk
from tkinter import NW
import threading
import time
import socket
import pickle
import struct

class Video(threading.Thread):
    def __init__(self, videoFrame, SERVER_IP, SERVER_PORT, endCall) -> None:
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.endCall = endCall
        self.SERVER_PORT = SERVER_PORT
        self.SERVER_IP = SERVER_IP
        self.SERVER_SOCKET = None
        self.img = None
        self.videoFrame = videoFrame

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


    def run(self):
        # time.sleep(2)

        print(self.SERVER_IP, self.SERVER_PORT)

        ######################################################################
        self.SERVER_SOCKET = socket.socket()
        while True:
            try:
                self.SERVER_SOCKET.connect((self.SERVER_IP, self.SERVER_PORT))
                break
            except:
                continue

        ######################################################################

        payload_size = struct.calcsize('L')
        recv = b''
        while self.stopped() == False:
            try:
                while len(recv) < payload_size:
                    recv += self.SERVER_SOCKET.recv(4096)
                packed_msg_size = recv[: payload_size]
                recv = recv[payload_size:]
                msg_size = struct.unpack('L', packed_msg_size)[0]
                while len(recv) < msg_size:
                    recv += self.SERVER_SOCKET.recv(4096)
                frame_data = recv[: msg_size]
                recv = recv[msg_size: ]
                
                data = pickle.loads(frame_data)
                img = data['payload']
                img = cv2.resize(img, (int(self.videoFrame.cget('width')), int(self.videoFrame.cget('height'))))
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                self.img = ImageTk.PhotoImage(image = img)

                self.videoFrame.create_image((0, 0), anchor=NW, image=self.img)
                # time.sleep(.03)
            except:
                self.endCall()
        
        self.SERVER_SOCKET.close()