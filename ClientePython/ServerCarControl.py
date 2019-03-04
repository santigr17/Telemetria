"""
    
"""

from threading import Thread        # p.start()
import threading                    # 
import time                         # time.sleep(x)
import socket


control_address = ('192.168.43.202', 8080)
 = ('192.168.43.200', 7070)

global vel 
global dire
global luces
global battery


def conControl():
    while(True):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(control_address)
            while data!=b'\n':
                data=b''
                data = sock.recv(1)
                mensaje+=data.decode("utf-8")
            #print('received {!r}'.format(data))
            print(mensaje)
            mensaje=""
            data=b''
            sock.close()
            time.sleep(0.05)

        except Exception as e:
            print(str(e))

            
def conCarro(mensaje):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(car_address)   
    try:
        # Send data
        if(not ("\r" in message)) : message += "\r"
        sock.sendall(message.encode())

        mensaje=""
        data=b''
        while data!=b'\r':
            data=b''
            data = sock.recv(1)
            mensaje+=data.decode("utf-8")

    except Exception as e:
        print(str(e))


def sending(mensaje):
    q=Thread(target=conCarro,args=(mensaje))
    q.start()


p=Thread(target=conControl,args=())
p.start()







