import socket

class ServerFunctions:
    
    @staticmethod
    def dnm(deneme, deneme2):
        deneme += deneme2
        return deneme
    
    @staticmethod
    def start_server(tcp_port, localhost="127.0.0.1"):
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # big funny
        socket1.bind((localhost, tcp_port))
        return socket

    @staticmethod
    def connect_server(tcp_port, localhost="127.0.0.1"):
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((localhost, tcp_port))
        return socket1
    
    @staticmethod
    def recv1(socket1, time):
        conn, addr = socket1.accept()
        conn.settimeout(time)
        message = conn.recv(1024)
        message.decode()
        return message

    @staticmethod
    def recv_with_timer(socket1, time):
        start_time = timeit.default_timer()
        recv1(socket1, time)
        elapsed = timeit.default_timer() - start_time
        return [rv, elapsed]    
    
    @staticmethod
    def send1(socket1, message):
        message = bytes(message, "UTF-8")
        socket1.send(message)
        
    
    





