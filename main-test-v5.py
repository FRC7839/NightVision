#########################################################################################################
"""VERSION 5                                                                                             
        TO DO
            **ADD PC TEST MODE



                                                                                                      """ 
#########################################################################################################

from cscore import CameraServer, VideoSource
from frc_lib7839 import *
import numpy as np
import socket
import math
import time
import sys
import cv2

global pc_test_mode
global test_mode
global pc_mode
global cam_num


pc_test_mode = InputPFunctions.find_arg("--pc-test-mode", num=True)
test_mode = InputPFunctions.find_arg("--test-mode", num=True)
pc_mode = InputPFunctions.find_arg("--pc-mode", num=True)
cam_num = InputPFunctions.find_arg("--pc-mode")


if os.name == "nt":
    pc_mode = 1
    
elif pc_test_mode is not None:
    pc_mode = 1
    test_mode = 1 

def handle_error_lite(errmsg):
    if type(errmsg) == str:
        if str(errmsg).startswith("InputP"):
            if test_mode is not None:
                raise Exception(str(errmsg))
            else:
                return True
        else:
            return False

def main():
    functions = CameraFunctions()
    
    print("Started")
    
    settings = DbFunctions.get_setting(file_s)
    
    if handle_error_lite(settings) == True:
        settings = {}
        settings[setting_names[0]] = str(True)
        settings[setting_names[1]] = str("MIDDLE")
        settings[setting_names[2]] = str("15")
        settings[setting_names[3]] = str("0")
        settings[setting_names[4]] = str("1")        
    

    cam_tol = int(settings["Camera Tolerance"])
    robo_loc = settings["Robot Location"]
    
    ip_addr = ServerFunctions.get_ipaddr()
    
    isNtStarted = None
    isConntedtoRadio = None
    y_error = None
    
    if ip_addr.startswith("10.78.39") and os.name == "posix" and str(socket.gethostname()) == "frcvision":
        isConntedtoRadio = True
        try:
            if pc_mode is None:                
                NetworkTables.initialize()
            else:
                isNtStarted = False
        except:
            ### ERROR ###
            print(" ### NT NOT STARTED ### ")
            isNtStarted = False 
            
        else:
            print("Network Tables initialize")
            isNtStarted = True
            
    else:
        isConntedtoRadio = False


    if pc_mode is not None:    
        cap = cv2.VideoCapture(cam_num)
        cap.set(3, 480)
        cap.set(4, 640)
        cap.set(cv2.CAP_PROP_EXPOSURE, -9)
   
    else:
        cs = CameraServer.getInstance()
        cs.enableLogging()

        camera = cs.startAutomaticCapture()  
        camera.setResolution(640, 480)

        cvSink = cs.getVideo()
        
        
        
    if isNtStarted:
        outputStream = cs.putVideo("LQimg", 120, 90)
        print("outputStream = cs.putVideo('LQimg', 120, 90)")

    imgHQ = np.zeros(shape=(640, 360, 3), dtype=np.uint8)
    imgLQ = np.zeros(shape=(120, 90, 3), dtype=np.uint8)

    text_font = cv2.FONT_HERSHEY_SIMPLEX
    _name = ""

    while True:
        ok_contours = []
        global success
        success = False
        time, processingImg = cvSink.grabFrame(imgHQ)

        if time == 0:
            if isNtStarted:
                outputStream.notifyError(cvSink.getError())
            # logging.debug(cvSink.getError())
            continue

        contours = functions.detect_targets(processingImg)
        
        try:
            for cnt in contours:
                _ok, _name = functions.cnt_test(cnt)
                if _ok:
                    ok_contours.append(cnt)
                success = True
        except TypeError:
            pass

        final_result = processingImg
        gen_frames(final_result, True)
        if len(ok_contours) >= 1:
            final_result = functions.draw_rectangle(processingImg, ok_contours)
            cv2.putText(
                final_result, _name, (30, 50), text_font, 1, (0, 0, 255), 2, cv2.LINE_AA
            )
            _, y_error, distance = functions.calculate_errors(ok_contours)
        

        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        imgLQ = cv2.resize(final_result, (120, 90))
        
        try: # Hedefin yarısı görüldüğünde success değişkeni true değerini almasına rağmen hedef kenarlara değdiği için y_error değeri almıyor (Siyabendin müthiş çözümleri)
            if (success == True and y_error == None): # Success true olunca tarama modu duruyor ve kamera y_errora göre hareket etmeye başlıyor 
                print("Bunu okuyorsan siyabend gerizekalıdır") # Ama bizim y_error köşe olayı yüzünden olmadığı için kamera hareketsiz kalıyordu
      
        except UnboundLocalError:
            if (success == True):
                success = False
            
        check_ip(isNtStarted, "10.78.39")
        
        isServerStarted = ServerFunctions.check_server(check_cam_port)
        if not isServerStarted:        
            ServerFunctions.start_server(check_cam_port)
            
        try:

            if ((success == True) and (y_error < (-1 * cam_tol))): # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın sağında kalıyorsa ve servo en sağda değilse
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Robot location: " + robo_loc,
                    "Camera Tolerance: " + str(cam_tol),      
                    "Network Tables " + str(isNtStarted)              
                    "Hedef sağda",
                    sep="  --  ",
                )
                # go_right()
                                
                                
            elif ((success == True) and (y_error > cam_tol)): # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın solunda kalıyorsa ve servo en solda değilse
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Robot location: " + robo_loc,
                    "Camera Tolerance: " + str(cam_tol),
                    "Network Tables " + str(isNtStarted)
                    "Hedef solda",
                    sep="  --  ",
                )
                # go_left()                

            elif ((success == True) and (y_error < cam_tol) and (y_error > (-1 * cam_tol))):
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Robot location: " + robo_loc,
                    "Camera Tolerance: " + str(cam_tol),
                    "Network Tables " + str(isNtStarted)
                    "Hedef ortada",
                    sep="  --  ",
                )        

            else:
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),                    
                    "Robot location: " + robo_loc,
                    "Camera Tolerance: " + str(cam_tol),
                    "Network Tables " + str(isNtStarted)
                    "Hedef bulunamadı",
                    sep="  --  ",
                )      
                   
        except UnboundLocalError:
            pass

    cap.release()
    cv2.destroyAllWindows()
            
class Setting:  
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def return_list(self):
        return [self.name, self.value]


    if os.name == "nt":     
        ipaddress = socket.gethostbyname(socket.gethostname())
    
    elif os.name == "posix":
        ipaddress = os.popen("ifconfig wlan0 \
                     | grep 'inet addr' \
                     | awk -F: '{print $2}' \
                     | awk '{print $1}'").read()

    if str(ipaddress).startswith(ipStartswith) and isNtStarted == False:
        return True
    else: 
        return False

if __name__ == "__main__":
    main()