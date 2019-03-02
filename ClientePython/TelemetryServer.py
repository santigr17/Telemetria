about ="""
___________________________________________
Instituto Tecnologico de Costa Rica         *
Computer Engineering                        *
Tutorías taller de programación             *
                                            *
Milton Villegas Lemus                       * 
Ejemplo de música en Windows                *
Juego destrucción de misiles                *
                                            *
Santiago Gamboa Ramírez                     *
fecha de emision: 05/03/2018                *
Version: 1.0.0                              *
____________________________________________*
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
#__________/Música
def Song1():
    winsound.PlaySound('song1.wav', winsound.SND_ASYNC)
def Song2():
    winsound.PlaySound('song2.wav', winsound.SND_ASYNC)


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
#__________/Cargar una imagen
CE=cargarImg("logo.gif")
imagen_cancion=Label(C_root,bg='white')
imagen_cancion.place(x=50,y=10)
imagen_cancion.config(image=CE)

#           ____________________________
#__________/funcion para el boton mute
def off():
    winsound.PlaySound(None, winsound.SND_ASYNC)

#           ________________________________________________________________
#__________/funcion para reroducir una cancion y cambiar la imagen del label
def play2():
    off()
    imagen2 = cargarImg("img2.gif")
    imagen_cancion.config(image=imagen2)
    p=Thread(target=Song1,args=())
    p.start()
    root.mainloop()

#           ________________________________________________________________
#__________/funcion para reroducir una cancion y cambiar la imagen del label
def play1():
    off()
    imagen = cargarImg("img1.gif")
    imagen_cancion.config(image=imagen)
    p=Thread(target=Song2,args=())
    p.start()
    root.mainloop()

#           ____________________________
#__________/Crear una nueva ventana
def VentanaJuego(nombre_jugador):
    #Esconder la pantalla sin destruirla
    root.withdraw()
    #Pantalla secundaria
    juego=Toplevel()
    juego.title('EJEMPLO')
    juego.minsize(800,600)
    juego.resizable(width=NO, height=NO)

    C_juego=Canvas(juego, width=800,height=600, bg='light blue')
    C_juego.place(x=0,y=0)

    fondoImg=cargarImg('fondo1.gif')
    F_juego=Label(C_juego, image=fondoImg,bg='light blue')
    F_juego.photo=fondoImg
    F_juego.place(x=0,y=0)

    L_nombre=Label(C_juego, text="Jugador: "+nombre_jugador ,font=('Agency FB',20), fg='light blue', bg='white')
    L_nombre.place(x=10,y=10)

#           ___________________________________
#__________/Variables globales para control de los hilos
    global flag_base_destruida, flag_misil
    flag_base_destruida = False
    flag_misil=True

#           ___________________________________
#__________/Función que ejecuta 15 veces el hilo
    def crearmisil(i):
        global flag_misil , flag_base_destruida
        flag_misil = True
        flag_base_destruida = False      
        
        img_misil=cargarImg('bomba.gif')
        misil=Label(C_juego, image=img_misil,bg='light blue')
        misil.photo=img_misil

       
        posx= 50 * i
        posy=0
        misil.place(x=posx,y=0)
        

#           ______________________________________
#__________/Capturar un click sobre el label bomba
        def onClick(event):
            global flag_misil
            flag_misil=False

        misil.bind('<Button-1>',onClick)

#           ____________________________
#__________/Funcion que mueve un misil
        
        def move_misilAux(misil,posy, posx):
            misil.place(x=posx,y=posy)
            time.sleep(0.02)
            global flag_misil , flag_base_destruida
            if(posy>490):
                flag_misil = False
                flag_base_destruida = True
                return
            if(flag_misil):
                return move_misilAux(misil, posy+2, posx)
        
        move_misilAux(misil, posy, posx)
        if(flag_base_destruida):
            misil.destroy()
            return True
        else:
            misil.destroy()
            return False
            
        
#           ___________________________________
#__________/Funcion que es llamada con el hilo
    def ataque():
        result=True
        i = 0
        while(i<16):
            if(crearmisil(i)):
                result=False
                break
            
            i+=1
        if(result and i>=20):
            print("Felicidades has ganado")
            messagebox.showinfo("Felicidades", "Felicidades has ganado!!")
        else:
            print("Mala suerte has perdido")
            yesno = messagebox.askyesno("Confirmar", "Jugar de nuevo?")
            if(yesno):
                p=Thread(target=ataque,args=())
                p.start()

#           _____________________________
#__________/Volver a la ventana principal
    def back():
        global pausa
        pausa=True
        juego.destroy()
        root.deiconify()

#           __________________________________________
#__________/Se crea un hilo para controlar los misiles
    p=Thread(target=ataque,args=())
    p.start()


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
#           ____________________________
#__________/Botones de ventana principal

Btn_hilos = Button(C_root,text='Juego',command=empezar_juego,fg='white',bg='green')
Btn_hilos.place(x=560,y=470)

Btn_song1 = Button(C_root,text='Cancion 1',command=play1,bg='green',fg='white')
Btn_song1.place(x=100,y=550)

Btn_song2=Button(C_root,text='Cancion 2',command=play2,bg='green',fg='white')
Btn_song2.place(x=200,y=550)

Btn_mute=Button(C_root,text='Parar ',command=off,fg='white',bg='green')
Btn_mute.place(x=300,y=550)

root.mainloop()