import curses_functions
import threading
import time
import zmq

global check_cam_port
check_cam_port = 5802

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

def check_server(tcp_port):
    try:
        curses_functions.start_server(tcp_port)
    except:
        isServerStarted = True
    else:
        isServerStarted = False
    return isServerStarted

def main():
    try:
        isServerStarted = check_server(check_cam_port)
    except:
        isServerStarted = False
    
    sendnt = []
    sendnt.append("#")
    sendnt.append(str(curses_functions.Setting("is_network_tables_started", str(True))))
    
    sendnt = curses_functions.list_to_str(sendnt)
    
    if isServerStarted:
        try:
            socket = curses_functions.connect_server(check_cam_port)
            socket.send(str.encode(str(sendnt)))
        except:
            pass
    
    print("tunapro")



if __name__ == "__main__":
    while True:
        main()
        time.sleep(0.3)
        
        
# def main():
#     tcp_port = 5802
#     isServerStarted = check_server(tcp_port)
#     try:
#         if isServerStarted:
#             socket = curses_functions.connect_server(tcp_port)
#             socket.send(b"naber")
#     except:
#         print("NOOOOOOOOOOOOOOOOOO")
    
#     print("tunapro")

# isServerStarted = check_server(tcp_port)
# socket = curses_functions.connect_server(tcp_port)




# def main():
#     tcp_port = 5802
#     try:
#         isServerStarted = check_server(tcp_port)
#     except:
#         isServerStarted = False
        
#     sendnt = "naber"
    
#     if isServerStarted:
#         try:
#             socket = curses_functions.connect_server(tcp_port)
#         except:
#             socket.send(str.encode(str(sendnt)))
#         else:
#             socket.send(str.encode(str(sendnt)))

#     print("tunapro")