from pyfirmata.util import Iterator 
import pyfirmata
import time
import zmq


#region zmq_client
class Setting:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def return_list(self):
        return [self.name, self.value]

    def __str__(self):
        return (self.name + "#" + self.value) 
        
class zc_f:
    # @staticmethod
    # def list_to_str(input_settings):
    #     final = ""
    #     i = 0
    #     while i < len(input_settings):
    #         try:
    #             final += input_settings[i] + "#"
    #         except TypeError:
    #             final += zmq_client_functions.list_to_str(input_settings[i])
    #         i-=-1
    #     return final

    @staticmethod
    def list_to_str(input_settings):
        return (str("#".join(input_settings)) + "#")

    @staticmethod        
    def addSetting(name, value, input_array):
        if input_array == []:
            input_array = ["tunapro"]
            
        # input_array.append(Setting(str(name), str(value)).return_list())
        input_array.append(str(Setting(name, value)))
        return input_array

    @staticmethod
    def send_settings(input_str, tcp_port = 5800):
        connect_server(tcp_port)
        transmit_settings(input_str)

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
#endregion

class rw_f:
    
    @staticmethod
    def map_x(value, min_v, max_v, min_wv, max_wv):
        if value <= max_v and value >= min_v:
            dvd = (max_wv - min_wv) + 1
            i = min_wv 
            dvd2 = max_v / dvd
            dvd3 = dvd2
            
            while i < dvd:
                if value <= dvd2:
                    return i
                    break
                elif value > dvd2: 
                    dvd2 += dvd3 
                i-=-1
                
            if value <= dvd2:
                return max_wv
    
    @staticmethod    
    def get_robo_loc(potan):    
        i1 = rw_f.map_x(potan, 0, 1, 0, 2)
        robo_loc = ""
        while range(3):
            if i1 == 2:
                robo_loc = "left"
                return robo_loc
                break
            elif i1 == 1:
                robo_loc = "middle"
                return robo_loc
                break
            elif i1 == 0:
                robo_loc = "right"
                return robo_loc
                break
            print("Potansiyometre cevap vermiyor")
            time.sleep(0.3)
          
def main():
    tcp_port = 5800
    settings = []

    #region arduino
    board = pyfirmata.ArduinoNano("COM4")

    #region component
    swt1 = board.get_pin("a:1:i")
    pot1 = board.get_pin("a:2:i")
    inp1 = board.get_pin("a:6:i")
    inp2 = board.get_pin("a:7:i")
    but1 = board.get_pin("d:2:i")
    led1 = board.get_pin("d:11:p")
    #endregion
    #region iterator
    iterator = Iterator(board)
    iterator.start()
    time.sleep(0.2)
    #endregion
    #endregion
    
    robo_loc = rw_f.get_robo_loc(pot1.read())
    print(robo_loc)
    settings = zc_f.addSetting("isTest", "True", settings)
    settings = zc_f.addSetting("robot_location", robo_loc, settings)
    settings = zc_f.list_to_str(settings)
    
    
    
    zc_f.connect_server(tcp_port)
    zc_f.transmit_settings(settings)


if __name__ == "__main__":
    print("Started")
    try:
        main()
    except KeyboardInterrupt:
        exit()