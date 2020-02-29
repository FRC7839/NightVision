import numpy as np
import pyfirmata
import socket
import timeit
import math
import json
import time
import cv2
import sys  
import os

if str(sys.platform).startswith("win"):
    import serial.tools.list_ports

# region global
global wait_time_for_get_key
global setting_defaults
global setting_names
global lc_defaults
global all_errors
global all_infos
global lc_names
global file_lc
global file_s
global max_v

global INTERNAL_KEY_GET_FUNC_ERR
global SERVER_ALREADY_STARTED_ERR
global SERVER_NOT_STARTED_ERR
global MM_CANNOT_START_ERR
global INTERNAL_SYNTAX_ERR
global WRITE_ERR
global ARDUINO_INPUT_ERR
global ARDUINO_CONN_ERR
global CANT_CONNECT_ERR
global READ_ERR

global ARDUINO_CONNECTION_SUCCESS
global ARDUINO_CONNECTING

global arduino_menu_value
global camera_menu_value
global main_menu_value
global info_menu_value
global ip_menu_value

INTERNAL_KEY_GET_FUNC_ERR = "INTERNAL_KEY_GET_FUNCTION_ERROR"
SERVER_ALREADY_STARTED_ERR = "SERVER_ALREADY_STARTED_ERROR"
ARDUINO_CONN_LOST = "ARDUINO_CONNECTION_LOST"
MM_CANNOT_START_ERR = "MM_CANNOT_START_ERROR"
INTERNAL_SYNTAX_ERR = "INTERNAL_SYNTAX_ERROR"
ARDUINO_INPUT_ERR = "ARDUINO_INPUT_ERROR"
CANT_CONNECT_ERR = "CAN_NOT_CONNECT_TO_SERVER"
SERVER_NOT_STARTED_ERR = "SERVER_NOT_STARTED"
ARDUINO_CONN_ERR = "ARDUINO_INPUT_ERROR"
WRITE_ERR = "FILE_NOT_FOUND_ERROR"
READ_ERR = "READ_ERROR"

ARDUINO_CONNECTION_SUCCESS = "ARD_CONN_SUCCESS"
ARDUINO_CONNECTING = "ARD_CONNECTING"

# settings.json dosyasini kontrol edebilmek icin arayuzde ayarlanacak ayarlar
setting_names = [
    "isTunaPro",
    "Robot Location",
    "Camera Tolerance",
    "Waiting Period",
    "Autonomous Mode",
    "Team Number",
    "Camera Offset"
]

setting_defaults = [
    True,
    "MIDDLE",
    "15",
    "0",
    "1",
    "7839",
    "666"
]

lc_names = [
    "Led Status",
    "Match Mode Status"
]

lc_defaults = [
    True,
    False
]

# Arduinodan deger aldiktan sonraki bekleme suresi
wait_time_for_get_key = 0.115

# Robot ayarlarinin kaydedilecegi dosya
file_s = "settings.json"

# Led kontrulunun yapilmasini saglayacak dosya ama muhtemelen kullanmayacagiz
file_lc = "led_control.json"

# Potansiyometreden okunan degerin kaca bolunecegi
# Kamera toleransini degistirmek ve ayarlarin hassasiyetini arttirmak icin arttirilabilir
# Ama muhtemelen problem cikarir denemedim ve onermiyorum
max_v = 30

# Errorler
all_errors = {
    "SERVER_ALREADY_STARTED_ERROR" : "InputP ERROR: Sunucu daha once baslatildi.",
    "SERVER_NOT_STARTED": "InputP ERROR: Server baslatilamadi.",
    "CAN_NOT_CONNECT_TO_SERVER": "InputP ERROR: Sunucuya baglanilamiyor",
    "INTERNAL_KEY_GET_FUNC_ERROR": "InputP ERROR: Key_get fonksiyonuna girilen fonksiyonda bilinmeyen hata",
    "INTERNAL_SYNTAX_ERROR": "InputP ERROR: Tuna, kodunda hata var.",
    "MM_CANNOT_START_ERROR": "InputP ERROR: Mac modu baslatilamiyor.",
    "ARDUINO_INPUT_ERROR": "InputP ERROR: Pyfirmata cevap vermiyor.",
    "FILE_NOT_FOUND_ERROR": "InputP ERROR: JSON Dosyasi yok ve olusturulamiyor.",
    "READ_ERROR": "InputP ERROR: JSON dosyasi okunamiyor.",
    "ARDUINO_CONNECTION_ERROR": "InputP ERROR: Arduino'ya baglanilamiyor.",
    "ARDUINO_CONNECTION_LOST": "InputP ERROR: Arduino çıkarıldı"
}

