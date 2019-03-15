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
cero = [-7.0, -67.0, -15.0]
vel = 0
dire = 0

global ControlConnected
global CarConnected
ControlConnected = True
CarConnected = True


def conControl():
    notError = True
    global ControlConnected
    global CarConnected
    
    while(notError and CarConnected):
        ejesMedia = [0,0,0]
        for i in range(10):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(control_address)
                mensaje=""
                data=b''
                while data!=b'\n':
                    data=b''
                    data = sock.recv(1)
                    mensaje+=data.decode("utf-8")
                acumular(mensaje, ejesMedia)
                sock.close()
                
            except Exception as e:
                print(str(e))
                notError = False
                ControlConnected = False
                break
            
        print ("Ejes media:",ejesMedia)
        procesar(ejesMedia)
    

def acumular(mensaje, prom):
    a = mensaje[:len(mensaje)-1]
    b = a.split(";")
    for i in range(len(b)-1):
        c = (b[i].split(":"))[1]
        prom[i]+=float(c)
    
    

def procesar(ejes):
    global vel
    global dire
    ejex = ejes[0]//10
    ejey = ejes[1]//10
    ejez = ejes[2]//10

    print(ejex,ejey,ejez)
    if(0<ejex>cero[0]+20):
        if(ejex>cero[0]+20 and vel < 1023):
            vel+=200
        elif(0 < ejex>cero[0]+40 and vel < 1023):
            vel+=400
        elif(ejex>cero[0]+80 and vel < 1023):
            dire+=650
            
    elif(0>ejex<cero[0]-20):
        if(ejex<cero[0]-20 and vel > -1023):
            vel-=200
            
        elif(ejex<cero[0]-40 and vel > -1023):
            vel-=400
            
        elif(ejex<cero[0]-80 and vel > -1023):
            vel-=650

    else:
        if(vel//1>0): vel-=100
        elif(vel//1<0):vel+=100


    if(vel>1023):
        vel = 1023
    
    if(vel<-1023):
        vel = -1023

        
    if(ejey>cero[1]+40):
        dire=1

    elif(cero[1]-100< ejey <cero[1]+100):
        dire=0

    elif(ejey<cero[1]-40):
        dire = -1

    time.sleep(0.001)
    print("vel:",vel)
    print("dir:",dire)

    
def conCarro():
    global CarConnected
    global ControlConnected
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(car_address)

    except Exception as e:
            print(str(e))
            CarConnected = False
            
    while (ControlConnected):
        try:
            mns = getMessage()
            # Send data
            if(not ("\r" in mns)) : mns += "\r"

            #print("Mensaje",mns)
            sock.sendall(mns.encode())
            
            mensaje=""
            data=b''
            while data!=b'\r':
                data=b''
                data = sock.recv(1)
                mensaje+=data.decode("utf-8")

        except Exception as e:
            print(str(e))
            CarConnected = False
            break
        finally:
            time.sleep(0.05)
    if(CarConnected):
        sock.close()
    time.sleep(0.05)

def getMessage():
    message = "pwm:"+str(vel)+";"
    message += "dir:"+str(dire)+";"
    return message

p=Thread(target=conControl,args=())
p.start()

q=Thread(target=conCarro,args=())
q.start()



