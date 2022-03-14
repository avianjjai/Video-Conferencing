import pyaudio
import threading
import socket
import struct
import pickle
import numpy as np

class Speaker(threading.Thread):
    def __init__(self, frame_size, SERVER_IP, SERVER_PORT, endCall):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.endCall = endCall
        self.SERVER_PORT = SERVER_PORT
        self.SERVER_IP = SERVER_IP
        self.SERVER_SOCKET = None

        attr = dict(
            format = pyaudio.paInt16,
            channels = 1,
            rate = frame_size,
            output = True
        )

        self.obj = pyaudio.PyAudio()
        self.stream = self.obj.open(**attr)

    def stop(self):
        self._stop.set()
    
    def stopped(self):
        return self._stop.isSet()

    def play(self, sound):
        self.stream.write(sound.tobytes())

    def run(self):
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
                sound = data['payload']
                self.play(sound)
            except:
                self.endCall()
            
        self.SERVER_SOCKET.close()
        self.stream.close()
        self.obj.terminate()