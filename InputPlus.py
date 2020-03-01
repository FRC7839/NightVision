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


if os.name == "nt":
    from frc_lib7839 import *
    pc_mode = 1

if pc_mode is not None and os.name == "posix":
    sys.path.insert(1, '/home/pi/NightVision')
    from frc_lib7839 import *


# if pc_mode is not None:
#     skip_cam_arg = 1
#     skip_nt_arg = 1

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
    if not PanicMenu:
        try:
            if flash_led.flashthreadopen:
                flash_led.exitthread = True
        except:
            pass
        led_blue.write(0)
        led_green.write(1)
        led_control = {}
        # Ana yer
        while True:
            # Dosyadan okumayi dene
            led_control = DbFunctions.get_setting(file_lc)  # led control dosyasindan ayari cekiyor
            handle_error(led_control, stdscr, PanicMenu=True)

            settings["Match Mode Status"] = True

            m_menu_elements = []  # Menu elementleri arrayi
            m_menu_elements.append(" ## MATCH MODE STARTED ## ")  # Title

            # LED Bilgisayar tarafindan kontrol ediliyor ve menu bunu gosteriyor
            if led_control["Led Status"] is not None and led_control["Led Status"] in [
                True,
                False,
                "True",
                "False",
            ]:
                m_menu_elements.append(
                    " ## LED CONTROL : " + str(led_control["Led Status"]) + " ## "
                )

            # Eger kapali ya da acik alamazsa error veriyor.
            else:
                m_menu_elements.append(" ## LED CONTROL FAILED ## ")
                led_control["Led Status"] = True

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

            if flash_led.flashthreadopen:
                flash_led.exitthread = True 

            if led_control["Led Status"] in ["True", True]:
                ArduinoFunctions.led_write(led_green, led_camera, 1)  # on


            elif led_control["Led Status"] in ["False", False]:
                ArduinoFunctions.led_write(None, led_camera, 0)  # off
                flash_led(led_green)

            else:
                ArduinoFunctions.led_write(led_green, led_camera, 1)  # on

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

                rv = DbFunctions.save_settings(file_s, settings)
                handle_error(rv, stdscr, PanicMenu=True)

                break

    ### KERNEL PANIC ###
    else:

        try:
            if flash_led.flashthreadopen:
                flash_led.exitthread = True
        except:
            pass

        try:
            led_red.write(1)
        except:
            pass
        
        settings = DbFunctions.get_setting(file_s)
        led_control = DbFunctions.get_setting(file_lc)  # led control dosyasindan ayari cekiyor

        if handle_error(led_control, stdscr, PanicMenu=False) or handle_error(settings, stdscr, PanicMenu=False):
            led_control = {}
            settings = {}

            for i in range(len(lc_names)):
                led_control[lc_names[i]] = lc_defaults[i]

            for i in range(len(setting_names)):
                settings[setting_names[i]] = setting_defaults[i]

            f_err = True

        m_menu_elements = []  # Menu elementleri arrayi
        m_menu_elements.append(" ## PANIC MODE STARTED ## ")  # Title

        # LED Bilgisayar tarafindan kontrol ediliyor ve menu bunu gosteriyor
        if led_control["Led Status"] is not None and led_control["Led Status"] in [True,False,"True","False",]:
            m_menu_elements.append(" ## LED CONTROL : " + str(led_control["Led Status"]) + " ## ")

        # Eger kapali yada acik alamazsa error veriyor.
        else:
            m_menu_elements.append(" ## LED CONTROL FAILED ## ")

            led_control["Led Status"] = True
            rv = DbFunctions.save_settings(file_lc, led_control)  # Olmazsa yapacak bir sey yok
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

        while True:

            print_menu_for_match(stdscr, m_menu_elements)
            time.sleep(1)

            if type(errmsg) == str and errmsg.startswith("InputP"):
                print_info(stdscr, errmsg, color=2)
                errmsg = None

            background_setup(stdscr, None, PanicMode=True)

            if type(err_type) == str and err_type == "ARDUINO":
                rv2 = ArduinoFunctions.check_ports()

                try:
                    if swt1.read() is None and rv2 != all_errors[ARDUINO_CONN_LOST]:
                        isReadError = True
                    else:
                        isReadError = False
                except:
                    if rv2 != all_errors[ARDUINO_CONN_LOST]:
                        isReadError = True
                    else:
                        isReadError = False

                if not handle_error(rv2, stdscr, PanicMenu=False, clean=True) and not isReadError:
                    not_main(stdscr)
                    led_red.write(0)


