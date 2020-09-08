# region gereksiz yazilar
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
### NightFury#7839 (Adimiz su an farkli olabilir tartismalar hala devam ediyor)
###
#########################################################################################################


#                                                                  -->> . <<--NOKTAYI SILME KOD BOZULUYOR
#                                                                      /\   HERKES LORD NOKTA KARSISINDA EGILSIN
#                                                                      |    TANRIMIZ NOKTA
#                                                                      |
#                                               if you look to your above, you can see programmers going nuts

"""#####################################################################################################################"TODO"
                                                                                                                        
                                                                            14/2 TAKIM NUMARASINA GoRE AYAR YAPIMI (OK)
                                                                            14/2 SET UP LED CONTROLLING SYSTEM (For Interface)
                                                                            14/2 Led kontrol icine robot ayarlari yazilma hatasini duzelt
                                                                            14/2 FRC7839-NightVision yazisini yukari sag veya sol koseye yaz (COLONELKAI)
                                                                            14/2 WRITE CURRENT SETTING RETURN TO MAIN MENU (COLONELKAI)
                                                                            14/2 INFO menusu (Yazanlar - Tarih - Takim - vs) (COLONELKAI)
                                                                            14/2 check_arduino() olustur ve key get icine koy
                                                                            16/2 Panic mode icinde tekrar arduinoyu takmayi dene 
                                                                            16/2 Save ve get_setting icin handle_error()
                                                                            16/2 handle_error mm modeunun kernel panicine errorleri yollasin (yarim ama is gorur)
                                                                            17/2 TAKIM NUMARASI EKLEMEK IcIN ARDUINO CONFIGE AYAR EKLE (TUNAPRO1234 ve COLONELKAI)
                                                                                (button0'a her basildiginda sonraki rakama gececek)
                                                                            17/2 SETTINGS MENUSUNE ANLIK DOSYA RESFRESHI 
                                                                            17/2 Settings dosyasina takim numarasini ekle 
                                                                            17-18/2 TEAM NUMBER YAZISI DA BEYAZ YANMALI
                                                                            17-18/2 Led dosyasina is mm started ayarini ekle (Kamera algoritmasinin okuyup okumamasi gerektigini soylemek icin)
                                                                            17-18/2 INFO MENuSu cALIsMIYOR
                                                                            (YALAN) Settings write error (TUNAPRO1234)     
                                                                            1/3 SSID MENUSU HALLEDILECEK (KAYRA) 
                                                                            28/2 CHECK PORTS LINUX ICIN DUZENLENECEK

# THREADING ILE ARDUINONUN TAKILI OLUP OLMADIGI ANLASILACAK (KAYRA) 

# Match mode da iken led_camera kapatılmak istenirse yeşil led yanıp sönebilir (KAYRA)

# BLUETOOTH COM PORT HATASI 

# MATCH MODE BASLATILABILIR OLMASINA RAGMEN MAVI LED YANIP SONUYOR

# Yazilar uzerindeki turkce karakterleri kaldir (ç, ı, İ, ö, ş, ü, ğ)
"TODO"########################################################################################################################"""

###############################################################################################################################
##
##
## Eger https://github.com/FRC7839/NightVision'deki ReadMe.md dosyasini okuduysaniz muhtemelen burayi okumaniza
## gerek kalmayacaktir. Kodu istediginiz gibi kullanin sadece isim vermemeniz beni cidden uzerdi.
##
##
##  InputPlus.py Nedir Ne Ise Yarar Bu Yazilimi Kullanmak Icin Sebepler Nelerdir:
##
##
##      oncelikle eger bu yazilimi FRC2020 icin almayi dusunuyorsaniz cidden gecikme icin cooook ozur diliyorum.
##  Ama tatilde algoritmayi gelistirmesi icin biraz Siyabendi bekledim ve robot olmadigi icin servoyla farkli bir
##  prototip tasarlamam filan gerekti her neyse.
##
##
##      InputPlus.py sadece arayuz olmasi sebebiyle her sene tekrar kullanilabilecek bir koddur. Sadece algoritmayi
##  yenilemek sizin icin yeterli olacaktir. Kodu biraz incelersiniz hata vermemesi icin elimizden gelen her seyi
##  yaptigimizi gorebilirsiniz. Eger algilama ya da okuma gibi hatalar alirsaniz InputPlus, kendini PANIC MODE'a alir
##  ve ledin kapanmasini onleyip ayarlari dosyaya yazmaya calisir. Algoritmayla kod sadece bir JSON dosyasi uzerinden
##  iletisim kuruduklari icin herhangi bir yazilimin cokmesi digerinin de cokmesine sebep olmaz.
##
##
##      Programi yonetbilmek icin github sayfamizda aciklanan sekilde baglanmis bir adet arduino, bir adet potansiyometre,
##  iki  adet regular push button ve ledlerin ve arduinonun girisi icin disi headerlar kullanilabilir. Ayrica bir adet
##  Raspberry pi, rpi icin ekran kullanmalisiniz (kap kullanmanizi oneririm).
##
##
##      Github sayfasini FRC 2020 Bosphorus Regional'dan sonra herkesin duzenlemesi icin public hale getirmeye calisacagim.
##
##
#########################################################################################################
##                                                                                                     ##
##  --skip-camera-check     : camera kontorlunu atliyor (Zaten windowsta kamera kontrolu yok)          ##
##  --skip-network-check    : ip adres kontrolunu atliyor (NOT CONNECTED TO RADIO Hatasi kapaniyor)     ##
##  --pc-mode               : skip camera ve skip networkun birlesimi                                  ##
##  --test-mode             : verilen hatalar programi durdurur (FRC esnasinda onermiyorum)            ##
##  --pc-test-mode          : pc ve test modunun birlesimi                                             ##
##                                                                                                     ##
#########################################################################################################


###################### CURSES CALISMA MANTIGI ##################################################
# ilk olarak get menu values functionlari bir array'a ekranda yazilacak her bir satiri atiyor. #
# her satir bir element oluyor ve surekli olarak get menu values fonksiyonunu elementler       #
# uzerinde islem yapip onlari degistiriyor                                                     #
# sonra print menu bunlari alip yerlerini hesapladiktan sonra ekrana yazdiriyor.               #
# bu bize get menu values kullanark ekrandaki goruntuyu aktif olarak degistirmemizi sagliyor.  #
################################################################################################

# arduino_check_thread kullanımı
# not: lütfen tüm değişkenleri okuma/yazma olaylarını "Try/except" içine alın thread başlamadı ise hata verir
# thread başlatmak için: arduino_check_thread()
# threadi durdurmak için: arduino_check_thread.exitthread = True (try except içine al)
# thread'den değer okumak için (example yerine değerin yazılmasını istediğiniz değişken): example = arduino_check_thread.rv (try except içine al)

#endregion

