"""
    
"""

from threading import Thread        # p.start()
import threading                    # 
import time                         # time.sleep(x)
import socket


control_address = ('192.168.43.202', 8080)
car_address = ('192.168.43.200', 7070)

global vel 
global dire
global luces
global battery
global cero
cero = [0,0,0]

def conControl():
    while(True):
        promEjes = [0,0,0]
        for i in range(10):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(control_address)
                while data!=b'\n':
                    data=b''
                    data = sock.recv(1)
                    mensaje+=data.decode("utf-8")
                #print('received {!r}'.format(data))
                print(mensaje)
                convert(mensaje, promEjes)
                mensaje=""
                data=b''
                sock.close()
                time.sleep(0.05)

            except Exception as e:
                print(str(e))

        procesar(promEjes)
        

def convert(mensaje, prom):
    a = mensaje[:len(mensaje)-1]
    b = a.split(";")
    for i in range(len(b)):
        c=b[i].split(":")[1]
        print(c)
        prom[i]+=c
        print(prom[i])

def procesar(ejes):
    global cero
    global vel
    ejex = ejes[0]/10
    ejey = ejes[1]/10
    ejez = ejes[2]/10

    if(ejex>cero[0]+100 and vel < 1023):
        vel=600
    elif(ejex>cero[0]+200 and vel < 1023):
        vel=800
    elif(ejex>cero[0]+300 and vel < 1023):
        vel+1023
    elif(-100 <= ejex <= 100):
        vel = 0
    elif(ejex<cero[0]+100 and vel > -1023):
        vel-=100
    elif(ejex<cero[0]+200 and vel > -1023):
        vel-=200
    elif(ejex<cero[0]+300 and vel > -1023):
        vel-300    


    
def conCarro():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(car_address)
    while True:
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
        finally:
            time.sleep(0.10)

##
##p=Thread(target=conControl,args=())
##p.start()
##
##q=Thread(target=conCarro,args=())
##q.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(car_address)

while(True):
    mns = input("command: ")    
    if(not ("\r" in mns)) : mns += "\r"
    try:
        sock.sendall(mns.encode())
    except Exception as e:
        print(str(e))
    finally:
        time.sleep(0.500)

