import numpy as np
import pyfirmata
import socket
import timeit
import math
import json
import time
import cv2
import zmq
import os

# Siyo dc gel nf

#region global
global cam_curses_port1
global cam_curses_port2
global led_control_port
global is_input_started
global setting_names
global all_errors
global file_lc
global file_s
global max_v
global wait_time_for_get_key


setting_names = ["isTunaPro", "Robot Location", "Camera Tolerance", "Waiting Period", "Autonomous Mode"]
wait_time_for_get_key = 0.11
cam_curses_port1 = 5800
cam_curses_port2 = 5801
is_input_started = 5802
led_control_port = 5803
file_s = "settings.json"
file_lc = "led_control.json"
max_v = 30



all_errors = {
        "READ_ERROR" : "InputP ERROR: Dosya " + file_s+ " okunamıyor...",
        "ARD_CONN_ERR" : "InputP ERROR: Arduino'ya baglanilamiyor...",
        "ARD_POT_ERR" : "InputP ERROR: Potansiyometre cevap vermiyor...",
        "FILE_NOT_FOUND" : "InputP ERROR: JSON Dosyasi yok ve olusturulamiyor...",
        "SERVER_NOT_STRTD" : "InputP ERROR: Server baslatilamadi...",       
    }
#endregion

class ArduinoFunctions:
    @staticmethod
    def old_led_write(led, ledi, st):
        led.write(st/50)
        st = 1 - st
        ledi.write(st)
        
    @staticmethod
    def led_write(led1, out1, st, gnd = True):
        led1.write(st/50)
        if gnd == True:
            st = 1 - st
        out1.write(st)
        
    @staticmethod
    def import_arduino(COM1="COM3", COM2="COM4"):
        if os.name == "nt":
            try:
                try:
                    board = pyfirmata.ArduinoNano(COM1)
                except:
                    board = pyfirmata.ArduinoNano(COM2)
            except:
                print("CANNOT CONNECT TO ARDUINO")
                exit()

        elif os.name == "posix":
            try:
                try:
                    board = pyfirmata.ArduinoNano("/dev/ttyUSB0")
                except:
                    board = pyfirmata.ArduinoNano("/dev/ttyUSB1")

            except:
                print("Arduino connection failed please try again...")
                exit()

        return board

    @staticmethod
    def map_x(value, min_v, max_v, min_wv, max_wv):
        if value is not None:
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
                    i -= -1

                if value <= dvd2:
                    return max_wv
        else:
            ### ERROR ###
            print("InputP: Pyfirmata değer döndürme problemi, Arduino'yu yeniden bağlamayı deneyin")
            return "ERROR"
        
    @staticmethod
    def map_xi(value, min_v, max_v, min_wv, max_wv):
        if value is not None: 
            value = max_v - value
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
                    i -= -1

                if value <= dvd2:
                    return max_wv
        else:
            ### ERROR ###
            print("InputP: Pyfirmata değer döndürme problemi, Arduino'yu yeniden bağlamayı deneyin")
            return "ERROR"
        
 
def key_get(
    digital_input1,
    digital_input2,
    analog_input1,
    wait_time=0.11,
    func=None,
    *args
    ):
    
    key = None
    msg = None

    but1 = None
    but1_p = None

    but2 = None
    but2_p = None
    
    pot1_p = ArduinoFunctions.map_xi(analog_input1.read(), 0, 1, 0, 30)
    pot1 = pot1_p

    while True:

        if (but1 != but1_p) and but2 > 0 and (not (but2 > 0)):
            but1 = but1_p
            key = "button0"

        elif (but2 != but2_p) and but2 > 0 and (not (but1 > 0)):
            but2 = but2_p
            key = "button1"
        
        elif (pot1_p != pot1):
            key = pot1
        
        if func is not None:
            ##
            start_t = timeit.default_timer()
            ##
            
            rv = func(*args)
            
            ##
            elapsed = timeit.default_timer() - start_t
            ##
            
            if elapsed > wait_time:
                pass
            
            else:
                time.sleep(wait_time - elapsed)
            
        else:
            time.sleep(wait_time)
            
        if key is not None:
            return key, rv

        but1 = digital_input1.read()
        but2 = digital_input2.read()
        pot1 = ArduinoFunctions.map_xi(analog_input1.read(), 0, 1, 0, 30)



    @staticmethod
    def get_robot_location_from_potansiometer_input(potan, max_v):
        i1 = ArduinoFunctions.map_x(potan, 0, max_v, 0, 2)
        robo_loc = ""
        while range(3):
            if i1 == 0:
                robo_loc = "LEFT"
                return robo_loc
                break
            elif i1 == 1:
                robo_loc = "MIDDLE"
                return robo_loc
                break
            elif i1 == 2:
                robo_loc = "RIGHT"
                return robo_loc
                break
            time.sleep(0.3)