all_infos = {
    "ARD_CONN_SUCCESS" : "InputP INFO: SUCCESSFUL", 
    "ARD_CONNECTING" : "InputP INFO: Importing Arduino"
}

arduino_menu_value = 2
camera_menu_value = 3
main_menu_value = 0
info_menu_value = 4
ip_menu_value = 1

# endregion


### ALL ERROR PROOF ###
class ArduinoFunctions:
    @staticmethod
    def check_ports():
        try:
            if str(sys.platform).startswith("linux") or str(sys.platform).startswith("cygwin"):
                dev = os.popen("ls /dev/tty* | grep USB").read()
                if dev == "":
                    return all_errors[ARDUINO_CONN_LOST]
                
                else:
                    dev = dev.split("\n")
                    # for i in range(len(dev)):
                    #     COMS[i] = COMS[i].split(":")[0]
                    return dev    
                
            elif str(sys.platform).startswith("win"):
                ports = serial.tools.list_ports.comports()

                COMS = []

                for port, desc, hwid in sorted(ports):
                    COMS.append("{}: {} [{}]".format(port, desc, hwid))

                for i in range(len(COMS)):
                    COMS[i] = COMS[i].split(":")[0]
                
                if len(COMS) > 0:
                    return COMS

                else:
                    return all_errors[ARDUINO_CONN_LOST]
                
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM LED_WRITE FUNCTION")
            return output_e
    
    @staticmethod
    def led_write(led1, out1, st, gnd=True):
        try:
            led1.write(st)
            if gnd == True:
                st = 1 - st
            out1.write(st)
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM LED_WRITE FUNCTION")
            return output_e

    ### ERROR PROOF ### (Raise)
    @staticmethod
    def import_arduino(com_ports):
        try:
            if type(com_ports) == list:
                for i in range(len(com_ports)):
                    try:
                        board = pyfirmata.ArduinoNano(str(com_ports[i]))

                    except:
                        pass
                    
                    else:
                        return board
            
            elif type(com_ports) == str:
                try:
                    board = pyfirmata.ArduinoNano(str(com_ports[i]))
                    
                except:
                    pass                
                
                else:
                    return board
                
            else:
                ### ERROR ###
                output_e = all_errors[INTERNAL_SYNTAX_ERR]
                print(output_e + " # FROM IMPORT_ARDUINO FUNCTION")
                return output_e                
    
            ### ERROR ###
            output_e = all_errors[ARDUINO_CONN_ERR]
            print(output_e)
            return output_e

        except:
            ### ERROR ###
            output = all_errors[INTERNAL_SYNTAX_ERR]
            print(output + " # FROM IMPORT_ARDUINO FUNCTION")
            return output


    ### ERROR PROOF ### (Raise)
    @staticmethod
    def map_x(value, min_v, max_v, min_wv, max_wv):
        try:
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
                output_e = all_errors[ARDUINO_INPUT_ERR]
                print(output_e)
                return output_e
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM MAP_X FUNCTION")
            return output_e

    ### ERROR PROOF ### (Raise)
    @staticmethod
    def map_xi(value, min_v, max_v, min_wv, max_wv):
        try:
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
                output_e = all_errors[ARDUINO_INPUT_ERR]
                print(output_e)
                return output_e
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM MAP_XI FUNCTION")
            return output_e

    ### ERROR PROOF ### (Handle and Raise)
    @staticmethod
    def key_get(
        digital_input1, digital_input2, analog_input1, wait_time=0.11, func=None, *args
    ):
        try:
            key = None
            rv = None

            but1 = digital_input1.read()
            but1_p = False

            but2 = digital_input2.read()
            but2_p = False

            # Pyfirmata librarysi bazen arduinoyu basarili bir sekilde import etesine ragmen iterator hatasi verip input alamiyor
            pot1_p = ArduinoFunctions.map_x(analog_input1.read(), 0, 1, 0, 30)
            pot1 = pot1_p

            while True:

                # O yuzden burada okunan degerin None olup olmadigini kontrol etmem gerekiyor
                ### GOT ERROR ###
                if str(pot1_p).startswith("InputP"):
                    ### ERROR ###
                    pot1 = str(pot1_p)
                    print(pot1 + " # FROM KEY_GET FUNCTION")
                    return pot1, None

                elif (but1 != but1_p) and but1 > 0 and (not (but2 > 0)):
                    but1 = but1_p
                    key = "button0"

                elif (but2 != but2_p) and but2 > 0 and (not (but1 > 0)):
                    but2 = but2_p
                    key = "button1"

                elif pot1_p != pot1:
                    key = pot1

                if func is not None:
                    #
                    start_t = timeit.default_timer()

                    try:
                        rv = func(*args)

                    except:
                        ### ERROR ###
                        rv = all_errors[INTERNAL_KEY_GET_FUNC_ERR]
                        print(rv)
                        return None, rv
                    
                    else:
                        if type(rv) == str and rv.startswith("InputP"):
                            key = None
                            return key, rv
                    
                    elapsed = timeit.default_timer() - start_t
                    #

                    if elapsed > wait_time:
                        pass

                    else:
                        time.sleep(wait_time - elapsed)

                else:
                    time.sleep(wait_time)

                if key is not None:
                    ### ERROR ###
                    try:
                        if str(rv).startswith("InputP"):
                            rv = str(rv)
                            print(rv + " # FROM KEY_GET FUNCTION")
                    except:
                        pass    
                    
                    return key, rv

                but1 = digital_input1.read()
                but2 = digital_input2.read()
                pot1 = ArduinoFunctions.map_x(analog_input1.read(), 0, 1, 0, 30)
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM KEY_GET FUNCTION")
            return output_e

    @staticmethod
    def encoder_key_get(
        outputA,
        outputB,
        but1,
        wait_time,
        func = None,
        *args
    ):
        try:
            aLastState = outputA.read()
            counter = 0
            key = None
            rv = None
            # Normalde encoder icin caldigim kodda vardi. Silmeyi dusundum ama encoder icin biraz sikinti yaratiyor. cidden
            
            if aLastState is None:
                key = all_errors[ARDUINO_INPUT_ERR]
                        
            while True: 
                aState = outputA.read()
                
                
                if (aState != aLastState):
                    
                    if (outputB.read() != aState):
                        counter-=-1
                        
                        if((counter % 2) == 0):
                            # print("Position: " + counter + "LOCATION: RIGHT" + swt2.read())
                            key = "button+1"
                            
                    else:
                        counter+=-1
                        
                        if((counter % 2) == 0):
                            # print("Position: " + counter + "LOCATION: LEFT" + swt2.read())
                            key = "button-1"
                            
                            
                    aLastState = aState; 
                
                
                if (but1.read() == 0 and not (counter == 0)):
                    counter = 0;
                    # print("Position: " + counter + "LOCATION: MIDDLE" + swt2.read())
                    key = "button0"

                # region fonksiyon
                if func is not None:
                    start_t = timeit.default_timer()

                    try:
                        rv = func(*args)

                    except:
                        ### ERROR ###
                        key = None
                        rv = all_errors[INTERNAL_KEY_GET_FUNC_ERR]
                        print(rv)
                        return key, rv
                    
                    else:
                        if type(rv) == str and rv.startswith("InputP"):
                            key = None
                            return key, rv
                    
                    elapsed = timeit.default_timer() - start_t
                    

                    if elapsed < wait_time:
                        # time.sleep(wait_time - elapsed)
                        pass
    
                else:
                    # time.sleep(wait_time)
                    if key is not None:
                        return key, None

                # endregion
                
                # time.sleep(wait_time)
                
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM KEY_GET FUNCTION")
            return output_e, None
                
        
    ### ERROR PROOF ### (Handle)
    @staticmethod
    def get_robo_loc_from_inp(potan, max_v):
        try:
            i1 = ArduinoFunctions.map_x(potan, 0, max_v, 0, 2)

            ### GOT ERROR ###
            if str(i1).startswith("InputP"):
                ### ERROR ###
                i1 = str(i1)
                print(i1 + " # FROM GET_ROBO_LOC FUNCTION")
                return i1

            elif i1 == 0:
                return "LEFT"

            elif i1 == 1:
                return "MIDDLE"

            elif i1 == 2:
                return "RIGHT"

        except:
            ### ERROR ###
            output = all_errors[INTERNAL_SYNTAX_ERR]
            print(output + " # FROM GET_ROBO_LOC FUNCTION")
            return output


