import curses_functions
import threading
import time
import zmq



def recv2(socket, time_value):
    time_value = int(time_value) * 10
    i = 0
    while i < time_value:
        try:
            reply = socket.recv(zmq.NOBLOCK)
            try:
                if reply is not None:
                    return str(reply)
            except ValueError:
                continue
        except zmq.ZMQError:
            time.sleep(0.1)
        i -=-1

def main():
    while True:
        tcp_port = 5802
        socket = curses_functions.start_server(5802)
        msg = recv2(socket, 5)
        
         
        timer.start() 
        
        if msg:
            print(msg)
            
        else:
            print("not connected")
        
if __name__ == "__main__":
        main()