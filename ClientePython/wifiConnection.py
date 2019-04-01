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
    loop = False
    
    keep_log = False
    new_log = []
    log = []
    
    def __init__(self, ip = '192.168.43.200', port = 7070, keep_log = False):
        Thread.__init__(self)
        self.node_address = (ip,port)
        if(keep_log):
            self.keep_log = True
        
    
    def run(self):
        self.loop = True
        while(self.loop):
            if(len(self.pending_mns)>0):
                self.busy = True
                message = ""
                for i in self.pending_mns:
                    message+=i
                    self.pending_mns.remove(i)
                message+="\r"

                if(self.keep_log):
                    self.new_log = [message,""]
                
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

                        if(self.keep_log):
                            self.new_log[1] = response
                    
                    except socket.timeout as error:
                        print("Timeout", 2,"s")
                        self.error=True
                        self.error_list.append(error)

                        if(self.keep_log):
                            self.new_log[1] = str(error)
                        
                    except Exception as a:
                        print(str(a))
                        self.error=True
                        self.error_list.append(a)

                        if(self.keep_log):
                            self.new_log[1] = str(a)
                            
                    finally:
                        sock.close()
                        
                        
                except Exception as e:
                    print(str(e))
                    self.error=True
                    self.error_list.append(e)

                    if(self.keep_log):
                            self.new_log[1] = str(e)

                            
                if(self.keep_log):
                    self.log.append(self.new_log)
                            
                self.busy = False    
            time.sleep(self.interval)

    def stop(self):
        self.loop = False
        
    def send(self,message):
        if(self.loop):
            if(isinstance(message,str) and len(message)>0 and message[-1]==";"):
                self.pending_mns.append(message)
        else:
            print("Start the loop before trying to send messages")

    def readstr(self):
        answer = ""
        for i in self.received_mns:
            response+=i
            self.sending_list.remove(i)
        return response

    def readlist(self):
        temp = self.received_mns.copy()
        self.received_mns = []
        return temp
    
    def errors(self):
        log = ""
        for i in self.error_list:
            log+=i
            self.error_list.remove(i)
        return log
