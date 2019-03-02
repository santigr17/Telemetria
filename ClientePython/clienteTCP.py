# -*- coding: cp1252 -*-
# socket_echo_client.py
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.43.200', 7070)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
message="-1"
while(message!=""):
    try:
        # Send data
        message = input("Ingrese un nuevo comando\n: ")
        if(not ("\r" in message)) : message += "\r"
        sock.sendall(message.encode())

        # Look for the response
        amount_received = 0
        amount_expected = 4
           
        while amount_received < amount_expected:
            data = sock.recv(4)
            amount_received += len(data)
            print('received {!r}'.format(data))

    except Exception as e:
        print("Error tratando de envíar mensaje:\n")
        print(str(e))      
        error = True
        while(error):
            ask = input("¿Desea intentar de nuevo?\n[y = Sí/n = No] :")
            if(ask == 'y'):
               error = False
            elif(ask == 'n'):
               error = False
               message == ""
            else:
               print("Por favor ingresar una opción válida.\ny: Sí, n: No")
        

print('closing socket')
sock.close()
