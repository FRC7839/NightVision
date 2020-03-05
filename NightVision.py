#########################################################################################################
###
### WRITTEN BY:
### 
### ColonelKai - Kayra Acar
### TUNAPRO1234 - Tuna Gul
### BLACKSHADOW - Siyabend Urun
### 
### FRC 2020 - NightVision - Target Detection Algorithm 
### 
### NightFury#7839 (Adımız şu an farklı olabilir tartışmalar hala devam ediyor)
### 
#########################################################################################################

#########################################################################################################
## NightVision Usage:
##
##      Öncelikle bu kod frcvision kurulmuş bir Raspberry pi üzerine kurulmalıdır, kodun ayarlarını yapabilmek için,
##  "InputPlus.py" adlı python scriptini /home/pi klasörüne atmalısınız. settings.json dosyası iki script (hem arayüz 
##  hem de algoritma) için de ortak database dosyasıdır. Her ne kadar okuma ve yazma fonksiyonlarının hata vermemesi 
##  için çalışsam da gözden kaçırdığım yerler olabilir, o yüzden lütfen acil bir durum olmadıkça dosyalar içinde
##  değişiklik yapmayın. 
##         
## 
##      Kod, çalışmak için FRC_LIB7839.py dosyasına ihtiyaç duymaktadır. FRC_LIB7839.py kodu da arayüz kodu
##  ile aynı dizinde (/home/pi) bulunmalıdır. Eğer bilgisayar üzerinde test yapmak amacıyla indiriyorsanız        
##  (ki geliştirme dışında pek bir amaç görmüyorum) aynı klasörde olması yeterli. 
##
##  
##      Frcvision kod her hata verdikten 5 saniye sonra kodu baştan başlatıyor, ayrıca algoritma kodlarının çoğunu  
##   Siyabend yazdı çok karıştırmak da istemiyorum. Bu nedenler yüzünden hata engelleme konusuna arayüzde olduğu kadar  
##   çok çalışamadım.   
##
##   
##      Bu kod FRC'nin 2020, (INFINITE RECHARGE) sezonu için hazırlanmış olsa da arayüz (InputPlus.py), her yıl için    
##  küçük bir düzenleme ile kullanıma hazır olabilir. Her ne kadar seneye çok katılmak istesem de muhtemelen               
##  katılamayacağımız gerçeği beni üzüyor. Belki kod 40-50'den fazla kez indirilirse seneye düzenlemeleri çok
##  daha erken yapabilirim.
##              
##      
## Bilgisayar Testleri İçin:
##           
##      Yukarda yazdığım gibi bilgisayarda test yapmak için tüm dosyaların aynı klasörde olması gerekmektedir.
##  
##  Bilgisayarlarda kamera ile kullanbilmek için: python NightVision.py --pc-mode <camera_numarası>
##      Laptop kullanıyorsanız, laptopun builtin kamerasının numarası 0 olacaktır. Eğer FRC'nin yolladığı kamerayı 
##      taktıysanız 1, eğer dünyanın en basit arayüzünü kullanamadıysanız ip adresini girebilirsiniz
##     
##  Bilgisayarlarda örnek görüntü ile test yapmak için: python NightVision --pc-test-image <image\location>
##      Bunu okuyorsan Siyabend sakattır
##  
##  Raspberry pi üzerine örnek görüntü ile test yapmak içim python NightVision --test-image <image\location>
##      Muhtemelen çalışmaz daha önce denemedim ve ihtiyaç da duymadım
##
#########################################################################################################


"""#####################################################################################################"TODO"
## VERSION 5                                                                                             
##      **ADD PC TEST MODE (TUNAPRO1234)
##      ADD LED CONTROLLING SYSTEM (TUNAPRO1234)
##      ADD NETWORK TABLES SENDING SYSTEM FOR AUTONOMOUS (BLACKSHADOW)
##      Sürekli JSON Database'inden okuma ve handle_error_lite'lar
##
##
##
##
##
##
##
##
##
##
##
"TODO"#####################################################################################################"""

from frc_lib7839 import *
import numpy as np
import threading
import socket
import queue
import math
import time
import sys
import cv2
import os


# region global
global success
global pc_mode
global cam_num
global team_ip1


team_number = InputPFunctions.find_arg("--team-number", num=True)

if team_number is None:
    team_ip1 = "78.39"
    