from threading import Thread
from frc_lib7839 import *
import threading
import pyfirmata
import curses
import json
import time
import sys
import os

# region global

global pc_test_mode
global skip_cam_arg
global skip_nt_arg
global test_mode
global pc_mode


pc_test_mode = InputPFunctions.find_arg("--pc-test-mode", num=True)
test_mode = InputPFunctions.find_arg("--test-mode", num=True)
pc_mode = InputPFunctions.find_arg("--pc-mode", num=True)
match_mode_can_be_started = False
check_arduino_thread_rv = True


if os.name == "nt":
    from frc_lib7839 import *
    pc_mode = 1

if pc_mode is not None and os.name == "posix":
    sys.path.insert(1, '/home/pi/NightVision')
    from frc_lib7839 import *


if pc_mode is not None:
    skip_cam_arg = 1
    skip_nt_arg = 1

elif pc_test_mode is not None:
    pc_mode = 1
    skip_cam_arg = 1
    skip_nt_arg = 1
    test_mode = 1

else:
    skip_cam_arg = InputPFunctions.find_arg("--skip-camera-check", num=True)
    skip_nt_arg = InputPFunctions.find_arg("--skip-network-check", num=True)

# endregion

# DIKKAT
# Match mode otonom yuzunden diger tum menulerden farkli bir print
# fonksiyonuna ve getvalues'a ihtiyac duyuyor
# match mode icin get menu values fonksiyonu


def match_mode(
    stdscr,
    settings=None,
    led_blue=None,
    led_camera=None,
    led_red=None,
    led_green=None,
    swt1=None,
    pot1=None,
    PanicMenu=False,
    errmsg=None,
    err_type=None,
    isReadError=False
):
    # match mode, sadece durum raporu veren menü
    if not PanicMenu: # eğer error'suz başlatılmışsa
        try: # eğer açıksa yanıp sönen tüm led'leri kapat
            if flash_led.flashthreadopen:
                flash_led.exitthread = True
        except:
            pass
        
        led_blue.write(0) # mavi led kapalı
        led_green.write(1) # yeşil led açık
        # Ana yer
        while True:
            # Dosyadan okumayi dene
            #settings = DbFunctions.get_setting(file_s)  # led control dosyasindan ayari cekiyor
            #handle_error(led_control, stdscr, PanicMenu=True)

            settings["Match Mode Status"] = True
            # çıkmadan ayarları kaydet
            rv3 = DbFunctions.save_settings(file_s, settings)
            handle_error(rv3, stdscr, PanicMenu=True)

            handle_error(settings, stdscr, PanicMenu=True)
            
            m_menu_elements = []  # Menu elementleri arrayi
            m_menu_elements.append(" ## MATCH MODE STARTED ## ")  # Title

            # LED Bilgisayar tarafindan kontrol ediliyor ve menu bunu gosteriyor
            if settings["Led Status"] is not None and settings["Led Status"] in [
                True,
                False,
                "True",
                "False",
            ]:
                m_menu_elements.append(
                    " ## LED CONTROL : " + str(settings["Led Status"]) + " ## "
                )

            # Eger kapali ya da acik alamazsa error veriyor.
            else:
                m_menu_elements.append(" ## LED CONTROL FAILED ## ")
                settings["Led Status"] = True

            try:
                # Menunun geri kalani, durum reporu veriyor.
                m_menu_elements.append(
                    " ## TEAM_NUMBER : " + str(settings["Team Number"]) + " ## "
                )
                m_menu_elements.append(
                    " ## CAMERA_TOLERANCE : "
                    + str(settings["Camera Tolerance"])
                    + " ## "
                )
                m_menu_elements.append(
                    " ## ROBOT_LOCATION : " + str(settings["Robot Location"]) + " ## "
                )
                m_menu_elements.append(
                    " ## WAITING_PERIOD : " + str(settings["Waiting Period"]) + " ## "
                )
                m_menu_elements.append(
                    " ## AUTONOMOUS_MODE : " + str(settings["Autonomous Mode"]) + " ## "
                )

            except:
                handle_error(all_errors[READ_ERR], stdscr, PanicMenu=True)

            try:
                if flash_led.flashthreadopen: # eğer yanip sönen işik varsa kapatiyor
                    flash_led.exitthread = True 
            except:
                pass

            # led ayarlari
            if settings["Led Status"] in ["True", True]: 
                ArduinoFunctions.led_write(led_green, led_camera, 1)  # on


            elif settings["Led Status"] in ["False", False]:
                ArduinoFunctions.led_write(None, led_camera, 0)  # off
                flash_led(led_green)

            else:
                ArduinoFunctions.led_write(led_green, led_camera, 1)  # on

            # ekrana yazdıran fonksiyon
            print_menu_for_match(stdscr, m_menu_elements)
            
            time.sleep(3)
            # exit kodu
            if (
                ArduinoFunctions.map_x(pot1.read(), 0, 1, 0, max_v) == max_v
                and ArduinoFunctions.map_xi(swt1.read(), 0, 1, 0, max_v) == 0
            ):
                ArduinoFunctions.led_write(led_blue, led_camera, 1)  # on
                led_green.write(0)

                settings["Match Mode Status"] = False

                try: # eğer yanıp sönen led varsa kapat
                    if flash_led.flashthreadopen:
                        flash_led.exitthread = True 
                except:
                    pass
                # çıkmadan ayarları kaydet
                rv = DbFunctions.save_settings(file_s, settings)
                handle_error(rv, stdscr, PanicMenu=True)

                break

    ### KERNEL PANIC ###
    else: # panic modu açıksa

        try: # eğer yanıp sönen led var ise kapat
            if flash_led.flashthreadopen:
                flash_led.exitthread = True
        except:
            pass
        # arduino bağlandı mı kontrol etmek için ön hazırlık
        cp_p = ArduinoFunctions.check_ports()
        cp_c = cp_p
        
        try:
            led_red.write(1) # kırmızı ışığı yak
        except:
            pass
        
        settings = DbFunctions.get_setting(file_s)

        if handle_error(settings, stdscr, PanicMenu=False):
            settings = {}

            for i in range(len(setting_names)): 
                setting_control[setting_names[i]] = setting_defaults[i]
                
            f_err = True

        m_menu_elements = []  # Menu elementleri arrayi
        m_menu_elements.append(" ## PANIC MODE STARTED ## ")  # Title

        # LED Bilgisayar tarafindan kontrol ediliyor ve menu bunu gosteriyor
        if settings["Led Status"] is not None and settings["Led Status"] in [True,False,"True","False",]:
            m_menu_elements.append(" ## LED CONTROL : " + str(settings["Led Status"]) + " ## ")

        # Eger kapali yada acik alamazsa error veriyor.
        else:
            m_menu_elements.append(" ## LED CONTROL FAILED ## ")

            led_control["Led Status"] = True
            rv = DbFunctions.save_settings(file_s, settings)  # Olmazsa yapacak bir sey yok
            handle_error(rv, stdscr, PanicMenu=False)

        if settings is not None:
            # Menunun geri kalani, durum reporu veriyor.
            try:
                m_menu_elements.append(" ## TEAM_NUMBER : " + str(settings["Team Number"]) + " ## ")
                m_menu_elements.append(" ## CAMERA_TOLERANCE : "+ str(settings["Camera Tolerance"])+ " ## ")
                m_menu_elements.append(" ## ROBOT_LOCATION : " + str(settings["Robot Location"]) + " ## ")
                m_menu_elements.append(" ## WAITING_PERIOD : " + str(settings["Waiting Period"]) + " ## ")
                m_menu_elements.append(" ## AUTONOMOUS_MODE : " + str(settings["Autonomous Mode"]) + " ##")
                if not err_type is None:
                    m_menu_elements.append(" ## ERROR : " + err_type + " ## ")
            except:
                pass

        errortimer = threading.Timer(0.1, print_error, args=[stdscr, errmsg])
        errortimer.start()

        while True: # ana loop    
            print_menu_for_match(stdscr, m_menu_elements) # ekrana yazdır
            time.sleep(1) 

            if type(errmsg) == str and errmsg.startswith("InputP"): # eğer error mesajı verilmiş ise
                print_info(stdscr, errmsg, color=2) # ekrana yazdır
                errmsg = None

            background_setup(stdscr, None, PanicMode=True) # arka planı kırmızı yapmak

            if type(err_type) == str and err_type == "ARDUINO": # eğer arduino error ise
                rv2 = ArduinoFunctions.check_ports() # portlari yeniden kontrol et

                try:
                    if swt1.read() is None and rv2 != all_errors[ARDUINO_CONN_LOST]: # eğer switch error veriyor ve arduino bağlantısı bozuk
                        isReadError = True                                           # değilse iterator/read error
                    else:
                        isReadError = False
                except: # eğer swt objesi yoksa
                    if rv2 != all_errors[ARDUINO_CONN_LOST]:
                        try:
                            DbFunctions.save_settings()

                        except:
                            isReadError = True
                        else:
                            isReadError = False
                    else:
                        isReadError = False

                # if not handle_error(rv2, stdscr, PanicMenu=False, clean=True) and not isReadError:
                #     led_red.write(0)
                #     not_main(stdscr)

                cp_c = ArduinoFunctions.check_ports()
                if cp_c != cp_p: # eğer şimdiki portlar önceden farklı ise yeni arduino bağlanmış demektir
                    cp_p = cp_c
                    
                    if cp_c is not None and type(cp_c) == list and type(cp_c[0]) == str and not cp_c[0] == "":
                        try:
                            led_red.write(0)
                        except:
                            pass
                        not_main(stdscr) # arduino'yu yeniden import etmeyi dene

