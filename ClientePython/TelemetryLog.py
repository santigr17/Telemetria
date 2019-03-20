about ="""

"""

#           _____________________________
#__________/BIBLIOTECAS
from tkinter import *               # Tk(), Label, Canvas, Photo
from threading import Thread        # p.start()
import threading                    # 
import os                           # ruta = os.path.join('')
import time                         # time.sleep(x)
from tkinter import messagebox      # AskYesNo ()

global connCar, pressing, power, dire, lights
connCar, pressing = False, False
power = 0;
dire = 0;
lights = '0b11111111'

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

#           ______________________________
#__________/Se crea una Etiqueta con un título

L_titulo=Label(C_root,text=about,font=('Agency FB',14),bg='white',fg='black')
L_titulo.place(x=550,y=10)

#           _____________________________________
#__________/Se crea una entrada de texto y titulo
L_ingresarCommand = Label(C_root,text="Comando:",font=('Agency FB',14),bg='white',fg='green')
L_ingresarCommand.place(x=30,y=500)

E_Command = Entry(C_root,width=20,font=('Agency FB',14))
E_Command.place(x=100,y=500)

SentCarText = Text(C_root, height=3, width=45)
SentCarText.place(x=10,y=50)
SentCarText.insert(END, "Text of sending messages to car\nJust a text Widget\nin two lines\n")

RevCarText = Text(C_root, height=3, width=45)
RevCarText.place(x=400,y=50)
RevCarText.insert(END, "Text of sending messages to car\nJust a text Widget\nin two lines\n")


def active(key):
    global pressing
    while(pressing):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(car_address)
            mns = getValues()
            mns += "\r"
            sock.sendall(mns.encode())
        except Exception as e:
            print(str(e))
        finally:
            sock.close()
            time.sleep(0.1)


    
def keyPress(event):
    global pressing
    pressing = True
    
    q=Thread(target=active,args=())
    q.start()


def keyRelease(event):
    global pressing
    pressing = False
    goDefault()
        
    

root.bind_all('<KeyPress>', keyPress)
root.bind_all('<KeyRelease>', keyRelease)


def log():
    pass

def conCar():
    global Car
    Car = True

def send():
    pass

#           ____________________________
#__________/Botones de ventana principal

Btn_hilos = Button(C_root,text='Print Log',command=log,fg='white',bg='green')
Btn_hilos.place(x=200,y=10)

Btn_ConnectCar = Button(C_root,text='Start Control',command=conCar,fg='white',bg='green')
Btn_ConnectCar.place(x=50,y=10)

Btn_ConnectControl = Button(C_root,text='Enviar',command=send,fg='white',bg='green')
Btn_ConnectControl.place(x=250,y=500)

root.mainloop()
