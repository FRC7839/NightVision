import zmq
import pyfirmata
import time

def main():
    settings = []
    settings = server_functions.addSetting("robot_location", "right", settings)
    settings = server_functions.list_to_str(settings)
    tcp_port = 5800
    server_functions.send_settings(settings)


class Setting:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def return_list(self):
        return [self.name, self.value]


class server_functions:
    @staticmethod
    def list_to_str(input_settings):
        final = ""
        i = 0
        while i < len(input_settings):
            try:
                final += input_settings[i] + "#"
            except TypeError:
                final += server_functions.list_to_str(input_settings[i])
            i-=-1
        return final

    @staticmethod        
    def addSetting(name, value, input_array):
        if input_array == []:
            input_array = ["tunapro"]
            
        input_array.append(Setting(str(name), str(value)).return_list())
        return input_array

    @staticmethod
    def send_settings(input_str, tcp_port = 5800):
        server_functions.connect_server(tcp_port)
        server_functions.transmit_settings(input_str)

    @staticmethod        
    def connect_server(tcp_port = 5800):
        global socket
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:" + str(tcp_port))

    @staticmethod
    def transmit_settings(input_str):    
        input_str = str.encode(input_str)
        socket.send(input_str)
       
        
if __name__ == "__main__":
    print("Started")
    main()