def get_first_menu_values(team_ip2):
    # ana menü için değerleri hazırlayan kod
    ipaddr_func = InputPFunctions.get_ipaddr() # bağlı ipadresini alma
    check_cam_func = InputPFunctions.check_cam() # camera bağlı mı kontrol

    mainmenu = []
    mainmenucheck = []

    if skip_nt_arg is not None: # eğer network skip aktif ise atla
        mainmenu.append("SKIPPED NETWORK CHECKING")
        mainmenucheck.append(True)

    elif ipaddr_func.startswith("127"): # eğer localhost ise bağlamadı yaz
        mainmenu.append("IP ADRESS: NOT CONNECTED")
        mainmenucheck.append(False)  ## False

    elif not ipaddr_func.startswith("10." + team_ip2): # eğer takım radyosundan farklı bir yere bağlandıysa uyarı ver
        mainmenu.append("NOT CONNECTED TO RADIO")
        mainmenucheck.append(False)  ## False

    else: # başarılı şekilde bağlandı
        mainmenu.append("IP ADRESS: " + ipaddr_func)
        mainmenucheck.append(True)

    mainmenu.append("SETTINGS") # settings menüsü için button
    mainmenucheck.append(True)

    if skip_cam_arg is not None: # eğer kamera kontrol skip aktif ise atla
        mainmenu.append("SKIPPED CAMERA CHECKING")
        mainmenucheck.append(True)

    elif (
        check_cam_func == "CAMERA CONNECTED" # eğer bağlı ise yada windows'ta ise
        or check_cam_func == "TRUE BECAUSE WINDOWS"
    ):
        mainmenu.append(check_cam_func) # başarılı!
        mainmenucheck.append(True)

    else:
        mainmenu.append(str(check_cam_func))
        mainmenucheck.append(False)  ## False

    mainmenu.append("LED TEST") # led test button
    mainmenucheck.append(True)

    mainmenu.append("INFO") # info menüsü button
    mainmenucheck.append(True)

    mainmenu.append("REBOOT") # linux'da bilgisayarı yeniden başlatan kod
    mainmenucheck.append(True)

    mainmenu.append("EXIT") # çıkış butonu
    mainmenucheck.append(True)

    return [mainmenu, mainmenucheck]


def get_ip_menu_values(
    team_ip2,
    ipaddr_func=InputPFunctions.get_ipaddr(),
):
    # ip menüsü için değerleri ayarlayan kod
    mainmenu = []
    mainmenu_status = []

    if skip_nt_arg is not None: # eğer network skip aktif ise atla
        mainmenu.append(" ## SKIPPED NETWORK CHECKING ## ")
        mainmenu_status.append(False)

    else:
        mainmenu.append("")
        mainmenu_status.append(False)

    mainmenu.append("HOSTNAME: " + str(socket.gethostname())) # PC'nin ismi
    mainmenu.append("IP ADRESS: " + ipaddr_func) # ip adress
    mainmenu.append("RADIO IP RANGE: 10." + team_ip2 + ".0/24")

    mainmenu.append("OK") # çıkış butonuu

    if str(socket.gethostname()) != "frcvision":
        mainmenu_status[0] = False

    if ipaddr_func.startswith("127"):
        mainmenu_status.append(False)
        mainmenu_status.append(False)
        mainmenu[2] = "IP ADRESS: NOT CONNECTED"

    elif not ipaddr_func.startswith("10." + team_ip2):
        mainmenu_status.append(False)
        mainmenu_status.append(False)

    else:
        mainmenu_status.append(True)
        mainmenu_status.append(True)

    mainmenu_status.append("Normal")
    mainmenu_status.append("Normal")

    return [mainmenu, mainmenu_status]


