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


#           ____________________________
#__________/Función para cargar imagenes
def cargarImg(nombre):
    ruta=os.path.join('img',nombre)
    imagen=PhotoImage(file=ruta)
    return imagen



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
L_ingresarNombre = Label(C_root,text="Ingrese su nombre:",font=('Agency FB',14),bg='white',fg='green')
L_ingresarNombre.place(x=560,y=400)
E_nombre = Entry(C_root,width=20,font=('Agency FB',14))
E_nombre.place(x=560,y=425)


#           ____________________________
#__________/Crear una nueva ventana
def VentanaJuego(nombre_jugador):
    #Esconder la pantalla sin destruirla
    #root.withdraw()
    #Pantalla secundarias
    juego=Toplevel()
    juego.title('EJEMPLO')
    juego.minsize(800,600)
    juego.resizable(width=NO, height=NO)

    C_juego=Canvas(juego, width=800,height=600, bg='light blue')
    C_juego.place(x=0,y=0)


    L_nombre=Label(C_juego, text="Piloto: "+nombre_jugador ,font=('Agency FB',20), fg='light blue', bg='white')
    L_nombre.place(x=10,y=10)

    CarText = Text(C_juego, height=3, width=45)
    CarText.place(x=10,y=50)
    CarText.insert(END, "Text of sending messages to car\nJust a text Widget\nin two lines\n")
    
    ControlText = Text(C_juego, height=3, width=45)
    ControlText.place(x=400,y=50)
    ControlText.insert(END, "Text of receiving messages from control\nJust a text Widget\nin two lines\n")
    
#           _____________________________
#__________/Volver a la ventana principal
    def back():
        juego.destroy()
        #root.deiconify()


#           ____________________________
#__________/Boton volver pantalla juego

    Btn_back = Button(C_juego,text='Atras',command=back,bg='white',fg='green')
    Btn_back.place(x=100,y=560)



#           ____________________________
#__________/Función del botón juego
def empezar_juego():
    #Obtener el nombre de un entry
    nombre = str(E_nombre.get())
    VentanaJuego(nombre)


def conCar():
    pass

def conControl():
    pass
#           ____________________________
#__________/Botones de ventana principal

Btn_hilos = Button(C_root,text='Log',command=empezar_juego,fg='white',bg='green')
Btn_hilos.place(x=560,y=470)

Btn_ConnectCar = Button(C_root,text='Car Connection',command=conCar,fg='white',bg='green')
Btn_ConnectCar.place(x=100,y=550)

Btn_ConnectControl = Button(C_root,text='Control Connection',command=conControl,fg='white',bg='green')
Btn_ConnectControl.place(x=200,y=550)

root.mainloop()