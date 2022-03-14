import pyaudio
import threading
import socket
import struct
import pickle
import numpy as np

class Mic(threading.Thread):
    def __init__(self, frame_size, duration, SERVER_PORT, endCall):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.endCall = endCall
        self.SERVER_PORT = SERVER_PORT
        self.SERVER_IP = None
        self.SERVER_SOCKET = None

        self.CALLER_PORT = None
        self.CALLER_IP = None
        self.CALLER_SOCKET = None

        self.duration = duration
        self.frame_size = frame_size

        attr = dict(
            format = pyaudio.paInt16,
            channels = 1,
            rate = frame_size,
            input = True,
            frames_per_buffer = int(frame_size*duration)
        )

        self.obj = pyaudio.PyAudio()
        self.stream = self.obj.open(**attr)

    def stop(self):
        self._stop.set()
    
    def stopped(self):
        return self._stop.isSet()

    def record(self):
        nsamples = int(self.duration*self.frame_size)
        buffer = self.stream.read(nsamples)
        arr = np.frombuffer(buffer, dtype='int16')
        return arr

    def run(self):
        print(self.SERVER_IP, self.SERVER_PORT)

        try:
            self.SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Caller Socket Created Successfully')
        except socket.error as err:
            print('Caller Socket creation failed with error %s' %(err))

        self.SERVER_SOCKET.bind(('', self.SERVER_PORT))
        print('socket binded to %s'%(self.SERVER_PORT))

        self.SERVER_SOCKET.listen(5)
        print('socket is listening')

        self.CALLER_SOCKET, addr = self.SERVER_SOCKET.accept()
        self.CALLER_IP = addr[0]
        self.CALLER_PORT = addr[1]
        ######################################################################

        ######################################################################
        print('CALLER[IP] = ', self.CALLER_IP)
        print('CALLER[PORT] = ', self.CALLER_PORT)
        ######################################################################


        while self.stopped() == False:
            try:
                sound = self.record()

                ###############################################
                send = pickle.dumps(dict(
                    type = 'Frame',
                    payload = sound
                ))

                msg_size = struct.pack('L', len(send))
                self.CALLER_SOCKET.sendall(msg_size + send)
                ###############################################
            except:
                self.endCall()
            
        self.SERVER_SOCKET.close()
        self.stream.close()
        self.obj.terminate()