def get_arduino_menu_values(settings):
    mainmenu = []
    mainmenu_status = []

    # ROBOT LOCATION
    if settings["Robot Location"] is None:
        mainmenu.append("INPUT FOR ROBOT LOCATION")
        mainmenu_status.append(False)

    else:
        mainmenu.append("ROBOT LOCATION: " + settings["Robot Location"])
        mainmenu_status.append("Normal")

    # CAMERA TOLERANCE
    if settings["Camera Tolerance"] is None:
        mainmenu.append("INPUT FOR CAMERA TOLERANCE")
        mainmenu_status.append(False)

    else:
        mainmenu.append("CAMERA TOLERANCE: " + settings["Camera Tolerance"])
        mainmenu_status.append("Normal")

    # WAITING PERIOD
    if settings["Waiting Period"] is None:
        mainmenu.append("INPUT FOR WAITING PERIOD")
        mainmenu_status.append(False)

    else:
        mainmenu.append("WAITING PERIOD: " + settings["Waiting Period"])
        mainmenu_status.append("Normal")

    # AUTONOMOUS MODE
    if settings["Autonomous Mode"] is None:
        mainmenu.append("INPUT FOR AUTONOMOUS MODE")
        mainmenu_status.append(False)
    else:
        mainmenu.append("AUTONOMOUS MODE: " + settings["Autonomous Mode"])
        mainmenu_status.append("Normal")

    if settings["Camera Offset"] is None:
        mainmenu.append("INPUT FOR CAMERA OFFSET")
        mainmenu_status.append(False)
    else:
        mainmenu.append("CAMERA OFFSET:    mm")
        mainmenu_status.append("Normal")

    # mainmenu.append("")
    mainmenu.append("TEAM NUMBER:     ")
    mainmenu_status.append(True)

    # WRITE CURRENT SETTINGS AND OK BUTTONS
    mainmenu.append("WRITE CURRENT SETTINGS TO FILE")
    mainmenu_status.append("Normal")

    mainmenu.append("RETURN TO MAIN MENU")
    mainmenu_status.append(False)

    return [mainmenu, mainmenu_status]


def get_cam_menu_values(isCamOnline=InputPFunctions.check_cam()):
    mainmenu = []
    mainmenu_status = []

    # # ILK ELEMENT (NETWORK TABLES)
    # if msg:
    #     mainmenu.append("NETWORK TABLES CONNECTED")
    #     mainmenu_status.append(True)
    # if not msg:
    #     mainmenu.append("NETWORK TABLES NOT CONNECTED")
    #     mainmenu_status.append(False)
    # else:
    #     mianmenu.append("CAMERA NOT STARTED")
    #     mainmenu_status.append(False)

    # IKINCI ELEMENT (IS CAM ONLINE)
    if isCamOnline:
        mainmenu.append("CAMERA CONNECTED")
        mainmenu_status.append(True)

    if not isCamOnline:
        mainmenu.append("CAMERA NOT CONNECTED")
        mainmenu_status.append(False)

    # OK BUTTON
    mainmenu.append("OK")
    mainmenu_status.append("Normal")

    return [mainmenu, mainmenu_status]


def get_info_menu_values(teamnumber):
    menu = []
    menucheck = []

    menu.append("MADE FOR FRC 2020 SEASON")
    menucheck.append(True)

    menu.append("TUNAPRO123")
    menucheck.append(True)

    menu.append("ColonelKai")
    menucheck.append(True)

    menu.append("BlackShadow")
    menucheck.append(False)

    menu.append("NICE")
    menucheck.append(True)

    return [menu, menucheck]


def print_info(stdscr, input_str, color=3):
    errortimer = threading.Timer(0.1, print_error, args=[stdscr, input_str, color])
    errortimer.start()


def print_error(stdscr, cur_stat, color=2, wait_time=5):
    # verilen error mesajunu verilen zaman (genellikle 5 sn) kadar en üste yazan kod
    starttime = time.perf_counter() # başlama zamanı
    while True: 
        if type(cur_stat) == str: # eğer error mesajı direkt verildiyse direk yazdır
            errmsg = cur_stat
            if errmsg is not None:
                h, w = stdscr.getmaxyx()
                x = w // 2 - (len(errmsg) + 1) // 2
                y = h - 1
                stdscr.attron(curses.color_pair(color))
                stdscr.addstr(y, x, errmsg)
                stdscr.attroff(curses.color_pair(color))
                stdscr.refresh()

        elif cur_stat is not None: # eğer sözlük olarak verildiyse içinden alıp yazdır
            errmsg = cur_stat["current_error"]

            if errmsg is not None:
                h, w = stdscr.getmaxyx()
                x = w // 2 - (len(errmsg) + 1) // 2
                y = h - 1
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, x, errmsg)
                stdscr.attroff(curses.color_pair(2))
                stdscr.refresh()

        elif cur_stat is None: # eğer ilisi de değilse boş yazdır
            h, w = stdscr.getmaxyx()
            x = (w // 2) - (1 // 2)
            y = h - 1
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, "")
            stdscr.attroff(curses.color_pair(2))
            stdscr.refresh()
        timenow = time.perf_counter() # verilen zamanı geçiyorsa kapat
        if timenow - starttime > wait_time:
            break


def print_cam_offset_edit(stdscr, team_n, cam_offset_pos, cur_stat):
    # ayarlar menüsünde camera offset'in 3 hanesini tek tek ayarlamak için olan özel kod
    if cam_offset_pos is not None:
        h, w = stdscr.getmaxyx() # ekranın genişliğini ve yüksekliğini bulur
        cam_offset_pos_list = [] 

        for idx, i in enumerate(team_n): # burada team_n yazıyor ama başka kodumu copy-pasteledim aslında o cam_offset
            y = h // 2 # ekranın yükseklik olarak ortası
            x = w // 2 # ekranın genişlik olarak ortası

            x -=- 1 # x'e bir ekliyoruz 

            if cur_stat["current_menu"] == arduino_menu_value: # eğer ayarlar menüsünde isek

                if idx == 0: # eğer 1. hanede ise
                    x = x + 4 # x'i 1. hanenin yerini bulmak için değiştir
                    if cam_offset_pos == 0: # eğer 1. hane seçili ise
                        stdscr.attron(curses.color_pair(1)) # renk beyaz
                        stdscr.addstr(y, x, i) # 1. haneyi yazdır
                        stdscr.attroff(curses.color_pair(1))
                    else: # seçili değilse
                        stdscr.attron(curses.color_pair(3)) # renk normal
                        stdscr.addstr(y, x, i) # 1. haneyi yazdır
                        stdscr.attroff(curses.color_pair(3))

                # alttakiler de 1. hane ile aynı prensip ile çalışıyor
                if idx == 1: # 2. hane
                    x = x + 5
                    if cam_offset_pos == 1:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(3))

                if idx == 2: # 3. hane
                    x = x + 6
                    if cam_offset_pos == 2:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(3))

                # burası kaldırıldı
                x = w // 2 # x'i yeniden hesaplıyor
                x = x - 9 
                stdscr.attron(curses.color_pair(3))
                # stdscr.addstr(y, x, "TEAM NUMBER: ")
                stdscr.attroff(curses.color_pair(3))

                stdscr.refresh() # ekranı yeniliyor