### ALL ERROR PROOF ###
class DbFunctions:

    ### ERROR PROOF ### (Raise)
    @staticmethod
    def write_settings_to_json(input_dictionary=None, file=file_s, reset=False):
        try:
            if reset == True:
                

                if input_dictionary is None and file == file_s:
                    settings = {}
                    
                    for i in range(len(setting_names)):
                        try:
                            settings[setting_names[i]]
                        except KeyError:
                            settings[setting_names[i]] = setting_defaults[i]
                
                elif input_dictionary is None and file == file_lc:
                    lc_set = {} 
                    
                    for i in range(len(lc_names)):
                        try:
                            lc_set[lc_names[i]]
                        except KeyError:
                            lc_set[lc_names[i]] = lc_defaults[i]
                            
                    settings = lc_set

                else:
                    settings = input_dictionary

                try:
                    input_dictionary = settings
                    with open(file, "w+") as p:
                        json.dump(settings, p, indent=4)

                except:
                    ### ERROR ###
                    output_e = all_errors[WRITE_ERR]
                    print(output_e)
                    return output_e

                DbFunctions.write_settings_to_json(input_dictionary, file, reset=False)

            else:
                try:
                    with open(file, "w+") as p:
                        json.dump(input_dictionary, p, indent=4)

                except:
                    ### ERROR ###
                    output_e = all_errors[WRITE_ERR]
                    print(output_e)
                    return output_e

        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM WRITE_SETTINGS FUNCTION")
            return output_e

    ### ERROR PROOF ### (Raise)
    @staticmethod
    def read_settings_on_json(wanted_setting=None, file=file_s):
        try:
            try:
                with open(file, "r") as p:
                    settings = json.load(p)
            except:
                ### ERROR ###
                output_e = all_errors[READ_ERR]
                print(output_e)
                return output_e

            if wanted_setting is not None:
                try:
                    output = settings[wanted_setting]
                except:
                    return None

            else:
                output = settings

            return output

        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM READ_SETTINGS FUNCTION")
            return output_e

    ### ERROR PROOF ### (Handle)
    @staticmethod
    def save_settings(file=file_s, *args):
        try:
            for settings in args:
                c_s = DbFunctions.read_settings_on_json(file=file)
                
                if type(c_s) == str:
                    if c_s is None or c_s == "" or c_s.startswith("InputP"):
                        rv = DbFunctions.write_setting_to_json(file=file, reset=True)

                        if str(rv).startswith("InputP"):
                            ### ERROR ###
                            rv += str(rv)
                            print(rv + " # FROM SAVE_SETTINGS FUNCTION")
                            return rv
                
                if settings is None:
                    settings = c_s

                for i in range(len(setting_names)):
                    try:
                        settings[setting_names[i]]
                    except:
                        settings[setting_names[i]] = setting_defaults[i]

                rv = DbFunctions.write_settings_to_json(settings, file=file)

                if type(rv) == str:                
                    if rv.startswith("InputP"):
                        return rv

        except:
            ### ERROR ###
            output = all_errors[INTERNAL_SYNTAX_ERR]
            print(output + " # FROM SAVE_SETTINGS FUNCTION")
            return output
    
    
    @staticmethod
    def get_setting(file=file_s, setting_name=None):
        try:
            if not (setting_name in setting_names) and file == file_s and setting_name is not None:
                ### ERROR ###
                output_e = all_errors[INTERNAL_SYNTAX_ERR]
                print(output_e + " # FROM GET_SETTING FUNCTION (SPECIFIED SETTING NOT FOUND) ")
                return output_e

            c_s = DbFunctions.read_settings_on_json(file=file)
           

            if c_s is None or (type(c_s) == str and str(c_s).startswith("InputP")) or c_s == "":
                
                rv = DbFunctions.write_settings_to_json(file=file, reset=True)
                DbFunctions.get_setting(file=file, setting_name=setting_name)
                
                if str(rv).startswith("InputP"):
                    ### ERROR ###
                    rv = str(rv)
                    print(rv + " # FROM GET_SETTING FUNCTION")
                    return rv

            
            else:
                
                # eger setting yoksa ekleniyor
                if file == file_s:
                    settings = {}
                    
                    for i in range(len(setting_names)):
                        try:
                            c_s[setting_names[i]]
                        except KeyError:
                            c_s[setting_names[i]] = setting_defaults[i]
                
                elif file == file_lc:
                    lc_set = {} 
                    
                    for i in range(len(lc_names)):
                        try:
                            c_s[lc_names[i]]
                        except KeyError:
                            c_s[lc_names[i]] = lc_defaults[i]
                    
                            
                rv2 = DbFunctions.write_settings_to_json(c_s, file=file)
                                
                if type(rv2) == str and str(rv2).startswith("InputP"):
                    ### ERROR ###
                    output_e = str(rv2)
                    print(output_e + " # FROM GET_SETTING FUNCTION")
                    return output_e


            c_s = DbFunctions.read_settings_on_json(file=file)
            
            if type(c_s) == str and str(c_s).startswith("InputP") or c_s == None or c_s == "":
                ### ERROR ###
                c_s = all_errors[READ_ERR]
                print(c_s + " # FROM GET_SETTING FUNCTION")
                return c_s

            
            
            if setting_name is not None:
                try:
                    output = c_s[setting_name]
                except:
                    ### ERROR ###
                    output_e = all_errors[INTERNAL_SYNTAX_ERR]
                    print(output_e + " # FROM GET_SETTING FUNCTION (SPECIFIED SETTING NOT FOUND)")
                    return output_e

                return output

            else:
                output = c_s
                return output
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM GET_SETTING FUNCTION")
            return output_e


