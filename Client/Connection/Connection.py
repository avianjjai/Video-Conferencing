import socket
import numpy as np
import pickle
from SESSION.SESSION import SERVER, ME, CALLER


def makeCall(SERVER_IP, SERVER_PORT):
    ######################################################################
    CAMERA_PORT = np.random.randint(3000, 30000)
    MIC_PORT = np.random.randint(30000, 40000)

    SERVER_SOCKET = socket.socket()
    SERVER_SOCKET.connect((SERVER_IP, SERVER_PORT))

    send = pickle.dumps(dict(
        CAMERA_PORT = CAMERA_PORT,
        MIC_PORT = MIC_PORT
    ))

    SERVER_SOCKET.send(send)

    recv = pickle.loads(SERVER_SOCKET.recv(1024))
    CALLER_CAMERA_PORT = recv['CAMERA_PORT']
    CALLER_MIC_PORT = recv['MIC_PORT']
    CALLER_IP = recv['IP']

    SERVER_SOCKET.close()
    
    return dict(
        CAMERA_PORT = CAMERA_PORT,
        MIC_PORT = MIC_PORT,
        CALLER_CAMERA_PORT = CALLER_CAMERA_PORT,
        CALLER_MIC_PORT = CALLER_MIC_PORT,
        CALLER_IP = CALLER_IP
    )
    ######################################################################
