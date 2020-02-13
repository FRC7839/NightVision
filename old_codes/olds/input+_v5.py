import frc7839_lib
import pyfirmata
import curses
import socket
import time
import zmq
import os

global arduino_menu_value
global camera_menu_value
global cam_curses_port1
global cam_curses_port2
global main_menu_value
global check_cam_port
global robot_settings
global ip_menu_value
global file

robot_settings = ["istunapro", "robot_location", "camera_tolerance", "waiting_period"]
cam_curses_port1 = frc7839_lib.cam_curses_port1
cam_curses_port2 = frc7839_lib.cam_curses_port2
check_cam_port = frc7839_lib.check_cam_port
arduino_menu_value = 2
camera_menu_value = 3
main_menu_value = 0
ip_menu_value = 1
file = "settings.txt"


# ArduinoFunctions.led_write(led, led2, 1 veya 0)
# awimbawe

# Sadece txt olayları fonksiyonları için:
# check_settings_on_txt() fonksiyonu verilen dosyada aynı ayardan birden fazla olup olmadığını test ediyor
# save_setting_on_txt() write_settings_on_txt() fonksiyounu kullanrak dosyaydaki her şeyi alıp tekrar yazması gerekiyor
# read basit zaten
# curses_funcitons içine class aç ve "from curses_funcitons import classes" yap çok havalı duruyor
# Ayrıca bunları curses_funcions içinde başka bir class içine çek


# def sendValuesToCamera(robot_location, ip_addr_func="127.0.0.1", camera_tolerance="15"):
#     settings = []

#     settings = frc7839_lib.DbFunctions.addSetting("isTest", "True", settings)
#     settings = frc7839_lib.DbFunctions.addSetting("robot_location", robot_location, settings)
#     settings = frc7839_lib.DbFunctions.addSetting("camera_tolerance", camera_tolerance, settings)
#     settings = frc7839_lib.DbFunctions.addSetting("ip_address", ip_addr_func, settings)

#     return status


# region checkNT
# def checkNT(socket5802):
#     msg = frc7839_lib.recv2(socket5802, nt_read_time)

#     if msg != "" and msg is not None:
#         msg_r = msg.split("#")
#         msg_r = frc7839_lib.find_setting(msg_r, "is_network_tables_started")

#         if msg_r == "True":
#             return "NT CONNECTED"

#         else:
#             return "NT NOT CONNETED"

#     elif msg is None:
#         return "CAMERA.PY NOT STARTED"
# endregion


def check_cam():
    if os.name == "nt":
        return "TRUE BECAUSE WINDOWS"

    elif os.name == "posix" and socket5802.gethostname() == "frcvision":
        if os.path.exists("/dev/video0"):
            return "CAMERA.PY CONNECTED"

        else:
            return "CAMERA NOT FOUND"


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


def get_ssid():
    if os.name == "nt":
        return "Tunapro1234 7/2/2020"

    if os.name == "posix":
        ssid = os.popen(
            "iwconfig wlan0 \
                | grep 'ESSID' \
                | awk '{print $4}' \
                | awk -F\\\" '{print $2}'"
        ).read()

        return ssid


def get_first_menu_values(nt_stat=None):
    ipaddr_func = get_ipaddr()
    check_cam_func = get_cam_menu_values(nt_stat)[0][0]

    mainmenu = []
    mainmenucheck = []

    if ipaddr_func.startswith("127"):
        mainmenu.append("IP ADRESS: NOT CONNECTED")
        mainmenucheck.append(False)

    elif not ipaddr_func.startswith("10.78.39"):
        mainmenu.append("NOT CONNECTED TO RADIO")
        mainmenucheck.append(False)

    else:
        mainmenu.append("IP ADRESS: " + ipaddr_func)
        mainmenucheck.append(True)

    mainmenu.append("ARDUINO CONFIG")
    mainmenucheck.append(True)

    if check_cam_func == "NT CONNECTED":
        mainmenu.append(check_cam_func)
        mainmenucheck.append(True)
    else:
        mainmenu.append(str(check_cam_func))
        mainmenucheck.append(False)

    mainmenu.append("LED TEST")
    mainmenucheck.append(True)

    mainmenu.append("EXIT")
    mainmenucheck.append("Normal")

    return [mainmenu, mainmenucheck]