# region old
           
# class oldDbFunctions:
#     @staticmethod
#     def find_setting(msg_array, wanted_setting, starting_point=1, return_number=False):
#         i = starting_point
#         while i < len(msg_array):
#             if (msg_array[i] == wanted_setting) and ((i + 1) < len(msg_array)):
#                 if return_number:
#                     return i
#                 else:    
#                     return msg_array[i + 1]
#             else:
#                 pass
#             i -= -1

#         print("The specified setting cannot be found...")

#     @staticmethod
#     def addSetting(name, value, input_array):
#         if input_array == []:
#             input_array = ["tunapro"]
        
#         input_array.append(str(Setting(name, value)))
#         return input_array
    
#     @staticmethod
#     def list_to_str(input_settings):
#         return str("#".join(input_settings)) + "#"

#     @staticmethod 
#     def str_to_list(input_str):
#         return input_str.split("#")

#     @staticmethod
#     def fix_settings_on_txt(file):
#         setting_to_write = "#istunapro#True#"
            
#         if DbFunctions.read_setting_on_txt(file=file) is None:
#             try:
#                 with open(file,"w") as file2:
#                     file2.write(setting_to_write)
#             except:
#                 with open(file,"w+") as file2:
#                     file2.write(setting_to_write)
            
#             Eğer dosya yoksa oluştur ##
        
        
#         else:

#             DOSYA OKUMA ########33

#             with open(file, "r") as file1:
#                 settings = file1.read()

#             with open(file, "r") as file1:
#                 settings = file1.read()
            
#             error = False
                
#             s_settings = []
#             settings = DbFunctions.str_to_list(settings)
            
#             Normal okuma ##


#             for setting in settings:
#                 try:
#                     int(setting)
#                 except:
#                     pass
#                 else:
#                     setting = ""
                
#                 if setting == "#" or setting == "True" or setting == "False" or setting == "":
#                     pass
#                 else:
#                     s_settings.append(setting)

#             Txt dosyası "#", "True", "False" gibi anahtar kelimelerden arındırlıp sadece ##
#             setting adları alındı (Aynısınan birden fazla olup olmadığını görmek için) ##


#             for i in range(len(s_settings)):
#                 for i2 in range(len(s_settings)):
#                     if s_settings[i] == s_settings[i2] and i > i2:
#                         error = True
            
#             Aynı settingten birden fazla olup olmadığının kontolü

            
#             if error == True:
#                 try:
#                     with open(file,"w") as file2:
#                         file2.write(setting_to_write)
#                 except:
#                     with open(file,"w+") as file2:
#                         file2.write(setting_to_write)

#                 Eğer aynı setting birden fazla kez girilmişse fazla girilenleri yok ediyor (umarım testleri yapmak için çok zamanım olmadı)



#     @staticmethod
#     def write_setting_to_txt(input_str, file="settings.txt", reset=False):
#         if reset == True:
#             try:
#                 with open(file, "w") as file2:
#                     file2.write("")
#             except:
#                 with open(file, "w+") as file2:
#                     file2.write("")

#             write_setting_to_txt(input_str, file, reset=False)
    
#         else:    
#             try:
#                 with open(file, "w") as file1:
#                     file1.write(input_str)
#             except:
#                 with open(file, "w+") as file1:
#                     file1.write(input_str)

             
#     @staticmethod
#     def read_setting_on_txt(wanted_setting=None, file = "settings.txt"):
#         try:
#             with open(file, "r") as file1:
#                 output = file1.read()
#         except:
#             return None
        
#         if wanted_setting is not None:
#             try:
#                 output = output.split("#")
#                 output = DbFunctions.find_setting(output, wanted_setting)
#             except:
#                 return None
        
#         return output

#     @staticmethod
#     def save_settings(saving_setting, saving_value, path):
#         DbFunctions.fix_settings_on_txt(path)
#         settings = DbFunctions.read_setting_on_txt(file=path)
#         settings = DbFunctions.str_to_list(settings)
#         nows = DbFunctions.find_setting(settings, saving_setting, return_number=True)
        
