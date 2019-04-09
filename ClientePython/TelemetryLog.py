
#           _____________________________
#__________/BIBLIOTECAS
from tkinter import *               # Tk(), Label, Canvas, Photo
from threading import Thread        # p.start()
import threading                    # 
import os                           # ruta = os.path.join('')
import time                         # time.sleep(x)
from tkinter import messagebox      # AskYesNo ()
import tkinter.scrolledtext as tkscrolled
##### Biblioteca para el Carro
import wifiConnection


#           ____________________________
#__________/Función para cargar imagenes
def cargarImg(nombre):
    ruta=os.path.join('img',nombre)
    imagen=PhotoImage(file=ruta)
    return imagen


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


#           _____________________________________
#__________/Creando el cliente para NodeMCU
myCar = wifiConnection.NodeMCU()
myCar.start()

def send (event):
    mns = str(E_Command.get())
    if(len(mns)>0 and mns[-1] == ";"):
        E_Command.delete(0, 'end')
        myCar.send(mns)
    
root.bind('<Return>', send)

#           ____________________________
#__________/Variables Carro
global power
power = 0

lights = [1,1,1,1]

dire = 0
horn = 0
toggle = True
vel = 20


def get_log():
    indice = 0
    while(myCar.keep_log):
        while(indice < len(myCar.log)):
            mnsSend = "[{0}] cmd: {1}\n".format(indice,myCar.log[indice][0])
            SentCarScrolledTxt.insert(END,mnsSend)
            SentCarScrolledTxt.see("end")

            mnsRecv = "[{0}] result: {1}\n".format(indice,myCar.log[indice][1])
            RevCarScrolledTxt.insert(END, mnsRecv)
            RevCarScrolledTxt.see('end')

            indice+=1
        time.sleep(0.200)
    
p = Thread(target=get_log)
p.start()
           


def move (event, focus):
    if(focus):
        global power
        mns = ""
        if event.keysym == 'Up':
            if(power < 1000):
                value = power
                if(power<350):
                    power +=vel+100
                    value = 0
                else:
                    power+=vel
                mns = "pwm:{0};".format(value)
            
        else:
            if(power > -1000):
                value = power
                if(power>-350):
                    power -= vel+100
                    value = 0
                else:
                    power-=vel
                mns = "pwm:{0};".format(value)
        if(mns!=""):
            myCar.send(mns)
        time.sleep(0.2)

                
def active(key):
    mns = ""
    if key== 'Right':
        mns += "dir:1;dir:-1;"

    elif key== 'Left':
        mns += "dir:-1;dir:1;"

    elif key== 'h':
            mns += "horn:1;"

    elif key== 'l':
        lights[0] = not lights[0]
        mns += "ll:{0};".format(str(int(lights[0])))
    
    elif key== 'r':
        lights[1] = not lights[1]
        mns += "lr:{0};".format(str(int(lights[1])))

    elif key== 'b' :
        lights[2] = not lights[2]
        mns += "lb:{0};".format(str(int(lights[2])))

    elif key== 'f' :
        lights[3] = not lights[3]
        mns += "lf:{0};".format(str(int(lights[3])))

    elif key == 's':
        mns += "sense;"
        

    if(mns!=""):
        myCar.send(mns)



def restore(keyName):
    mns = ""
    if keyName == 'Right' or keyName == 'Left':
        mns = "dir:0;"
        
    elif keyName == 'h':
        mns += "horn:0;"

    myCar.send(mns)
        

def keyPress(event, focus, pressedKeys):
    if(focus):
        keyName = event.keysym
        if(keyName in ['Right','Left', 'h','l', 'r', 'b', 'f', 's' ]):
            if(not (keyName in pressedKeys)):
                pressedKeys.append(keyName)
                active(keyName)
    
                

            
def keyRelease(event, pressedKeys):
    keyName = event.keysym
    if(keyName in ['Right','Left', 'h','l', 'r', 'b', 'f', 's'] and (keyName in pressedKeys)):
        pressedKeys.remove(keyName)
        restore(keyName)

            
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

    pressedKeys = [] 

    Controles.bind('<Up>', lambda event: move(event, root.focus_get() == Controles))
    Controles.bind('<Down>', lambda event: move(event, root.focus_get() == Controles))
    Controles.bind_all('<KeyPress>', lambda event: keyPress(event, root.focus_get() == Controles, pressedKeys)) 
    Controles.bind_all('<KeyRelease>', lambda event: keyRelease(event, pressedKeys))
    
    Controles.mainloop()
    

#           ____________________________
#__________/Botones de ventana principal

Btn_ConnectControl = Button(C_root,text='Send',command=send,fg='white',bg='blue', font=('Agency FB',12))
Btn_ConnectControl.place(x=450,y=10)

Btn_Controls = Button(C_root,text='Arrows',command=pantalla_controles,fg='white',bg='blue', font=('Agency FB',12))
Btn_Controls.place(x=500,y=10)

root.mainloop()
