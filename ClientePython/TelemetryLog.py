
#           _____________________________
#__________/BIBLIOTECAS
from tkinter import *               # Tk(), Label, Canvas, Photo
from threading import Thread        # p.start()
import threading                    # 
import os                           # ruta = os.path.join('')
import time                         # time.sleep(x)
from tkinter import messagebox      # AskYesNo ()
import tkinter.scrolledtext as tkscrolled

import socket


#           ____________________________
#__________/Variables Globales
global sock, pressedKeys, power, dire, lights, horn, toggle
pressedKeys = []
lights = [1,1,1,1]
power = 0
dire = 0
horn = 0
toggle = True
sock = None


#           ____________________________
#__________/Función para cargar imagenes
def cargarImg(nombre):
    ruta=os.path.join('img',nombre)
    imagen=PhotoImage(file=ruta)
    return imagen


#         ____________________________
#________/Constantes
vel = 10
car_address = ('192.168.43.200', 7070)

#           ____________________________
#__________/Ventana Principal
root=Tk()
root.title('Proyecto 1')
root.minsize(800,400)
root.resizable(width=NO,height=NO)

#           ______________________________
#__________/Se crea un lienzo para objetos
C_root=Canvas(root, width=800,height=600, bg='white')
C_root.place(x=0,y=0)


#           _____________________________________
#__________/Se crea una entrada de texto y titulo
L_ingresarCommand = Label(C_root,text="New Command:",font=('Agency FB',14),bg='white',fg='blue')
L_ingresarCommand.place(x=100,y=10)

E_Command = Entry(C_root,width=30,font=('Agency FB',14))
E_Command.place(x=200,y=10)

SentCarScrolledTxt = tkscrolled.ScrolledText(C_root, height=10, width=45)
SentCarScrolledTxt.place(x=10,y=50)

RevCarScrolledTxt = tkscrolled.ScrolledText(C_root, height=10, width=45)
RevCarScrolledTxt.place(x=400,y=50)




def send2Car(mns):
    global sock
    response = ""
    try:
        if(sock == None):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.connect(car_address)
        mns += "\r\n"
        #sock.sendall(mns.encode())
        
        SentCarScrolledTxt.insert(END, mns)
        SentCarScrolledTxt.see("end")

        data=b''
        response = "ok;"
        time.sleep(0.5)
##        while data!=b'\r':
##            data = sock.recv(1)
##            response+=data.decode("utf-8")
        if(response[-1]!= "\n"): response+="\n"
        
        RevCarScrolledTxt.insert(END, response)
        RevCarScrolledTxt.see('end')

    except Exception as e:
        print(str(e))
        response = "NULL"
    finally:
        sock.close()
        
    return response

     
    
def active():
    global pressedKeys, toggle, power, dire, lights, horn
    while(pressedKeys != []):
        mns = ""
        for i in pressedKeys:
            if i == 'Up':
                if(power < 1000):
                   power+=vel
                   mns += "pwm:"+str(power)+";"
    
            elif i == 'Down':
                if(power > -1000):
                    power-=vel
                    mns += "pwm:"+str(power)+";"

            elif i == 'Right':
                dire = 1
                mns += "dir:"+str(dire)+";"

            elif i == 'Left':
                dire = -1
                mns += "dir:"+str(dire)+";"

            elif i == 'h':
                horn = 1
                mns += "horn:"+str(horn)+";"

            elif i == 'l' and toggle:
                toggle = False
                lights[0] = not lights[0]
                mns += "ll:"+str(lights[0])+";"
            
            elif i == 'r' and toggle:
                toggle = False
                lights[1] = not lights[1]
                mns += "lr:"+str(lights[1])+";"

            elif i == 'b' and toggle:
                toggle = False
                lights[2] = not lights[2]
                mns += "lb:"+str(lights[2])+";"

            elif i == 'f' and toggle:
                toggle = False
                lights[3] = not lights[3]
                mns += "lf:"+str(lights[3])+";"

        send2Car(mns)
##        updateView()
     

def keyPress(event, focus):
    if(focus):
        global pressedKeys
        keyName = event.keysym
        if(keyName in ['Up','Down','Right','Left', 'l', 'r', 'b', 'f', 'h', 'Space'] and not (keyName in pressedKeys)):
            if(pressedKeys == []):
                pressedKeys.append(keyName)
                p = Thread(target=active,args=())
                p.start()
            else:
                pressedKeys.append(keyName)
            

def default(keyName):
    global pressedKeys, power, dire, horn, toggle
    mns = ""
    if keyName == 'Up' or keyName == 'Down' :
        power=0
        mns += "pwm:"+str(power)+";"
    elif keyName == 'Right' or keyName == 'Left':
        dire = 0
        mns += "dire:"+str(dire)+";"
    elif keyName == 'h':
        horn = 0
        mns += "horn:"+str(horn)+";"
    else:
        toggle = True
    
    send2Car(mns)



def keyRelease(event, focus):
    if(focus):
        keyName = event.keysym
        if(keyName in ['Up','Down','Right','Left', 'h','l', 'r', 'b', 'f', 'Space'] and (keyName in pressedKeys)):            
            pressedKeys.remove(keyName)
            default(keyName)


def send ():
    mns = str(E_Command.get())
    send2Car(mns)


def pantalla_controles():
    Controles = Toplevel()
    Controles.title('Controles Teclado')
    Controles.minsize(400,400)
    Controles.resizable(width=NO, height=NO)

    C_controles=Canvas(Controles, width=400, height=400, bg='white')
    C_controles.place(x=0,y=0)

    Controles.focus_set()
    #           ____________________________
    #__________/Cargar una imagen
    down=cargarImg("down.gif")
    down_img=Label(C_controles,bg='white', image=down)
    down_img.place(x=150,y=225)
    
    up = cargarImg("up.gif")
    up_img = Label(C_controles,bg='white', image=up)
    up_img.place(x=150,y=75)

    left = cargarImg("left.gif")
    left_img = Label(C_controles,bg='white', image=left)
    left_img.place(x=75,y=150)

    right=cargarImg("right.gif")
    right_img=Label(C_controles,bg='white', image=right)
    right_img.place(x=225,y=150)
    
    
    Controles.bind_all('<KeyPress>', lambda event: keyPress(event, root.focus_get() == Controles)) 
    Controles.bind_all('<KeyRelease>', lambda event: keyRelease(event, Controles.focus_get() == Controles))
    
    Controles.update()

    

root.bind('<Return>', send)





#           ____________________________
#__________/Botones de ventana principal

Btn_ConnectControl = Button(C_root,text='Send',command=send,fg='white',bg='blue', font=('Agency FB',12))
Btn_ConnectControl.place(x=450,y=10)

Btn_Controls = Button(C_root,text='Arrows',command=pantalla_controles,fg='white',bg='blue', font=('Agency FB',12))
Btn_Controls.place(x=500,y=10)

root.mainloop()