### OK ###
class ServerFunctions:
    ### OK ###
    @staticmethod
    def check_server(port):
        try:
            sockettemp = ServerFunctions.start_server(port)
            sockettemp.close()
        except:
            print("Server Opened")
            return True
        else:
            print("Server Not Opened")
            return False

    ### OK ###
    @staticmethod
    def start_server(port):
        try:
            s = socket.socket()
            time.sleep(0.1)
            s.bind(("", port))
            time.sleep(0.1)
            s.listen(5)
            time.sleep(0.1)
            return s
        except:
            ### ERROR ###
            output_e = all_errors[SERVER_ALREADY_STARTED_ERR]
            print(output_e)
            return output_e
            
    ### OK ###
    @staticmethod
    def recieve(s, time):
        try:
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
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM RECEIVE FUNCTION")
            return output_e
                        

    ### OK ###
    @staticmethod
    def connect_to_server(port):
        s = socket.socket()
        try:
            s.connect(("127.0.0.1", port))
            return s
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM CONNECT_TO_SERVER FUNCTION")
            return output_e

    ### OK ###
    @staticmethod
    def send_to_server(s, message):
        try:
            s.send(str.encode(str(message)))
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM SEND FUNCTION")
            return output_e


# Siyabendin kodlarini ellemek istemiyorum
class CameraFunctions:
    @staticmethod
    def detect_targets(capture, pc_mode = None):
        kernel = np.ones((3, 3), np.uint8)
        kernel2 = np.ones((13, 13), np.uint8)

        hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)
        # lower_green = np.array([45, 110, 105])
        # upper_green = np.array([102, 255, 255])

        lower_green = np.array([60, 110, 70])
        upper_green = np.array([80, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        if pc_mode is not None:
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


### ALL ERROR PROOF ###
class InputPFunctions:
       
    ### ERROR PROOF ### (Raise)
    @staticmethod
    def get_ipaddr():
        try:
            if str(sys.platform).startswith("win"):
                return socket.gethostbyname(socket.gethostname())

            elif str(sys.platform).startswith("linux") or str(sys.platform).startswith("cygwin"):
                ipaddress = os.popen(
                    "ifconfig eth0 \
                            | grep 'inet addr' \
                            | awk -F: '{print $2}' \
                            | awk '{print $1}'"
                ).read()

                return ipaddress
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            return output_e
            print(output_e + " # FROM GET_IPADDR FUNCTION")

    ### ERROR PROOF ### (Raise)
    @staticmethod
    def check_cam():
        try:
            if str(sys.platform).startswith("win"):
                return "TRUE BECAUSE WINDOWS"

            elif str(sys.platform).startswith("linux") or str(sys.platform).startswith("cygwin") and socket.gethostname() == "frcvision":
                if os.path.exists("/dev/video0"):
                    return "CAMERA.PY CONNECTED"

                else:
                    return "CAMERA NOT FOUND"
        except:
            ### ERROR ###
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM CHECK_CAM FUNCTION")
            return output_e

    ### ERROR PROOF ### (Raise)
    @staticmethod
    def get_ssid():
        try:
            if str(sys.platform).startswith("win"):
                return "Tunapro1234 7/2/2020"

            if str(sys.platform).startswith("linux") or str(sys.platform).startswith("cygwin"):
                ssid = os.popen(
                    "iwconfig wlan0 \
                        | grep 'ESSID' \
                        | awk '{print $4}' \
                        | awk -F\\\" '{print $2}'"
                ).read()

                return ssid
        except:
            ### ERROR ###
            output = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e + " # FROM GET_SSID FUNCTION")
            return output_e

    
    @staticmethod    
    def find_arg(wanted_setting, input_array=sys.argv, num=False):
        try:
            wanted_setting_value = None
            
            if wanted_setting in input_array:
                
                for s in range(len(input_array)):
                    
                    if input_array[s] == wanted_setting:
                        wanted_setting_index = s
                
                        if (s+1) < len(input_array):
                            wanted_setting_value = input_array[s+1]
                
                if num:
                    return wanted_setting_index
                    
                elif num is None:
                    return (wanted_setting_index+1)
                    
                else:
                    return wanted_setting_value
                    
            else:
                return None
        
        except:
            output_e = all_errors[INTERNAL_SYNTAX_ERR]
            print(output_e  + " # FROM FIND_ARG FUNCTION")
            return output_e
        
    @staticmethod        
    def change_menu(key, cur_stat, led1, out1):
        if key == "button0" and cur_stat["current_menu"] == main_menu_value:

            # IP MENU
            if cur_stat["current_row"] == (ip_menu_value-1):
                new_menu = ip_menu_value
                new_row = 0


            # ARDUINO CONFIG MENU
            elif cur_stat["current_row"] == (arduino_menu_value-1):
                new_menu = arduino_menu_value
                new_row = 0
                

            # CAMERA MENU
            elif cur_stat["current_row"] == (camera_menu_value-1):
                new_menu = camera_menu_value
                new_row = 0
                

            # LED TEST
            elif cur_stat["current_row"] == 3:
                ArduinoFunctions.led_write(led1, out1, 0)
                time.sleep(1)
                ArduinoFunctions.led_write(led1, out1, 1)
                new_menu = cur_stat["current_menu"]
                new_row = cur_stat["current_row"]
                
            elif cur_stat["current_row"] == (info_menu_value):
                new_menu = info_menu_value
                new_row = 0

            #EXIT
            elif cur_stat["current_row"] == len(cur_stat["all_menu_elements"][main_menu_value][0]) - 1:
                new_menu = cur_stat["current_menu"]
                new_row = cur_stat["current_row"]
                exit()

        else:
            new_row = cur_stat["current_row"]
            new_menu = cur_stat["current_menu"]

        return new_row, new_menu