def get_ip_menu_values(ssid_func=get_ssid(), ipaddr_func=get_ipaddr()):
    mainmenu = []
    mainmenu_status = []

    mainmenu.append("HOSTNAME: " + str(socket.gethostname()))
    mainmenu.append("SSID: " + str(ssid_func))
    mainmenu.append("IP ADRESS: " + ipaddr_func)
    mainmenu.append("OK")

    mainmenu_status.append("Normal")

    if str(socket.gethostname()) != "frcvision":
        mainmenu_status[0] = False

    if ipaddr_func.startswith("127"):
        mainmenu_status.append(False)
        mainmenu_status.append(False)
        mainmenu[2] = "IP ADRESS: NOT CONNECTED"

    elif ipaddr_func.startswith("10.78.39"):
        mainmenu_status.append(False)
        mainmenu_status.append(False)

    else:
        mainmenu_status.append("Normal")
        mainmenu_status.append("Normal")

    mainmenu_status.append("Normal")

    return [mainmenu, mainmenu_status]


def get_arduino_menu_values(
    send_func_msg=None, robot_location=None, camera_tolerance=None
):
    mainmenu = []
    mainmenu_status = []

    if robot_location is None:
        mainmenu.append("INPUT FOR ROBOT LOCATION")
        mainmenu_status.append(False)

    else:
        mainmenu.append("ROBOT LOCATION: " + robot_location)
        mainmenu_status.append("Normal")

    if camera_tolerance is None:
        mainmenu.append("INPUT FOR CAMERA TOLERANCE")
        mainmenu_status.append(False)

    else:
        mainmenu.append("CAMERA TOLERANCE: " + camera_tolerance)
        mainmenu_status.append("Normal")

    mainmenu.append("WRITE CURRENT SETTINGS TO FILE")
    mainmenu_status.append("Normal")

    mainmenu.append("OK")
    mainmenu_status.append("Normal"),

    return [mainmenu, mainmenu_status]


def get_cam_menu_values(nt_stat, isCamOnline=check_cam()):
    mainmenu = []
    mainmenu_status = []

    # ILK ELEMENT (NETWORK TABLES)
    if nt_stat == "NT CONNECTED":
        mainmenu.append(nt_stat)
        mainmenu_status.append(True)

    elif nt_stat is None:
        mainmenu.append("NT NOT CHECKED")
        mainmenu_status.append(False)

    else:
        mainmenu.append(nt_stat)
        mainmenu_status.append(False)

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


def print_current_menu(stdscr, cur_stat):
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
        y = h // 2 - (len(cur_stat["current_menu_elements"]) + 1 ) // 2 + idx

        if idx == cur_stat["current_row"]:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))

        else:
            stdscr.attron(curses.color_pair(colornumber))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(colornumber))

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


def return_to_menu(key, cur_stat):
    # Ana Menuye Cikma
    if (
        (key == "button0")
        and cur_stat["current_menu"] != 0
        and cur_stat["current_row"] == (len(cur_stat["current_menu_elements"]) - 1)
    ):
        cur_stat["current_row"] = 0
        cur_stat["current_menu"] = 0

    return cur_stat["current_menu"], cur_stat["current_row"]


def background_setup(stdscr, cur_stat):
    if cur_stat["current_menu"] == 0:
        for i in cur_stat["current_menu_status"]:
            if i:
                stdscr.bkgd(" ", curses.color_pair(3))

            elif not i:
                stdscr.bkgd(" ", curses.color_pair(2))
                break

    elif cur_stat["current_menu"] != 0:
        stdscr.bkgd(" ", curses.color_pair(4))