def print_team_no_edit(stdscr, team_n, team_no_select, cur_stat):
    # print_cam_offset_edit ile aynısı, sadece konumu farklı ve 4 haneli
    if team_no_select is not None:
        h, w = stdscr.getmaxyx()
        for idx, i in enumerate(team_n):
            y = h // 2
            x = w // 2
            y -=- 1

            if cur_stat["current_menu"] == arduino_menu_value:

                if idx == 0:
                    x = x + 4
                    if team_no_select == 0:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(3))

                if idx == 1:
                    x = x + 5
                    if team_no_select == 1:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(3))

                if idx == 2:
                    x = x + 6
                    if team_no_select == 2:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(3))

                if idx == 3:
                    x = x + 7
                    if team_no_select == 3:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(3))

                x = w // 2
                x = x - 9
                stdscr.attron(curses.color_pair(3))
                # stdscr.addstr(y, x, "TEAM NUMBER: ")
                stdscr.attroff(curses.color_pair(3))

                stdscr.refresh()


def check_arduino_thread():
    global check_arduino_thread_rv
    # Devamlı olarak arduino'nun bağlantısını kontrol eden threaded kod.
    # not: threaded kodlardan beynim yok olmaya başladı
    check_arduino_thread.exitthread = False # bu fonksiyon kodun herhangi bir yerinde True olduğunda thread durucak kapa emri olarak kullanıyorum.

    # threaded olarak çalışacak fonksiyon
    def check_arduino_thread_actual(): #thread ile çalışacak kod
        global check_arduino_thread_rv
        check_arduino_thread.threadopen = True # thread'in açık olduğunu belirtiyor ki  birden fazla thread açılmasın
        check_arduino_thread.exitthread = False # kapatma emrinin kapalı olduğunu kontrol ediyor
        while True: # asıl döngü
            rv = ArduinoFunctions.check_ports() # portları kontrol eden fonksiyon
            try:
                if type(rv) == list and rv[0] is None and rv[0] == "": # eğer liste boşsa false döndür
                    # Bulunamadı
                    check_arduino_thread_rv = False       

                elif type(rv) == str and rv.startswith("InputP"): # eğer check_ports fonkisyonu error döndürdü ise false döndür
                    # ERROR
                    check_arduino_thread_rv = False

                elif type(rv) == list and rv[0] is not None and type(rv[0]) == str and not rv[0] == "": # eğer boş değilse true döndür
                    # bulundu
                    check_arduino_thread_rv = True

            except: # eğer error verirse false döndür
                # bulunamadı
                check_arduino_thread_rv = False

            #thread kapama emri kontrolü
            if check_arduino_thread.exitthread:    
                check_arduino_thread.exitthread = False                 
                break

            time.sleep(1) # thread fazla yüklemesin diye bekleme
        
        check_arduino_thread.threadopen = False # eğer threadin dışına çıkarsa threadin artık açık olmadığını söylüyor




    # Threadi çalıştıran kod. 
    # timer kullanmamın sebebi bunu yazarken henüz threading'in nasıl çalıştığını bilmiyordum 
    try:
        if not check_arduino_thread.threadopen: # eğer bir thread açık değilse aç
            arduino_check_timer = threading.Timer(0.1, check_arduino_thread_actual, [])
            arduino_check_timer.start()
    except: # eğer error verdiyse threadopen henüz verilmemiştir o yüzden yeni thread aç
        arduino_check_timer = threading.Timer(0.1, check_arduino_thread_actual, [])
        arduino_check_timer.start()


def flash_led(led):
    # obje olarak led verdiğin zaman dur komutuna kadar o ledi yakıp sönüyor
    # kodun geri kalanı check_arduino_thread() ile aynı mantıkla çalışıyor
    flash_led.exitthread = False 
    def flash_led_actual(led):
        flash_led.flashthreadopen = True
        while True:
            time.sleep(0.5)
            ArduinoFunctions.led_write(led, None, 1)
            time.sleep(0.5)
            ArduinoFunctions.led_write(led, None, 0)
            if flash_led.exitthread:
                break
        flash_led.flashthreadopen = False
    
    try:
        if not flash_led.flashthreadopen:
            flash_timer = threading.Timer(0.1, flash_led_actual, [led])
            flash_timer.start()
    except:
        flash_timer = threading.Timer(0.1, flash_led_actual, [led])
        flash_timer.start()


def print_current_menu(stdscr, cur_stat, led_blue = None, led_camera = None):
    # genel olarak her menüyü (panic mode ve match mode gibi istisnalar dışında) yazdıran fonksiyon
    # curses'ın screen objesini ve içinde menü elemanları olan cur_stat'a ihtiyacı var
    firsttime = True

    if type(cur_stat["current_menu_elements"][0]) is list: #eğer elemanlar listesi başka bir listenin içerisindeeyse
        cur_stat["current_menu_elements"] = cur_stat["current_menu_elements"][0] # onları listeden çıkar

    stdscr.clear() # ekranı temizle
    h, w = stdscr.getmaxyx() # ekranın enini ve boyunu al

    for idx, row in enumerate(cur_stat["current_menu_elements"]): # menü elemanlarındaki her elemanın üzerinden gider
        if cur_stat["current_menu_status"][idx]: # eğer eleman doğru ise yeşil
            colornumber = 3

        elif not cur_stat["current_menu_status"][idx]: # yanlış ise kırmızı
            colornumber = 2

        else: # başka ise normal 
            colornumber = 4

        x = w // 2 - (len(row) + 1) // 2 # elemanın uzunluğuna göre x'i ve y'yi ayarlıyor
        y = h // 2 - (len(cur_stat["current_menu_elements"]) + 1) // 2 + idx

        if idx == cur_stat["current_row"]: # eğer o eleman seçili ise beyaz
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))

        else: # değilse olması gereken renk.
            stdscr.attron(curses.color_pair(colornumber))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(colornumber))

        if firsttime: # eğer ilk seferse y'i bir azalt
            firsty = y - 1
            firsttime = False
        elif not firsttime:
            pass

    for i in cur_stat["all_menu_elements"][main_menu_value][1]: # tüm elemanların True mu false mı olduğunu arıyor
        if i: 
            match_message = " ## MATCH MODE CAN BE STARTED ## "
            match_message_color = 4
            if not led_blue is None and not led_camera is None:
                ArduinoFunctions.led_write(led_blue, led_camera, 1)
                match_mode_can_be_started = True
        else:
            match_message = " ## MATCH MODE CANNOT BE STARTED ## "
            match_message_color = 2
            if not led_blue is None:
                match_mode_can_be_started = False
                flash_led(led_blue)
            break

        # eğer hepsi doğru ise match mode can be started, eğer bir tanesi bile yanlış ise match mode cannot be started diyor

    firstx = w // 2 - (len(match_message) + 1) // 2 

    stdscr.attron(curses.color_pair(match_message_color))
    stdscr.addstr(firsty - 1, firstx, match_message)
    stdscr.attroff(curses.color_pair(match_message_color))

    teamname = "FRC7839 " #ekranın sağ üstünde ismimizi yazdırma olayı
    namex = w - len(teamname)
    namey = 0

    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(namey, namex, teamname)
    stdscr.attroff(curses.color_pair(3))

    stdscr.refresh() # ekranı yenilemek