#         if nows is not None:
#             nows = int(nows)
#             settings[nows] = saving_setting
#             settings[nows+1] = str(saving_value)
#             settings = DbFunctions.list_to_str(settings)
#             DbFunctions.write_setting_to_txt(settings, file=path)
        
#         else:
#             settings[len(settings)-1] = saving_setting
#             settings.append(str(saving_value))
#             settings = DbFunctions.list_to_str(settings)
#             DbFunctions.write_setting_to_txt(settings, file=path)


#     @staticmethod
#     def get_settings():
#         return DbFunctions.read_setting_on_txt(file=path)

# endregion
        
class DbFunctions:

        ## DONE
    @staticmethod
    def write_settings_to_json(input_dictionary=None, file=file_s, reset=False):
        if reset == True:
            settings = {}
            
            if input_dictionary == None and file == file_s:
                for setting_name in setting_names:
                    settings[setting_name] = None  
            
            else:
                settings = input_dictionary 
            
            try:
                input_dictionary = settings 
                with open(file, "w+") as p: 
                    json.dump(settings, p, indent=4)    
                    
            except:
                print("File not created and cannot be created...")
                return "ERROR"
            
            DbFunctions.write_settings_to_json(input_dictionary, file, reset=False)
    
        else:    
            try:
                with open(file, "w+") as p: 
                    json.dump(input_dictionary, p, indent=4)    
                    
            except:
                ### ERROR ###
                print("File not created and cannot be created...")
                return "ERROR"
    
    ## DONE    
    @staticmethod
    def read_settings_on_json(wanted_setting=None, file = file_s):
        try:
            with open(file, "r") as p: 
                settings = json.load(p)
        except:
            ### ERROR ###
            print("InputP: Cannot read " + file_s + "...")
            return "ERROR"

        if wanted_setting is not None:
            try:
                output = settings[wanted_setting]
            except:
                return None
        
        else:
            output = settings     
            
        return output


    @staticmethod
    def save_settings(settings, file=file_s):
        c_s = DbFunctions.read_settings_on_json(file=file)
        if c_s is None or c_s == "" or c_s == "ERROR":
            DbFunctions.write_setting_to_json(file=file, reset=True)            
        
        if settings is None:
            settings = c_s
        del c_s
        
        for setting_name in setting_names:
            try:
                settings[setting_name]
            except:
                settings[setting_name] = None    
        
        DbFunctions.write_settings_to_json(settings, file=file)
        
    

    @staticmethod
    def get_setting(file=file_s, setting_name=None):
        if (not (setting_name in setting_names)) and setting_name is not None and file == file_s:
            ### ERROR ###
            print("SYNTAX ERROR TUNA GERIZEKALI")
            return "ERROR"
            
        c_s = DbFunctions.read_settings_on_json(file=file)
        
        if c_s is None or c_s == "ERROR" or c_s == "":
            DbFunctions.write_settings_to_json(file=file, reset=True)
        
        else:
            # eğer setting yoksa ekleniyor
            if file == file_s:
                for setting_name2 in setting_names:
                    try:
                        c_s[setting_name2]
                    except KeyError:
                        c_s[setting_name2] = None   
            
            
            DbFunctions.write_settings_to_json(c_s, file=file)
        
        
        c_s = DbFunctions.read_settings_on_json(file=file)
        
        if setting_name is not None:
            try:
                output = c_s[setting_name]
            except:
                ### ERROR ###
                print("SETTING NOT FOUND IN THE JSON FILE")
                return "ERROR"

            output = c_s[setting_name]
            return output    
        
        else:
            output = c_s
            return output    

        
