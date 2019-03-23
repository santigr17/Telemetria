
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


#         ____________________________
#________/Constantes
vel = 10
car_address = ('192.168.43.200', 7070)
center = [260,100,340,100,300,140]
left_rotate = [266, 80, 334, 120, 280, 134]
right_rotate = [334, 80, 266, 120, 320, 134]
#           ____________________________
#__________/Ventana Principal
root=Tk()
root.title('Taller Tkinter')
root.minsize(800,600)
root.resizable(width=NO,height=NO)

#           ______________________________
#__________/Se crea un lienzo para objetos
C_root=Canvas(root, width=800,height=600, bg='white')
C_root.place(x=0,y=0)


#           _____________________________________
#__________/Se crea una entrada de texto y titulo
L_ingresarCommand = Label(C_root,text="Nuevo Comando:",font=('Agency FB',14),bg='white',fg='blue')
L_ingresarCommand.place(x=100,y=10)

E_Command = Entry(C_root,width=30,font=('Agency FB',14))
E_Command.place(x=200,y=10)

SentCarScrolledTxt = tkscrolled.ScrolledText(C_root, height=10, width=45)
SentCarScrolledTxt.place(x=10,y=50)

RevCarScrolledTxt = tkscrolled.ScrolledText(C_root, height=10, width=45)
RevCarScrolledTxt.place(x=400,y=50)


##C_indicadores = Canvas(C_root, width=760, height=200, bg='light blue')
##C_indicadores.place(x=20, y = 300)
##
##C_indicadores.create_arc(10, 50, 210, 250, fill="#F7FF79", outline="grey", start=160, extent=-140)
##indi_power = C_indicadores.create_arc(10, 50, 210, 250, fill="orange", outline="grey", start=160, extent=-10)
##
##C_indicadores.create_oval(250, 50, 350, 150, fill = "#0003B2")
##C_indicadores.create_oval(260, 60, 340, 140, fill = "light blue")
##indi_rotate = C_indicadores.create_polygon(center, fill='#0003B2', outline = "black", tags="volante")
##
##indi_reverse = C_indicadores.create_oval(200, 40, 230, 70, fill="grey")
##
##indi_lights = []
##for i in range(4):
##    indi_lights.append(C_indicadores.create_oval(400+i*60, 50, 450+i*60, 100, fill="grey"))
##
##def updateView():
##    indi = int(abs(power)/10 + 20)
##    C_indicadores.itemconfig(indi_power, extent = -indi)
##    
##    
##    items = C_indicadores.find_withtag('volante')
##    C_indicadores.delete(item)
##    if(dire == -1):    
##        C_indicadores.create_polygon(right_rotate, fill='#0003B2', outline = "black", tags="volante")
##  
##    elif(dire == 1):
##        C_indicadores.create_polygon(left_rotate, fill='#0003B2', outline = "black", tags="volante")
##    
##    else:
##        C_indicadores.create_polygon(center, fill='#0003B2', outline = "black", tags="volante")
##
##    


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
     

def keyPress(event):
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



def keyRelease(event):
    keyName = event.keysym
    if(keyName in ['Up','Down','Right','Left', 'h','l', 'r', 'b', 'f', 'Space'] and (keyName in pressedKeys)):            
        pressedKeys.remove(keyName)
        default(keyName)


def send ():
    mns = str(E_Command.get())
    send2Car(mns)




root.bind_all('<KeyPress>', keyPress)
root.bind_all('<KeyRelease>', keyRelease)
root.bind('<Return>', send)





#           ____________________________
#__________/Botones de ventana principal

Btn_ConnectControl = Button(C_root,text='Enviar',command=send,fg='white',bg='blue', font=('Agency FB',12))
Btn_ConnectControl.place(x=450,y=10)

root.mainloop()
