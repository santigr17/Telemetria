from threading import Thread
import threading
import socket
import time

class NodeMCU(Thread):
    node_address = ()
    pending_mns = []
    received_mns = []
    error_list = []
    busy = False
    error = False
    interval = 0.050
    
    def __init__(self, address = '192.168.43.200', port = 7070 ):
        Thread.__init__(self)
        self.start()
    
    def run(self):
        while(True):
            if(len(self.pending_mns)>0):
                self.busy = True
                message = ""
                for i in self.pending_mns:
                    message+=i
                    self.pending_mns.remove(i)
                message+="\r"
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    sock.connect(self.node_address)
                    
                    try:
                        sock.sendall(mns.encode())
                        data=b''
                        response = ""
                        while data != b'\r':
                            data = sock.recv(1)
                            response+=data.decode("utf-8")
                            
                        self.received_mns.append(response)
                        
                    except socket.timeout as error:
                        print("Timeout", 2,"s")
                        self.error=True
                        self.error_list.append(error)
                        
                    except Exception as a:
                        print(str(a))
                        self.error=True
                        self.error_list.append(a)
                        
                    finally:
                        sock.close()
                        
                        
                except Exception as e:
                    print(str(e))
                    self.error=True
                    self.error_list.append(e)
                    
                self.busy = False    
            time.sleep(self.interval)
        
    def send(self,message):
        mns_format = False
        if(isinstance(message,str) and message[-1]==";"):
            self.pending_mns.append(message)
            mns_format = True
        return mns_format

    def read(self):
        answer = ""
        for i in self.received_mns:
            response+=i
            self.sending_list.remove(i)
        return response
