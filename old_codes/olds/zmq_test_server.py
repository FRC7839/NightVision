import time
import zmq

class Setting:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def return_list(self):
        return [self.name, self.value]
    
def start_server(tcp_port = 5800):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:" + str(tcp_port))
    return socket

def get_settings(tcp_port = 5800):
    socket = start_server(tcp_port)
    syn = socket.recv()
    socket.send(syn)    

    message_r = str(syn).split("#")

    socket2 = start_server(tcp_port+1)
    syn_ack = socket2.recv()
    pass
    
    if syn_ack == b"OK" :
        print("Got It")
        return message_r
    elif syn_ack == b"RETRY":
        print("Retrying to get settings")
        time.sleep(3)
        get_settings(tcp_port)
# def compute_msg():
    

def find_setting(msg_array, wanted_setting, starting_point=1):
    i = starting_point
    while i < len(msg_array):
        if ((msg_array[i] == wanted_setting) and ((i+1) < len(msg_array))):
            return msg_array[i + 1]
            break
        else:
            pass
        i-=-1
    
    print("The specified setting cannot be found...")

# def main():
#     tcp_port = 5800 
#     settings = get_settings(tcp_port)
#     print(settings)
   
#     robot_location = find_setting(settings, "robot_location")
#     # camera_tolerance = find_setting(settings, "camera_tolerance")
#     isTest = find_setting(settings, "isTest")
#     # print("ROBOT KONUMU: " + robot_location, "KAMERA TOLERANSI: " + camera_tolerance, sep = "\n")
#     print("ROBOT KONUMU: " + robot_location)
    

# if __name__ == "__main__":
#     print("Started")
#     main()