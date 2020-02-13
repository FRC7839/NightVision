#########################################################################################################
###
### WRITTEN BY:
### 
### ColonelKai - Kayra Acar
### TUNAPRO1234 - Tuna Gul
### BLACKSHADOW - Siyabend Urun
### 
### NightFury#7839 (Adımız şu an farklı olabilir tartışmalar hala devam ediyor)
### 
### FRC 2020 - NightVision - Target Detection Algorithm 
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
##
"TODO"#####################################################################################################"""

from FRC_LIB7839 import *
import numpy as np
import socket
import math
import time
import sys
import cv2
import os


# region global
global success
global pc_test_mode
global test_mode
global pc_mode
global cam_num


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
    cam_num = int(cam_num)

else:
    cam_num = 0

if pc_mode is None:
    from cscore import CameraServer, VideoSource

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

def main():
    functions = CameraFunctions()
    
    print("Started")
    
    settings = DbFunctions.get_setting(file_s)
    
    if handle_error_lite(settings) == True:
        settings = {}
        settings[setting_names[0]] = setting_defaults[0]
        settings[setting_names[1]] = setting_defaults[1]
        settings[setting_names[2]] = setting_defaults[2]
        settings[setting_names[3]] = setting_defaults[3]
        settings[setting_names[4]] = setting_defaults[4]
    

    cam_tol = int(DbFunctions.get_setting(file_s, "Camera Tolerance"))
    robo_loc = DbFunctions.get_setting(file_s, "Robot Location")
    
    isNtStarted = None
    isConntedtoRadio = None
    y_error = None
    
    ip_addr = InputPFunctions.get_ipaddr()
    
    if handle_error_lite(ip_addr) and pc_mode is None:
        ip_addr = "127.0.1.1"
    
    elif handle_error_lite(ip_addr) and pc_mode is not None:
        ip_addr = "127.0.0.1"
    
    
    if ip_addr.startswith("10.78.39"):
        print(" ## NETWORK TABLES INIT ## ")
    else:
        isConntedtoRadio = False
    
    if pc_mode is None:
        if isConntedtoRadio and os.name == "posix" and str(socket.gethostname()) == "frcvision":
            try:
                print(" ## NETWORK TABLES INIT ## ")
                NetworkTables.initialize()
                
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
        
        # gen_frames(final_result, True)
        
        if len(ok_contours) >= 1:
            final_result = functions.draw_rectangle(processingImg, ok_contours)
            cv2.putText(
                final_result, _name, (30, 50), text_font, 1, (0, 0, 255), 2, cv2.LINE_AA
            )
            _, y_error, distance = functions.calculate_errors(ok_contours)
        
        imgLQ = cv2.resize(final_result, (120, 90))
        
        if pc_mode is not None:
            cv2.imshow("FRC Vision", final_result)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
        if success == True and y_error is None: # Hedefin yarısı görüldüğünde success değişkeni true değerini almasına rağmen hedef kenarlara değdiği için y_error değeri almıyor (Siyabendin müthiş çözümleri)
            success = False                     #  
        # Success true olunca tarama modu duruyor ve kamera y_errora göre hareket etmeye başlıyor         
        # Ama bizim y_error köşe olayı yüzünden olmadığı için kamera hareketsiz kalıyordu
        
                
        if y_error is not None and success == True and pc_mode is None:
            
            if ((success == True) and (y_error < (-1 * cam_tol))): # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın sağında kalıyorsa ve servo en sağda değilse
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Robot location: " + robo_loc,
                    "Camera Tolerance: " + str(cam_tol),      
                    "Network Tables " + str(isNtStarted),              
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
                    "Network Tables " + str(isNtStarted),
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
                    "Network Tables " + str(isNtStarted),
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
                    "Network Tables " + str(isNtStarted),
                    "Hedef bulunamadı",
                    sep="  --  ",
                )      
            
                
        elif y_error is not None and success == True and pc_mode is not None:
            
            if ((success == True) and (y_error < (-1 * cam_tol))): # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın sağında kalıyorsa ve servo en sağda değilse
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Robot location: " + robo_loc,
                    "Camera Tolerance: " + str(cam_tol),      
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
                    "Hedef bulunamadı",
                    sep="  --  ",
                )                      
                
    if image_mode is None:
        cap.release()
    
    cv2.destroyAllWindows()
    exit()

if __name__ == "__main__":
    main()