def print_menu_for_match(stdscr, m_menu_elements):
    stdscr.clear() #ekranı temizle
    h, w = stdscr.getmaxyx() # en ve boy al

    for idx, row in enumerate(m_menu_elements): #verilen değerlerde
        x = w // 2 - (len(row) + 1) // 2 # y ve x hesaplamaları
        y = h // 2 - (len(m_menu_elements) + 1) // 2 + idx

        stdscr.attron(curses.color_pair(4)) #ekrana ekle
        stdscr.addstr(y, x, row)
        stdscr.attroff(curses.color_pair(4))

    stdscr.refresh() # ekranı yenile


def cursor_handler(key, cur_stat):
    # eğer bir menüde aşağıya gidilmek isterse bunu gerçekleştiren ve en altta ise yukarıya atan kod.
    # Imlec Asagi
    current_row = cur_stat["current_row"]

    if (key == "button1") and (
        current_row < (len(cur_stat["current_menu_elements"]) - 1)
    ):

        current_row += 1

    # Imlec Dongu (yeniden en yukarıya çıkması)
    elif (
        current_row == (len(cur_stat["current_menu_elements"]) - 1) and key == "button1"
    ):

        current_row = 0

    return current_row


def set_current_menu(cur_stat, all_menu_elements):
    cur_menu = int(cur_stat["current_menu"])

    cur_stat["current_menu_elements"] = all_menu_elements[cur_menu][0]
    cur_stat["current_menu_status"] = all_menu_elements[cur_menu][1]

    return cur_stat["current_menu_elements"], cur_stat["current_menu_status"]


def return_to_menu(key, cur_stat, stdscr):
    # bir menüdeyken en alttakı tuşa basıldı ise ana menüye geri atan kod.
    # Ana Menuye Cikma
    settings = None 
    if (
        (key == "button0")
        and cur_stat["current_menu"] != 0
        and cur_stat["current_row"] == (len(cur_stat["current_menu_elements"]) - 1)
    ):
        cur_stat["current_row"] = 0
        cur_stat["current_menu"] = 0

        settings = DbFunctions.get_setting(file_s)
        handle_error(settings, stdscr, PanicMenu=True)

    # write settings'de write settings butonuna bastığında da ana menüye atan kod
    if (
        (key == "button0")
        and cur_stat["current_menu"] == arduino_menu_value
        and cur_stat["current_row"] == (len(cur_stat["current_menu_elements"]) - 2)
    ):
        cur_stat["current_row"] = 0
        cur_stat["current_menu"] = 0

        settings = DbFunctions.get_setting(file_s)
        handle_error(settings, stdscr, PanicMenu=True)

    return cur_stat["current_row"], cur_stat["current_menu"], settings


def background_setup(stdscr, cur_stat=None, PanicMode=False):
    bruh = None
    #herhangi bir menüde iken tüm değerler True iken arkaplanı yeşil, değilken kırmızı yapan kod
    if PanicMode == True: 
        stdscr.bkgd(" ", curses.color_pair(2)) #burası arkaplanı ayarlayan curses fonksiyonu

    elif cur_stat is not None and cur_stat["current_menu"] == 0:
        for i in cur_stat["current_menu_status"]:
            if i:
                stdscr.bkgd(" ", curses.color_pair(3))
                bruh = 1

            elif not i:
                bruh = 0
                stdscr.bkgd(" ", curses.color_pair(2))
                break

    if bruh is not None and bruh == 1:
        flash_led.exitthread = True


    elif cur_stat is not None and cur_stat["current_menu"] != 0:
        stdscr.bkgd(" ", curses.color_pair(4))


def refresh_screen(stdscr, key, team_no_pos, cam_offset_pos, cur_stat, settings, team_ip2, led_blue = None, led_camera = None):
    # ekranda bir değişiklik yapıldığında gerekli değişiklikler yapılıp yeniden print_menu yapan kod
    new_all_menu_elements = cur_stat["all_menu_elements"] 

    new_all_menu_elements[main_menu_value] = get_first_menu_values(team_ip2) # ana menü değerlerini yeniden alıyor
    new_all_menu_elements[ip_menu_value] = get_ip_menu_values( # ip menüsü değerlerini yeniden alıyor
        team_ip2, InputPFunctions.get_ipaddr() # ip adresini yeniden kontrol ediyor
    )
    new_all_menu_elements[arduino_menu_value] = get_arduino_menu_values(settings) # ayarlar menüsü değerlerini yeniden alıyor
    new_all_menu_elements[camera_menu_value] = get_cam_menu_values() # camera menüsü değerlerini yeniden alıyor

    # cur_stat["all_menu_elements"] = new_all_menu_elements
    # cur_stat["current_menu_elements"] = new_all_menu_elements[c"ur_stat["current_menu"]]

    # Background seysi
    background_setup(stdscr, cur_stat) 

    # Background ayarlandiktan sonra menu yazdirildi
    print_current_menu(stdscr, cur_stat, led_blue, led_camera)

    # ayarlar menüsü için team_no olayı
    print_team_no_edit(stdscr, settings["Team Number"], team_no_pos, cur_stat)

    # ayarlar menüsü için camera_offset olayı
    print_cam_offset_edit(stdscr, settings["Camera Offset"], cam_offset_pos, cur_stat)

    return new_all_menu_elements


# region

# def handle_errors(stdscr=None, PanicMenu=True, *args):
#     for variable in args:
#         if type(variable) == str:
#             if str(variable).startswith("InputP"):
#                 background_setup(stdscr, None, PanicMode=True)

#                 if test_mode is not None:
#                     raise Exception(str(variable))

#                 else:
#                     if PanicMenu:
#                         match_mode(stdscr, PanicMenu=True, errmsg=variable)
#                     else:
#                         print_info(stdscr, variable, color=2, time=5)
#                     return True
#             else:
#                 return False

# endregion