else:
    team_ip1 = str(InputPFunctions.find_arg("--team-number"))    
    if len(team_ip1) == 3:
        team_ip1 = "0" + team_ip1[0] + "." + team_ip1[1:]

    elif len(team_ip1) == 4:
        team_ip1 = team_ip1[0:2] + "." + team_ip1[2:]


pc_test_image = InputPFunctions.find_arg("--pc-test-image", num=True)

pc_mode = InputPFunctions.find_arg("--pc-mode", num=True)
cam_num = InputPFunctions.find_arg("--pc-mode")

image_mode = InputPFunctions.find_arg("--test-image", num=True)


if pc_test_image is not None:
    pc_mode = 1
    image_mode = 1

if os.name == "nt":
    pc_mode = 1

if image_mode is not None:
    test_image = InputPFunctions.find_arg("--pc-mode")
    
    if test_image is None:
        test_image = InputPFunctions.find_arg("--pc-test-image")
    
    if not os.path.exists(test_image):
        test_image = None
        image_mode = None

if cam_num is not None:
    try:
        cam_num = int(cam_num)
    except ValueError:
        cam_num = cam_num
else:
    cam_num = 0

if pc_mode is None:
    from cscore import CameraServer, VideoSource
    from networktables import NetworkTables


if pc_mode is not None:
    w_time = 5

else:
    w_time = 30

# endregion

def handle_error_lite(errmsg):
    if type(errmsg) == str:
        if str(errmsg).startswith("InputP"):
            # if test_mode is not None:
            #     raise Exception(str(errmsg))
            # else:
            return True
        else:
            return False

def json_read_thread():        
    json_read_thread.finished = False
    settings = DbFunctions.read_settings_on_json(file_s)

    # print("bunu görmüyorsan kayra sakattır")
    
    if handle_error_lite(settings) == True:
        settings = {}
        settings[setting_names[0]] = setting_defaults[0]
        settings[setting_names[1]] = setting_defaults[1]
        settings[setting_names[2]] = setting_defaults[2]
        settings[setting_names[3]] = setting_defaults[3]
        settings[setting_names[4]] = setting_defaults[4]
    
    else:
        robo_loc = DbFunctions.read_settings_on_json("Robot Location", file_s)
        cam_tol = DbFunctions.read_settings_on_json("Camera Tolerance", file_s)
        wait_per = DbFunctions.read_settings_on_json("Waiting Period", file_s)
        auto_mode = DbFunctions.read_settings_on_json("Autonomous Mode", file_s)
        cam_off = DbFunctions.read_settings_on_json("Camera Offset", file_s)
        is_MM_started = DbFunctions.read_settings_on_json("Match Mode Status", file_s)
        
    json_read_thread.finished = True

    return robo_loc, cam_tol, wait_per, auto_mode, cam_off, is_MM_started