def get_first_menu_values(team_ip2):
    ipaddr_func = InputPFunctions.get_ipaddr()
    check_cam_func = InputPFunctions.check_cam()

    mainmenu = []
    mainmenucheck = []

    if skip_nt_arg is not None:
        mainmenu.append("SKIPPED NETWORK CHECKING")
        mainmenucheck.append(True)

    elif ipaddr_func.startswith("127"):
        mainmenu.append("IP ADRESS: NOT CONNECTED")
        mainmenucheck.append(False)  ## False

    elif not ipaddr_func.startswith("10." + team_ip2):
        mainmenu.append("NOT CONNECTED TO RADIO")
        mainmenucheck.append(False)  ## False

    else:
        mainmenu.append("IP ADRESS: " + ipaddr_func)
        mainmenucheck.append(True)

    mainmenu.append("SETTINGS")
    mainmenucheck.append(True)

    if skip_cam_arg is not None:
        mainmenu.append("SKIPPED CAMERA CHECKING")
        mainmenucheck.append(True)

    elif (
        check_cam_func == "CAMERA CONNECTED"
        or check_cam_func == "TRUE BECAUSE WINDOWS"
    ):
        mainmenu.append(check_cam_func)
        mainmenucheck.append(True)

    else:
        mainmenu.append(str(check_cam_func))
        mainmenucheck.append(False)  ## False

    mainmenu.append("LED TEST")
    mainmenucheck.append(True)

    mainmenu.append("INFO")
    mainmenucheck.append(True)

    mainmenu.append("REBOOT")
    mainmenucheck.append(True)

    mainmenu.append("EXIT")
    mainmenucheck.append(True)

    return [mainmenu, mainmenucheck]


def get_ip_menu_values(
    team_ip2,
    ipaddr_func=InputPFunctions.get_ipaddr(),
):
    mainmenu = []
    mainmenu_status = []

    if skip_nt_arg is not None:
        mainmenu.append(" ## SKIPPED NETWORK CHECKING ## ")
        mainmenu_status.append(False)

    else:
        mainmenu.append("")
        mainmenu_status.append(False)

    mainmenu.append("HOSTNAME: " + str(socket.gethostname()))
    mainmenu.append("IP ADRESS: " + ipaddr_func)
    mainmenu.append("RADIO IP RANGE: 10." + team_ip2 + ".0/24")

    mainmenu.append("OK")

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
    starttime = time.perf_counter()
    while True:
        if type(cur_stat) == str:
            errmsg = cur_stat
            if errmsg is not None:
                h, w = stdscr.getmaxyx()
                x = w // 2 - (len(errmsg) + 1) // 2
                y = h - 1
                stdscr.attron(curses.color_pair(color))
                stdscr.addstr(y, x, errmsg)
                stdscr.attroff(curses.color_pair(color))
                stdscr.refresh()

        elif cur_stat is not None:
            errmsg = cur_stat["current_error"]

            if errmsg is not None:
                h, w = stdscr.getmaxyx()
                x = w // 2 - (len(errmsg) + 1) // 2
                y = h - 1
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, x, errmsg)
                stdscr.attroff(curses.color_pair(2))
                stdscr.refresh()

        elif cur_stat is None:
            h, w = stdscr.getmaxyx()
            x = (w // 2) - (1 // 2)
            y = h - 1
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, "")
            stdscr.attroff(curses.color_pair(2))
            stdscr.refresh()
        timenow = time.perf_counter()
        if timenow - starttime > wait_time:
            break


def print_cam_offset_edit(stdscr, team_n, cam_offset_pos, cur_stat):
    if cam_offset_pos is not None:
        h, w = stdscr.getmaxyx()
        cam_offset_pos_list = []

        for idx, i in enumerate(team_n):
            y = h // 2
            x = w // 2

            x -=- 1

            if cur_stat["current_menu"] == arduino_menu_value:

                if idx == 0:
                    x = x + 4
                    if cam_offset_pos == 0:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(3))

                if idx == 1:
                    x = x + 5
                    if cam_offset_pos == 1:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y, x, i)
                        stdscr.attroff(curses.color_pair(3))

                if idx == 2:
                    x = x + 6
                    if cam_offset_pos == 2:
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


def print_team_no_edit(stdscr, team_n, team_no_select, cur_stat):
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