def handle_error(err_msg, stdscr=None, PanicMenu=True, clean=False):
    # bir değer verildiğinde error olup olmadığını kontrol eden kod.
    # eğer panicmenu açık ise bir error olduğunu fark ettiğinde panic moda geçiyor.
    if type(err_msg) == str: # eğer verilen değer string ise
        if str(err_msg).startswith("InputP"): # ve error ise
            err_type = None 
            
            # error tipini bulmak için olan kod
            if err_msg in [all_errors[READ_ERR], all_errors[WRITE_ERR]]:
                err_type = "FILE"

            elif err_msg in [
                all_errors[ARDUINO_CONN_ERR],
                all_errors[ARDUINO_CONN_LOST],
                all_errors[ARDUINO_INPUT_ERR],
            ]:  #
                err_type = "ARDUINO"

            background_setup(stdscr, None, PanicMode=True) # arkaplanı kırmızı yapıyor

            if test_mode is not None: # eğer testmodu açık ise 
                raise Exception(str(err_msg)) # hata verdiriyor, panic moduna girmiyor

            else: # eğer test mode kapalı ise
                if PanicMenu: #eğer panic modu açıksa pnic moduna giriyor
                    match_mode(
                        stdscr, PanicMenu=True, errmsg=err_msg, err_type=err_type
                    )

                else: # eğer panic modu kapalı ise sadece ekrana error mesajını alta yazdırıyor
                    if not clean:
                        print_info(stdscr, err_msg, color=2)

                return True # error olduğu için true döndürüyor

        else: # eğer error değilse false döndürüyor
            return False


def set_tip(team_number):
    # ip kontrol için takım numarasını alıp kontrol ettiği ip değerini ayarlayan kod
    team_ip2 = team_number

    if len(team_ip2) == 3:
        team_ip2 = "0" + team_ip2[0] + "." + team_ip2[1:]

    elif len(team_ip2) == 4:
        team_ip2 = team_ip2[0:2] + "." + team_ip2[2:]

    return team_ip2