def main():
    # os.popen('export DISPLAY=":0"') 
    functions = CameraFunctions()
    
    print("Started")    

    isNtStarted = None
    isConntedtoRadio = None
    y_error = None
    
    ip_addr = InputPFunctions.get_ipaddr()
    
    if handle_error_lite(ip_addr) and pc_mode is None:
        ip_addr = "127.0.1.1"
    
    elif handle_error_lite(ip_addr) and pc_mode is not None:
        ip_addr = "127.0.0.1"
    
    
    if ip_addr.startswith("10." + team_ip1):
        print(" ## NETWORK TABLES INIT ## ")
    else:
        isConntedtoRadio = False
    
    if pc_mode is None:
        if os.name == "posix":
            try:
                print(" ## NETWORK TABLES INIT ## ")
                NetworkTables.initialize("10.78.39.2")
                
            except:
                ### ERROR ###
                print(" ### NETWORK TABLES INIT FAILED ### ")
                isNtStarted = False 
                
            else:
                isNtStarted = True
                
    
    
    if image_mode is not None:
        cap = cv2.imread(test_image) 

    elif pc_mode is not None:    
        cap = cv2.VideoCapture(cam_num)
        cap.set(3, 480)
        cap.set(4, 640)
        cap.set(cv2.CAP_PROP_EXPOSURE, -9)
   
   
    else:
        cs = CameraServer.getInstance()
        cs.enableLogging()

        camera = cs.startAutomaticCapture()  
        camera.setResolution(640, 480)
        camera.getProperty("brightness").set(0)
        camera.getProperty("contrast").set(50)
        camera.getProperty("saturation").set(100)
        camera.getProperty("exposure_auto").set(1)
        camera.getProperty("exposure_absolute").set(0)
        
        cvSink = cs.getVideo()
        
        procTable = NetworkTables.getTable("imgProc")
        smartTable = NetworkTables.getTable("SmartDashboard")
        
    if pc_mode is None:
        outputStream = cs.putVideo("LQimg", 120, 90)
        print("outputStream = cs.putVideo('LQimg', 120, 90)")

    imgHQ = np.zeros(shape=(640, 360, 3), dtype=np.uint8)
    imgLQ = np.zeros(shape=(120, 90, 3), dtype=np.uint8)

    text_font = cv2.FONT_HERSHEY_SIMPLEX
    _name = ""
    
    print("VISION PROCESSING STARTED")
    
    robo_loc, cam_tol, wait_per, auto_mode, cam_off, is_MM_started = json_read_thread()        
    
    start_t = timeit.default_timer()
    que = queue.Queue()
    # t = threading.Thread(target=lambda q, arg1: q.put(json_read_thread(arg1)), args=(que, ""))
    # firsttimethreading = True
    # is_MM_started = False
    w_timed = 5
    m_timed = 20

    while True:
        elapsed = timeit.default_timer() - start_t 


        if is_MM_started is None or str(is_MM_started) == "False":        
            if elapsed >= w_timed:
                start_t = timeit.default_timer()
                robo_loc, cam_tol, wait_per, auto_mode, cam_off, is_MM_started = json_read_thread()
                print("db1")
        
        elif str(is_MM_started) == "True":        
            if elapsed >= m_timed:
                start_t = timeit.default_timer()
                robo_loc, cam_tol, wait_per, auto_mode, cam_off, is_MM_started = json_read_thread()
                print("db2")
        

            
            # # kayranın threading return değer ataması


            # try:    
            #     if json_read_thread.finished:
            #         t.join()
            #         robo_loc, cam_tol, wait_per, auto_mode, cam_off = que.get()
            #         # t.
            #         t.start()
            # except:
            #     if firsttimethreading:
            #         t.start()
            #         firsttimethreading = False
            #     elif firsttimethreading == False:
            #         pass
                


        ok_contours = []
        
        success = False
        
        if image_mode is not None:
            processingImg = cv2.imread(test_image) 

        elif pc_mode is not None:
            time, frame = cap.read()
            processingImg = frame
        
        else:
            time, processingImg = cvSink.grabFrame(imgHQ)
            if time == 0:
                if isNtStarted:
                    outputStream.notifyError(cvSink.getError())
            # logging.debug(cvSink.getError())
            # continue
        
        # if processingImg is not None:
        #     print("debug 1")

        contours = functions.detect_targets(processingImg, pc_mode)
        
        try:
            for cnt in contours:
                _ok, _name = functions.cnt_test(cnt)
                if _ok:
                    ok_contours.append(cnt)
                success = True
        except TypeError:
            pass

        # print("debug 2")
        
        # robo_loc, cam_tol, wait_per, auto_mode, cam_off = json_read_thread()        
        final_result = processingImg
        
        # gen_frames(final_result, True)
        
        if len(ok_contours) >= 1:
            final_result = functions.draw_rectangle(processingImg, ok_contours)
            cv2.putText(
                final_result, _name, (30, 50), text_font, 1, (0, 0, 255), 2, cv2.LINE_AA
            )
            _, y_error, distance = functions.calculate_errors(ok_contours)
    
        if pc_mode is None:
            # print("ok")
            procTable.putString('Robot Location', robo_loc)
            procTable.putString('Cam Tol', cam_tol)
            procTable.putString('Waiting Period', wait_per)
            procTable.putString('Autonomous Mode', auto_mode)
            procTable.putString('Camera Offset', cam_off)
            
            if success and y_error is not None:
                procTable.putString('yerror', y_error)
            else:
                procTable.putString('yerror', "NF")
                                        
            smartTable.putString('Robot Location', robo_loc)
            smartTable.putString('Cam Tol', cam_tol)
            smartTable.putString('Waiting Period', wait_per)
            smartTable.putString('Autonomous Mode', auto_mode)
            smartTable.putString('Camera Offset', cam_off)

            if success and y_error is not None:
                smartTable.putString('yerror', y_error)
            else:
                smartTable.putString('yerror', "NF")
                                    
            
                
                
        # print("debug 3")
        
        imgLQ = cv2.resize(final_result, (120, 90))
        
        if pc_mode is not None:
            cv2.imshow("FRC Vision", final_result)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        
            
        
        if y_error is None and success == True: # Hedefin yarısı görüldüğünde success değişkeni true değerini almasına rağmen hedef kenarlara değdiği için y_error değeri almıyor (Siyabendin müthiş çözümleri)
            success = False                     #  
            print("y_error none but success true")
        # Success true olunca tarama modu duruyor ve kamera y_errora göre hareket etmeye başlıyor         
        # Ama bizim y_error köşe olayı yüzünden olmadığı için kamera hareketsiz kalıyordu
        
        if success == False: 
            print("Not found anything")    
        
        # print("debug 4")
            
        try:
            if y_error is not None and success == True and pc_mode is None:
                
                if ((success == True) and (y_error < (-1 * int(cam_tol)))): # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın sağında kalıyorsa ve servo en sağda değilse
                    print(
                        "Success: " + str(success),
                        "Error: " + str(y_error),
                        "Distance: " + str(distance),
                        "Robot location: " + robo_loc,
                        "Camera Tolerance: " + str(int(cam_tol)),      
                        "Network Tables " + str(isNtStarted),              
                        "Hedef sağda",
                        sep="  --  ",
                    )
                    # go_right()
                                    
                                    
                elif ((success == True) and (int(y_error) > int(cam_tol))): # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın solunda kalıyorsa ve servo en solda değilse
                    print(
                        "Success: " + str(success),
                        "Error: " + str(int(y_error)),
                        "Distance: " + str(distance),
                        "Robot location: " + robo_loc,
                        "Camera Tolerance: " + str(int(cam_tol)),
                        "Network Tables " + str(isNtStarted),
                        "Hedef solda",
                        sep="  --  ",
                    )
                    # go_left()                

                elif ((success == True) and (int(y_error) <= int(cam_tol)) and (int(y_error) >= (-1 * int(cam_tol)))):
                    print(
                        "Success: " + str(success),
                        "Error: " + str(int(y_error)),
                        "Distance: " + str(distance),
                        "Robot location: " + robo_loc,
                        "Camera Tolerance: " + str(int(cam_tol)),
                        "Network Tables " + str(isNtStarted),
                        "Hedef ortada",
                        sep="  --  ",
                    )        

                else:
                    print(
                        "Success: " + str(success),
                        "Error: " + str(int(y_error)),
                        "Distance: " + str(distance),                    
                        "Robot location: " + robo_loc,
                        "Camera Tolerance: " + str(int(cam_tol)),
                        "Network Tables " + str(isNtStarted),
                        "Hedef bulunamadı",
                        sep="  --  ",
                    )         

            elif int(y_error) is not None and success == True and pc_mode is not None:
                
                if ((success == True) and (int(int(y_error)) < (-1 * int(int(cam_tol))))): # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın sağında kalıyorsa ve servo en sağda değilse
                    print(
                        "Success: " + str(success),
                        "Error: " + str(int(y_error)),
                        "Distance: " + str(distance),
                        "Robot location: " + robo_loc,
                        "Camera Tolerance: " + str(int(cam_tol)),      
                        "Hedef sağda",
                        sep="  --  ",
                    )
                    # go_right()
                                    
                                    
                elif ((success == True) and (int(y_error) > int(cam_tol))): # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın solunda kalıyorsa ve servo en solda değilse
                    print(
                        "Success: " + str(success),
                        "Error: " + str(int(y_error)),
                        "Distance: " + str(distance),
                        "Robot location: " + robo_loc,
                        "Camera Tolerance: " + str(int(cam_tol)),
                        "Hedef solda",
                        sep="  --  ",
                    )
                    # go_left()                

                elif ((success == True) and (int(y_error) <= int(cam_tol)) and (int(y_error) >= (-1 * int(cam_tol)))):
                    print(
                        "Success: " + str(success),
                        "Error: " + str(int(y_error)),
                        "Distance: " + str(distance),
                        "Robot location: " + robo_loc,
                        "Camera Tolerance: " + str(int(cam_tol)),
                        "Hedef ortada",
                        sep="  --  ",
                    )        

                else:
                    print(
                        "Success: " + str(success),
                        "Error: " + str(int(y_error)),
                        "Distance: " + str(distance),                    
                        "Robot location: " + robo_loc,
                        "Camera Tolerance: " + str(int(cam_tol)),
                        "Hedef bulunamadı",
                        sep="  --  ",
                    )         
        except TypeError:
            pass            
                
    if image_mode is None:
        cap.release()
    
    cv2.destroyAllWindows()
    exit()

if __name__ == "__main__":
    main()