def flash_led(led):
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
    firsttime = True

    if type(cur_stat["current_menu_elements"][0]) is list:
        cur_stat["current_menu_elements"] = cur_stat["current_menu_elements"][0]

    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(cur_stat["current_menu_elements"]):
        if cur_stat["current_menu_status"][idx]:
            colornumber = 3

        elif not cur_stat["current_menu_status"][idx]:
            colornumber = 2

        else:
            colornumber = 4

        x = w // 2 - (len(row) + 1) // 2
        y = h // 2 - (len(cur_stat["current_menu_elements"]) + 1) // 2 + idx

        if idx == cur_stat["current_row"]:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))

        else:
            stdscr.attron(curses.color_pair(colornumber))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(colornumber))

        if firsttime:
            firsty = y - 1
            firsttime = False
        elif not firsttime:
            pass

    for i in cur_stat["all_menu_elements"][main_menu_value][1]:
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

    firstx = w // 2 - (len(match_message) + 1) // 2

    stdscr.attron(curses.color_pair(match_message_color))
    stdscr.addstr(firsty - 1, firstx, match_message)
    stdscr.attroff(curses.color_pair(match_message_color))

    teamname = "FRC7839 "
    namex = w - len(teamname)
    namey = 0

    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(namey, namex, teamname)
    stdscr.attroff(curses.color_pair(3))

    stdscr.refresh()


def print_menu_for_match(stdscr, m_menu_elements):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(m_menu_elements):
        x = w // 2 - (len(row) + 1) // 2
        y = h // 2 - (len(m_menu_elements) + 1) // 2 + idx

        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(y, x, row)
        stdscr.attroff(curses.color_pair(4))

    stdscr.refresh()


def cursor_handler(key, cur_stat):
    # Imlec Asagi
    current_row = cur_stat["current_row"]

    if (key == "button1") and (
        current_row < (len(cur_stat["current_menu_elements"]) - 1)
    ):

        current_row += 1

    # Imlec Dongu
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

    # write settings icin
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
    if PanicMode == True:
        stdscr.bkgd(" ", curses.color_pair(2))

    elif cur_stat is not None and cur_stat["current_menu"] == 0:
        for i in cur_stat["current_menu_status"]:
            if i:
                stdscr.bkgd(" ", curses.color_pair(3))

            elif not i:
                stdscr.bkgd(" ", curses.color_pair(2))
                break

    elif cur_stat is not None and cur_stat["current_menu"] != 0:
        stdscr.bkgd(" ", curses.color_pair(4))


def refresh_screen(stdscr, key, team_no_pos, cam_offset_pos, cur_stat, settings, team_ip2, led_blue = None, led_camera = None):
    new_all_menu_elements = cur_stat["all_menu_elements"]

    new_all_menu_elements[main_menu_value] = get_first_menu_values(team_ip2)
    new_all_menu_elements[ip_menu_value] = get_ip_menu_values(
        team_ip2, InputPFunctions.get_ipaddr()
    )
    new_all_menu_elements[arduino_menu_value] = get_arduino_menu_values(settings)
    new_all_menu_elements[camera_menu_value] = get_cam_menu_values()

    # cur_stat["all_menu_elements"] = new_all_menu_elements
    # cur_stat["current_menu_elements"] = new_all_menu_elements[c"ur_stat["current_menu"]]

    # Background seysi
    background_setup(stdscr, cur_stat)

    # Background ayarlandiktan sonra menu yazdirildi
    print_current_menu(stdscr, cur_stat, led_blue, led_camera)

    print_team_no_edit(stdscr, settings["Team Number"], team_no_pos, cur_stat)

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
    if type(err_msg) == str:
        if str(err_msg).startswith("InputP"):
            err_type = None

            if err_msg in [all_errors[READ_ERR], all_errors[WRITE_ERR]]:
                err_type = "FILE"

            elif err_msg in [
                all_errors[ARDUINO_CONN_ERR],
                all_errors[ARDUINO_CONN_LOST],
                all_errors[ARDUINO_INPUT_ERR],
            ]:  #
                err_type = "ARDUINO"

            background_setup(stdscr, None, PanicMode=True)

            if test_mode is not None:
                raise Exception(str(err_msg))

            else:
                if PanicMenu:
                    match_mode(
                        stdscr, PanicMenu=True, errmsg=err_msg, err_type=err_type
                    )

                else:
                    if not clean:
                        print_info(stdscr, err_msg, color=2)

                return True

        else:
            return False


def set_tip(team_number):
    team_ip2 = team_number

    if len(team_ip2) == 3:
        team_ip2 = "0" + team_ip2[0] + "." + team_ip2[1:]

    elif len(team_ip2) == 4:
        team_ip2 = team_ip2[0:2] + "." + team_ip2[2:]

    return team_ip2


