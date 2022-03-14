import socket
import pickle

def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Server Socket Created Successfully')
    except socket.error as err:
        print('Server Socket creation failed with error %s' %(err))
    
    PORT = 30000
    server.bind(('', PORT))
    print('socket binded to %s'%(PORT))

    server.listen(5)
    print('socket is listening')

    clients = []
    while len(clients) < 2:
        c, addr = server.accept()
        print('Listen:', addr)
        clients.append([c, addr])

    c1_poi = clients[0][0]
    c2_poi = clients[1][0]

    c1_data = pickle.loads(c1_poi.recv(1024))
    print(c1_data)
    c1_CAMERA_PORT = c1_data['CAMERA_PORT']
    c1_MIC_PORT = c1_data['MIC_PORT']
    c1_ip = clients[0][1][0]

    c2_data = pickle.loads(c2_poi.recv(1024))
    c2_CAMERA_PORT = c2_data['CAMERA_PORT']
    c2_MIC_PORT = c2_data['MIC_PORT']
    c2_ip = clients[1][1][0]

    c1_data = pickle.dumps(dict(
        CAMERA_PORT = c1_CAMERA_PORT,
        MIC_PORT = c1_MIC_PORT,
        IP = c1_ip
    ))

    c2_poi.send(c1_data)

    c2_data = pickle.dumps(dict(
        CAMERA_PORT = c2_CAMERA_PORT,
        MIC_PORT = c2_MIC_PORT,
        IP = c2_ip
    ))
    
    c1_poi.send(c2_data)

    c1_poi.close()
    c2_poi.close()
    server.close()

if __name__ == '__main__':
    main()