def not_main(stdscr):
    flash_led.exitthread = True
    # region while dongusune kadar olan gereksiz seyler

    # region Settings okuma
    settings = DbFunctions.get_setting(file_s)
    handle_error(settings, stdscr, PanicMenu=True)
    # endregion

    team_ip2 = set_tip(settings["Team Number"]) #takım numarasına göre ip ayarlıyor

    all_menu_elements = [] # her menünün elemanlarını alıyor
    all_menu_elements.append(get_first_menu_values(team_ip2)) 
    all_menu_elements.append(get_ip_menu_values(team_ip2, InputPFunctions.get_ipaddr()))
    all_menu_elements.append(get_arduino_menu_values(settings))
    all_menu_elements.append(get_cam_menu_values(None))
    all_menu_elements.append(get_info_menu_values(None))

    # Imlec konumu
    current_row = 0
    # Aktif olan menu
    current_menu = 0
    # Aktif olan menudeki elemanlar
    current_menu_elements = all_menu_elements[0][0]
    # Aktif olan menudeki elemanlarin renk degerleri
    current_menu_status = all_menu_elements[0][1]

    cur_stat = {
        "current_row": current_row,
        "current_menu": current_menu,
        "current_menu_elements": current_menu_elements,
        "current_menu_status": current_menu_status,
        "all_menu_elements": all_menu_elements,
    }

    # RENKLER
    # 2 = RED
    # 3 = GREEN
    # 4 = NORMAL

    # region curses renklerini ayarlayan kısım
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # endregion

    # Kodun calisip calismadipini anlamak icin kullandigimiz port 5802
    # Ve ledin kapanip acma bilgisinin yazildigi port da 5803

    # endregion

    team_no_pos = 9
    cam_offset_pos = 9
    msg = None
    key = None


    # ekranı yazdır
    refresh_screen(stdscr, key, team_no_pos, cam_offset_pos, cur_stat, settings, team_ip2)

    # time.sleep(1)
    # region arduino import

    # kod başlarken importing arduino mesajı verir
    # board = pyfirmata.ArduinoNano("COM4")
    errortimer = threading.Timer(0.1, print_error, args=[stdscr, "InputP: Importing Arduino...", 3])
    errortimer.start()


    # sonradan arasındaki farkı bulup ne kadar zaman geçtiğini anlamak için şimdiki zamanı alır
    start_t = timeit.default_timer()
    ###

    com_ports = ArduinoFunctions.check_ports() # com portları alır
    time.sleep(1)
    if type(com_ports) == list: # eğer com port'lara birşey takılı ise
        board = ArduinoFunctions.import_arduino(com_ports) # arduinoyu import et

    else: # yoksa error ver
        board = all_errors[ARDUINO_CONN_ERR] 

    ###
    # geçen zamanı bul
    elapsed = timeit.default_timer() - start_t
    
    #eğer 5 saniyeden az sürdü ise 5 saniyeyi tamamla (Çoğunlukla çok daha uzun sürüyor)
    if elapsed < 5:
        time.sleep(5 - elapsed)
        # error mesajı ver
        # errortimer = threading.Timer(0.1, print_error, args=[stdscr, None])
        # errortimer.start()

    # eğer arduino import edildi ise
    if not type(board) == str:

        # swt1 = board.get_pin("a:1:i")
        # pot1 = board.get_pin("a:2:i")
        # inp1 = board.get_pin("a:6:i")
        # led_camera = board.get_pin("d:10:p")
        # but1 = board.get_pin("d:2:i")
        # but2 = board.get_pin("d:7:i")
        # led1 = board.get_pin("d:11:p")
        
        # Tüm arduino pinlerin tanımlaması
        
        
        pot1 = board.get_pin(pot1_str)
        swt1 = board.get_pin(swt1_str)
        but1 = board.get_pin(but1_str)
        but2 = board.get_pin(but2_str)
        led_camera = board.get_pin(cam_str)
        led_blue = board.get_pin(blue_str)
        led_green = board.get_pin(green_str)
        led_red = board.get_pin(red_str)

        # butonların basıldığını anlamak için iteratörleri çalıştırır
        time.sleep(0.5)
        iterator= pyfirmata.util.Iterator(board)
        iterator.start()
        time.sleep(0.5)

        # eğer potansiyometreden değer okuyamazsa iteratör hata verdi demektir
        if pot1.read() is None:
            handle_error(all_errors[ARDUINO_INPUT_ERR], stdscr, PanicMenu=True)
        
    # eğer board str ise arduino import başarısız olmuş demektir
    elif type(board) == str:
        handle_error(board, stdscr)

    else:
        # Arduino basarili bir sekilde import edilirse mesaj verecek
        print_info(stdscr, all_infos[ARDUINO_CONNECTION_SUCCESS] , color=3)

    time.sleep(0.2)

    # endregion

    rv = ArduinoFunctions.led_write(led_blue, led_camera, 1.0) 
    handle_error(rv, stdscr, PanicMenu=True) # led ayarlamasından error mu döndü kontrol eder
    check_arduino_thread() # arduino takılımı diye kontrol eden thread başlar<< 
    time.sleep(0.5)
    
    while True:
    
        # eğer sadece bakacağın menülerde ise row'u çıkış butonuna kitler
        if cur_stat["current_menu"] == ip_menu_value:
            cur_stat["current_row"] = 4
        elif cur_stat["current_menu"] == camera_menu_value:
            cur_stat["current_row"] = 1
        elif cur_stat["current_menu"] == info_menu_value:
            cur_stat["current_row"] = 4

        ##########
        # Ekran yenilenmesi
        cur_stat["all_menu_elements"] = refresh_screen(
            stdscr, key, team_no_pos, cam_offset_pos, cur_stat,settings, team_ip2, led_blue, led_camera,
        )
        
        key, ports = ArduinoFunctions.key_get( # arduino'dan değer alır
            but1, but2, pot1, wait_time_for_get_key
        )

        if key is None: # eğer None döndürürse
            isKeyError = True # hata verdi demektir
        else:
            isKeyError = False

        handle_error(ports, stdscr, PanicMenu=True) # hatalı mı kontrol

        if key is None:
            continue

        handle_error(key, stdscr, PanicMenu=True) # hata var mı kontrol

        # Imlec hareketleri degiskenlere yazildi
        cur_stat["current_row"] = cursor_handler(key, cur_stat)

        ##########

        # arduino_check_thread kullanımı
        # not: lütfen tüm değişkenleri okuma/yazma olaylarını "Try/except" içine alın thread başlamadı ise hata verir
        # thread başlatmak için: arduino_check_thread()
        # threadi durdurmak için: arduino_check_thread.exitthread = True (try except içine al)
        # thread'den değer okumak için (example yerine değerin yazılmasını istediğiniz değişken): example = arduino_check_thread.rv (try except içine al)
        
        
        for i in cur_stat["all_menu_elements"][main_menu_value][1]: # eğer menüdeki herşey True ise Match Mod'a girebilir hale getirir
            if i:
                canGoToMM = True
            elif not i:
                canGoToMM = False
                break
        pass            
        # Mac Modu
        if (
            canGoToMM == True
            and ArduinoFunctions.map_x(pot1.read(), 0, 1, 0, max_v) == 0 # eğer potansiyometre en solda ve switch de solda ise 
            and ArduinoFunctions.map_xi(swt1.read(), 0, 1, 0, max_v) == max_v
            and cur_stat["current_menu"] == main_menu_value
        ):
            match_mode(stdscr, settings, led_blue, led_camera, led_red, led_green, swt1, pot1, isKeyError) # match mode başlat
        # region arduino menu ozel
        if cur_stat["current_menu"] == 2: # eğer arudino menüsünde ise potansiyomentre'den değer okuyan yer
            if (
                key not in ["button1", "button0", "switch on", "switch off"] 
                and cur_stat["current_row"] == 0 # eğer robo_loc'da ise
            ):
                settings["Robot Location"] = ArduinoFunctions.get_robo_loc_from_inp(
                    key, max_v
                )

            elif (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 1 # cam_tol'de ise
            ):
                settings["Camera Tolerance"] = str(key)

            elif (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 2 # waiting_period'da ise
            ):
                settings["Waiting Period"] = str(key // 2)

            elif (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 3 # autonomus_mod'da ise
            ):
                settings["Autonomous Mode"] = str(
                    ArduinoFunctions.map_x(key, 0, max_v, 0, 5)
                )

            if cur_stat["current_row"] == 5 and team_no_pos == 9:
                team_no_pos = 0
            if cur_stat["current_row"] == 4 and cam_offset_pos == 9:
                cam_offset_pos = 0


            # Team degistirme seysi
            if cur_stat["current_row"] == 5:
                if key == "button0": # buton0'a bastığında sonraki haneye geçer
                    if team_no_pos < 4:
                        team_no_pos += 1

                    if team_no_pos >= 4:
                        team_no_pos = 0

                if type(key) == int: # eğer potansiyometre değeri ise o haneye atar
                    settings["Team Number"] = (
                        settings["Team Number"][0:team_no_pos]
                        + str(ArduinoFunctions.map_x(key, 0, max_v, 0, 9))
                        + settings["Team Number"][(team_no_pos + 1) : 4]
                    )

            if cur_stat["current_row"] == 4: 
                if key == "button0": # buton0'a bastığında sonraki haneye geçer
                    if cam_offset_pos < 3:
                        cam_offset_pos += 1

                    if cam_offset_pos >= 3:
                        cam_offset_pos = 0
                    
                
                if type(key) == int:
                    settings["Camera Offset"] = (
                        settings["Camera Offset"][0:cam_offset_pos]
                        + str(ArduinoFunctions.map_x(key, 0, max_v, 0, 9))
                        + settings["Camera Offset"][(cam_offset_pos + 1) : 3]
                    )



            if cur_stat["current_row"] != 5:
                team_no_pos = 9  # 9 sadece 0 ile 3 arasinda olmayan bir deger olarak

            
            if cur_stat["current_row"] != 4:
                cam_offset_pos = 9  # 9 sadece 0 ile 3 arasinda olmayan bir deger olarak


            # Write tusu, ayarları JSON dosyasına yazar
            if key == "button0" and cur_stat["current_row"] == 6:

                rv = DbFunctions.save_settings(file_s, settings)
                handle_error(rv, stdscr, PanicMenu=True)

                # if waiting_period is not None:
                #     DbFunctions.write_setting_to_txt(waiting_period, file)

            all_menu_elements[2] = get_arduino_menu_values(settings)

            cur_stat["current_menu_elements"] = all_menu_elements[2][0]
            cur_stat["current_menu_status"] = all_menu_elements[2][1]

        # endregion


        # Menu degistirme olaylari
        cur_stat["current_row"], cur_stat["current_menu"], rv = InputPFunctions.change_menu( 
            key, cur_stat, led_green, led_camera
        )
        handle_error(rv, stdscr, PanicMenu=False, clean=False)
        
        # ana menüye dönme
        cur_stat["current_row"], cur_stat["current_menu"], sett = return_to_menu(
            key, cur_stat, stdscr
        )
        (
            cur_stat["current_menu_elements"],
            cur_stat["current_menu_status"],
        ) = set_current_menu(cur_stat, all_menu_elements)
        # team_ip'yi yeniden hesaplama
        team_ip2 = set_tip(settings["Team Number"])

        if sett is not None and not type(sett) == 4:
            settings = sett

        try:
            rv = check_arduino_thread_rv # arduino takılı mı
        except:
            pass
        else:
            if not rv:
                handle_error(all_errors[ARDUINO_CONN_LOST], stdscr, True) # error verdi mi kontrol
        
try:
    curses.wrapper(not_main)
except KeyboardInterrupt:
    try:
        if flash_led.flashthreadopen:
            flash_led.exitthread = True 
    except:
        pass
    