class ServerFunctions:
    @staticmethod
    def check_server(port=is_input_started):
        try:
            sockettemp = ServerFunctions.start_server(port)
            sockettemp.close()
        except:
            print("Server Opened")
            return True
        else:
            print("Server Not Opened")
            return False

    @staticmethod
    def start_server(port=is_input_started):
        s = socket.socket()
        time.sleep(0.1)
        s.bind(("", port))
        time.sleep(0.1)
        s.listen(5)
        time.sleep(0.1)
        return s    
        
    @staticmethod
    def recv_with_timer(s, time = 0.1):
        start_t = timeit.default_timer()
        s.settimeout(time)
        try:
            conn, address = s.accept()
            message = conn.recv(1024)
        except:
            return None
        else:
            message.decode()
            message = str(message)
            message = message[2:-1]
            try:
                with open("recieve.txt", "w") as writer:
                    print(message)
                    writer.write(message)
            except:
                with open("recieve.txt", "w+") as writer:
                    print(message)
                    writer.write(message)
        elapsed = timeit.default_timer() - start_t
        return [rv, elapsed]

    @staticmethod
    def recieve(s, time):
        s.settimeout(time)
        
        try:
            conn, address = s.accept()

            message = conn.recv(1024)

        except:
            return None
            
        else:
            message.decode()

            message = str(message)

            message = message[2:-1]

            try:
                with open("recieve.txt", "w") as writer:
                    print(message)
                    writer.write(message)
            except:
                with open("recieve.txt", "w+") as writer:
                    print(message)
                    writer.write(message)

    @staticmethod
    def connect_to_server(port):
        s = socket.socket()
        try:
            s.connect(("127.0.0.1", port))
            return s
        except:
            return
        
    @staticmethod
    def send_to_server(s, message):
        try:        
            s.send(str.encode(str(message)))
        except:
            ### ERROR ###
            print("InputP: Bunu okuyorsan Kayra big gay")

    @staticmethod
    def get_ipaddr():
        if os.name == "nt":
            return socket.gethostbyname(socket.gethostname())

        elif os.name == "posix":
            ipaddress = os.popen(
                "ifconfig wlan0 \
                        | grep 'inet addr' \
                        | awk -F: '{print $2}' \
                        | awk '{print $1}'"
            ).read()

            return ipaddress


class CameraFunctions:
    @staticmethod
    def detect_targets(capture):
        kernel = np.ones((3, 3), np.uint8)
        kernel2 = np.ones((13, 13), np.uint8)

        hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)
        lower_green = np.array([45, 110, 105])
        upper_green = np.array([102, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        cv2.imshow("sl", mask)

        filter2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        filter3 = cv2.morphologyEx(filter2, cv2.MORPH_CLOSE, kernel2)

        _, contours, _ = cv2.findContours(
            filter3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        return contours

    @staticmethod
    def draw_rectangle(_frame, contours):
        if not (len(contours)):
            return _frame

        contour = contours[0]

        rect = cv2.minAreaRect(contour)
        box_points = cv2.boxPoints(rect)
        box1 = np.int0(box_points)
        cv2.drawContours(_frame, [box1], 0, (0, 0, 255), 2)
        return _frame

    @staticmethod
    def cnt_test(cnt):
        rect = cv2.minAreaRect(cnt)

        # rect_width = min(rect[1][0], rect[1][1])
        # rect_height = max(rect[1][0], rect[1][1])
        # rect_angle = rect[2]

        box = cv2.boxPoints(rect)

        corner1x, corner1y = box[0]
        corner2x, corner2y = box[1]
        corner3x, corner3y = box[2]
        corner4x, corner4y = box[3]

        x_list = list((corner1x, corner2x, corner3x, corner4x))
        x_list.sort()
        y_list = list((corner1y, corner2y, corner3y, corner4y))
        y_list.sort()

        rect_width = abs(x_list[0] - x_list[2])
        rect_height = abs(y_list[0] - y_list[2])

        horizontal_friction = False
        vertical_friction = False

        for x_coord in x_list:
            horizontal_friction = bool(not (5 < x_coord < 635))
            if horizontal_friction:
                break

        for y_coord in y_list:
            vertical_friction = bool(not (5 < y_coord < 475))
            if vertical_friction:
                break

        if (
            rect_width
            and rect_height
            and not horizontal_friction
            and not vertical_friction
            and cv2.contourArea(cnt) > 250
        ):
            rect_ratio = rect_width / rect_height
            if 1 > rect_ratio > 0:
                return True, "Loading Area"
            elif 1 <= rect_ratio <= 10:
                return True, "Target Area"
        else:
            return False, ""

    @staticmethod
    def calculate_errors(contours):
        try:
            cnt = contours[0]
        except IndexError:
            return False, 0
        rect = cv2.minAreaRect(cnt)
        box_p = cv2.boxPoints(rect)
        box = np.int0(box_p)

        moment1 = cv2.moments(box)
        center1x = int(moment1["m10"] / moment1["m00"])
        center1y = int(moment1["m01"] / moment1["m00"])
        camera_height = 40
        target_height = 300
        camera_angle = 75
        target_angle = (180 - center1y) / 180 * 43.30
        distance = (target_height - camera_height) / math.tan(
            camera_angle + target_angle
        )
        y_error = 320 - center1x
        return True, y_error, distance