def refresh_screen(stdscr, cur_stat, key, nt_stat):
    new_all_menu_elements = cur_stat["all_menu_elements"]

    new_all_menu_elements[main_menu_value] = get_first_menu_values(nt_stat)
    new_all_menu_elements[ip_menu_value] = get_ip_menu_values(get_ssid(), get_ipaddr())
    new_all_menu_elements[arduino_menu_value] = get_arduino_menu_values()
    new_all_menu_elements[camera_menu_value] = get_cam_menu_values(nt_stat)

    # cur_stat["all_menu_elements"] = new_all_menu_elements
    # cur_stat["current_menu_elements"] = new_all_menu_elements[cur_stat["current_menu"]]

    # Background seysi
    background_setup(stdscr, cur_stat)

    # Background ayarlandiktan sonra menu yazdirildi
    print_current_menu(stdscr, cur_stat)

    return new_all_menu_elements


def not_main(stdscr):

    # region while dongusune kadar olan gereksiz seyler
    # Tum menu elemanlari all_menu_elemants adinda bir fonksiyon icinde duruyor
    # Sebebini sormak sizin gercekten zeki oldugunuzu gosterir
    # Neden oldugunu bilmiyorum, sadece boyle daha karmasik ve daha havali duruyor
    all_menu_elements = []
    all_menu_elements.append(get_first_menu_values())
    all_menu_elements.append(get_ip_menu_values())
    all_menu_elements.append(get_arduino_menu_values())
    all_menu_elements.append(get_cam_menu_values(None))

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

    # region arduino import

    board = frc7839_lib.ArduinoFunctions.import_arduino()
    # board = pyfirmata.ArduinoNano("COM4")
    
    
    swt1 = board.get_pin("a:1:i")
    pot1 = board.get_pin("a:2:i")
    inp1 = board.get_pin("a:6:i")
    out1 = board.get_pin("d:10:p")
    but1 = board.get_pin("d:2:i")
    but2 = board.get_pin("d:7:i")
    led1 = board.get_pin("d:11:p")

    iterator = pyfirmata.util.Iterator(board)
    iterator.start()
    time.sleep(0.2)

    # endregion

    out1.write(0)
    # Potansiyometreden okunan degerin kaca bolunecegi
    max_v = 30
    # Gonderilecek Ayar 2 (Kamera Toleransi)
    camera_tolerance = frc7839_lib.DbFunctions.read_setting_on_txt(
        "camera_tolerance", file
    )
    # Gonderilecek Ayar 1 (Robot Konumu)
    robot_location = None
    # Gonderme isleminin sonucu
    send_func_msg = None

    key = None

    nt_stat = None

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

    # Ana menuyu yazdir
    # print_menu(stdscr, all_menu_elements[0][0], all_menu_elements[0][1])j
    # endregion

    try:
        socket5802 = frc7839_lib.ServerFunctions.start_server(check_cam_port)
    except:
        print("InputP - ERROR: Server acılamadı.")
        exit()
    else:
        print("InputP - Server acıldı.")
        
    frc7839_lib.ArduinoFunctions.led_write(led1, out1, 1)
    
    while True:
    
        # Ekran yenilenmesi
        cur_stat["all_menu_elements"] = refresh_screen(stdscr, cur_stat, key, nt_stat)

        # Basilan key deger okundu
        key, msg = frc7839_lib.ArduinoFunctions.key_get_with_recv(but1, but2, swt1, pot1, socket5802)
        

        # Imlec hareketleri degiskenlere yazildi
        cur_stat["current_row"] = cursor_handler(key, cur_stat)

        # region Menu degistirme (IP Menusune)

        if (
            key == "button0"
            and cur_stat["current_row"] == 0
            and cur_stat["current_menu"] == main_menu_value
        ):

            cur_stat["current_menu"] = ip_menu_value
            cur_stat["current_row"] = 0

        # endregion
        # region Menu degistirme (Arduino Menusune)

        elif (
            key == "button0"
            and cur_stat["current_row"] == 1
            and cur_stat["current_menu"] == main_menu_value
        ):

            cur_stat["current_menu"] = arduino_menu_value
            cur_stat["current_row"] = 0

        # endregion
        # region Menu degistirme (Kamera Menusune)
        ############

        elif (
            key == "button0"
            and cur_stat["current_row"] == 2
            and cur_stat["current_menu"] == main_menu_value
        ):

            cur_stat["all_menu_elements"][camera_menu_value] = get_cam_menu_values(
                nt_stat
            )

            # nt_stat = cur_stat["all_menu_elements"][camera_menu_value][0][0]

            cur_stat["current_menu"] = camera_menu_value
            cur_stat["current_row"] = 0

        ############
        # endregion

        # region Led Test
        elif (
            key == "button0"
            and cur_stat["current_row"] == 3
            and cur_stat["current_menu"] == main_menu_value
        ):

            frc7839_lib.ArduinoFunctions.led_write(led1, out1, 0)
            time.sleep(1)
            frc7839_lib.ArduinoFunctions.led_write(led1, out1, 1)

        # region Programi kapatmak icin,

        elif (
            key == "button0"
            and cur_stat["current_row"]
            == len(cur_stat["all_menu_elements"][main_menu_value][0]) - 1
            and cur_stat["current_menu"] == main_menu_value
        ):

            exit()

        # endregion

        # region arduino menu ozel
        if cur_stat["current_menu"] == 2:
            if (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 0
            ):
                robot_location = frc7839_lib.ArduinoFunctions.get_robot_location_from_potansiometer_input(
                    key, max_v
                )

            elif (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 1
            ):
                camera_tolerance = key
                camera_tolerance = str(max_v - camera_tolerance)

            # Send tuşu
            if (
                key == "button0"
                and cur_stat["current_row"] == 2
            ):
                if camera_tolerance is not None:
                    frc7839_lib.DbFunctions.save_settings("camera_tolerance", camera_tolerance, file)
                if robot_location is not None:
                    frc7839_lib.DbFunctions.save_settings("robot_location", robot_location, file)
               
                # if waiting_period is not None:
                #     frc7839_lib.DbFunctions.write_setting_to_txt(waiting_period, file)
                
            all_menu_elements[2] = get_arduino_menu_values(
                send_func_msg, robot_location, camera_tolerance
            )

            cur_stat["current_menu_elements"] = all_menu_elements[2][0]
            cur_stat["current_menu_status"] = all_menu_elements[2][1]

        # Eger Arduino menusunden cikilirsa Server tekrar kontrol edilecek
        else:
            send_func_msg = None
        # endregion

        cur_stat["current_menu"], cur_stat["current_row"] = return_to_menu(
            key, cur_stat
        )

        if cur_stat["current_menu"] == 0:
            cur_stat["current_menu_elements"] = all_menu_elements[0][0]
            cur_stat["current_menu_status"] = all_menu_elements[0][1]

        elif cur_stat["current_menu"] == 1:
            cur_stat["current_menu_elements"] = all_menu_elements[1][0]
            cur_stat["current_menu_status"] = all_menu_elements[1][1]

        elif cur_stat["current_menu"] == 2:
            cur_stat["current_menu_elements"] = all_menu_elements[2][0]
            cur_stat["current_menu_status"] = all_menu_elements[2][1]

        elif cur_stat["current_menu"] == 3:
            cur_stat["current_menu_elements"] = all_menu_elements[3][0]
            cur_stat["current_menu_status"] = all_menu_elements[3][1]


curses.wrapper(not_main)

# region def main
# def main():
#     try:
#         curses.wrapper(not_main)
#     except:
#         time.sleep(1)
#         print("An error occured restarting in 5 seconds...")
#         time.sleep(5)
#         main()
#
# if __name__ == "__main__":
#     main()
# endregion