def not_main(stdscr):
    # region while dongusune kadar olan gereksiz seyler

    # region Settings okuma
    settings = DbFunctions.get_setting(file_s)
    handle_error(settings, stdscr, PanicMenu=True)
    # endregion

    team_ip2 = set_tip(settings["Team Number"])

    all_menu_elements = []
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

    # region curses background set

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



    refresh_screen(stdscr, key, team_no_pos, cam_offset_pos, cur_stat, settings, team_ip2)

    # time.sleep(1)
    # region arduino import

    # board = pyfirmata.ArduinoNano("COM4")
    errortimer = threading.Timer(0.1, print_error, args=[stdscr, "InputP: Importing Arduino...", 3])
    errortimer.start()



    start_t = timeit.default_timer()
    ###

    com_ports = ArduinoFunctions.check_ports()

    if type(com_ports) == list:
        board = ArduinoFunctions.import_arduino(com_ports)

    else:
        board = all_errors[ARDUINO_CONN_ERR]

    ###
    elapsed = timeit.default_timer() - start_t

    if elapsed < 5:
        time.sleep(5 - elapsed)

        errortimer = threading.Timer(0.1, print_error, args=[stdscr, None])
        errortimer.start()


    if not type(board) == str:

        # swt1 = board.get_pin("a:1:i")
        # pot1 = board.get_pin("a:2:i")
        # inp1 = board.get_pin("a:6:i")
        # led_camera = board.get_pin("d:10:p")
        # but1 = board.get_pin("d:2:i")
        # but2 = board.get_pin("d:7:i")
        # led1 = board.get_pin("d:11:p")
        
        pot1 = board.get_pin("a:0:i")
        swt1 = board.get_pin("d:5:i")
        but1 = board.get_pin("d:6:i")
        but2 = board.get_pin("d:7:i")
        
        led_camera = board.get_pin("d:3:o")
        led_blue = board.get_pin("d:9:p")
        led_green = board.get_pin("d:10:p")
        led_red = board.get_pin("d:11:p")

        time.sleep(0.5)
        iterator= pyfirmata.util.Iterator(board)
        iterator.start()
        time.sleep(0.5)

        if pot1.read() is None:
            handle_error(all_errors[ARDUINO_INPUT_ERR], stdscr, PanicMenu=True)
        
    elif type(board) == str:
        handle_error(board, stdscr)

    else:
        # Arduino basarili bir sekilde import edilirse mesaj verecek
        print_info(stdscr, all_infos[ARDUINO_CONNECTION_SUCCESS] , color=3)

    time.sleep(0.2)

    # endregion

    rv = ArduinoFunctions.led_write(led_blue, led_camera, 1.0)
    handle_error(rv, stdscr, PanicMenu=True)

    while True:

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
        
        key, ports = ArduinoFunctions.key_get(
            but1, but2, pot1, wait_time_for_get_key
        )

        if key is None:
            isKeyError = True
        else:
            isKeyError = False

        handle_error(ports, stdscr, PanicMenu=True)

        if key is None:
            continue

        handle_error(key, stdscr, PanicMenu=True)

        # Imlec hareketleri degiskenlere yazildi
        cur_stat["current_row"] = cursor_handler(key, cur_stat)

        ##########

        for i in cur_stat["all_menu_elements"][main_menu_value][1]:
            if i:
                canGoToMM = True

            elif not i:
                canGoToMM = False
                break
        pass
        # Mac Modu
        if (
            canGoToMM == True
            and ArduinoFunctions.map_x(pot1.read(), 0, 1, 0, max_v) == 0
            and ArduinoFunctions.map_xi(swt1.read(), 0, 1, 0, max_v) == max_v
            and cur_stat["current_menu"] == main_menu_value
        ):
            match_mode(stdscr, settings, led_blue, led_camera, led_red, led_green, swt1, pot1, isKeyError)

        # region arduino menu ozel
        if cur_stat["current_menu"] == 2:
            if (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 0
            ):
                settings["Robot Location"] = ArduinoFunctions.get_robo_loc_from_inp(
                    key, max_v
                )

            elif (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 1
            ):
                settings["Camera Tolerance"] = str(key)

            elif (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 2
            ):
                settings["Waiting Period"] = str(key // 2)

            elif (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 3
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
                if key == "button0":
                    if team_no_pos < 4:
                        team_no_pos += 1

                    if team_no_pos >= 4:
                        team_no_pos = 0

                if type(key) == int:
                    settings["Team Number"] = (
                        settings["Team Number"][0:team_no_pos]
                        + str(ArduinoFunctions.map_x(key, 0, max_v, 0, 9))
                        + settings["Team Number"][(team_no_pos + 1) : 4]
                    )

            if cur_stat["current_row"] == 4:
                if key == "button0":
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


            # Write tusu
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
        
        cur_stat["current_row"], cur_stat["current_menu"], sett = return_to_menu(
            key, cur_stat, stdscr
        )
        (
            cur_stat["current_menu_elements"],
            cur_stat["current_menu_status"],
        ) = set_current_menu(cur_stat, all_menu_elements)

        team_ip2 = set_tip(settings["Team Number"])

        if sett is not None and not type(sett) == 4:
            settings = sett


curses.wrapper(not_main)

