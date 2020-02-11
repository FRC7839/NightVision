import curses_functions
import pyfirmata
import curses
import socket
import time
import zmq
import os

# Check camera
# Son camera_tolerance değerini kaydetme

global cam_curses_port1
global cam_curses_port2
global check_cam_port

cam_curses_port1 = curses_functions.cam_curses_port1
cam_curses_port2 = curses_functions.cam_curses_port2
check_cam_port = curses_functions.check_cam_port


def saveCamTol(camTol):
    try:
        with open("settings.txt", "w") as writer:
            writer.write(camTol)
    except:
        with open("settings.txt", "w+") as writer:
            writer.write(camTol)


def getCamTol():
    try:
        with open("settings.txt", "r") as reader:
            output = reader.read()
    except:
        saveCamTol(None)

    return output


def sendValuesToCamera(robo_loc, ip_addr_func="127.0.0.1", cam_tol="15"):
    tcp_port = cam_curses_port1
    settings = []
    settings = curses_functions.addSetting("isTest", "True", settings)
    settings = curses_functions.addSetting("robot_location", robo_loc, settings)
    settings = curses_functions.addSetting("camera_tolerance", cam_tol, settings)
    settings = curses_functions.addSetting("ip_address", ip_addr_func, settings)

    status = curses_functions.transmit_settings(settings, tcp_port)
    return status


def check_cam_server(tcp_port=check_cam_port):
    try:
        curses_functions.start_server(tcp_port)
    except:
        isServerStarted = True
    else:
        isServerStarted = False

    return isServerStarted


def is_NetworkTables_init():
    if check_cam_server():
        socket = curses_functions.connect_server(check_cam_server)
        msg_ar = []
        msg = str(socket.recv())
        msg_ar = str(msg).split("#")
        msg = curses_functions.find_setting(msg_ar, "is_network_tables_started")

        if bool(msg):
            return True

        elif not bool(msg):
            return False

        else:
            exit()

    elif not check_cam_server():
        return "SERVER NOT STARTED"

    else:
        return "CANNOT CONNECT TO SERVER"


def check_cam():
    if os.name == "nt":
        return True

    elif os.name == "posix" and socket.gethostname() == "frcvision":
        if os.path.exists("/dev/video0"):
            return True
        else:
            return False


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
        return "Deneme"
    if os.name == "posix":
        ssid = os.popen(
            "iwconfig wlan0 \
                | grep 'ESSID' \
                | awk '{print $4}' \
                | awk -F\\\" '{print $2}'"
        ).read()

        return ssid


def menuOneGetValues():
    ipaddr_func = get_ipaddr()
    check_cam_func = check_cam()
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

    if check_cam_func:
        mainmenu.append("CAMERA CONNECTED")
        mainmenucheck.append(True)
    elif not check_cam_func:
        mainmenu.append("CAMERA NOT CONNECTED")
        mainmenucheck.append(False)

    mainmenu.append("EXIT")
    mainmenucheck.append("Normal")

    return [mainmenu, mainmenucheck]


def menuIpGetValues(ssid_func=get_ssid(), ipaddr_func=get_ipaddr()):
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


def menuArduinoGetValues(send_func_msg=None, robo_loc=None, cam_tol=None):
    mainmenu = []
    mainmenu_status = []

    try:
        if cam_tol is None:
            if getCamTol() == "":
                cam_tol = None

            else:
                cam_tol = getCamTol()
    except:
        pass

    if robo_loc is None:
        mainmenu.append("INPUT FOR ROBOT LOCATION")
        mainmenu_status.append(False)
    else:
        mainmenu.append("ROBOT LOCATION: " + robo_loc)
        mainmenu_status.append("Normal")

    if cam_tol is None:
        mainmenu.append("INPUT FOR CAMERA TOLERANCE")
        mainmenu_status.append(False)
    else:
        mainmenu.append("CAMERA TOLERANCE: " + cam_tol)
        mainmenu_status.append("Normal")

    if send_func_msg is not None:
        mainmenu.append(send_func_msg)
        if send_func_msg != "SENT":
            mainmenu_status.append(False)
        else:
            mainmenu_status.append(True)
    else:
        mainmenu.append("SEND CURRENT SETTINGS")
        mainmenu_status.append("Normal")

    mainmenu.append("OK")
    mainmenu_status.append("Normal"),

    return [mainmenu, mainmenu_status]


def menuCamGetValues(
    isNetworkTableOnline=is_NetworkTables_init(), isCamOnline=check_cam()
):
    mainmenu = []
    mainmenu_status = []

    # ILK ELEMENT (NETWORK TABLES)
    if isNetworkTableOnline == True:
        mainmenu.append("NETWORK TABLES CONNECTED")
        mainmenu_status.append(True)
    elif not isNetworkTableOnline == False:
        mainmenu.append("NETWORK TABLES NOT CONNECTED")
        mainmenu_status.append(False)
    elif isNetworkTableOnline != True or isNetworkTableOnline != False:
        mainmenu.append(str(isNetworkTableOnline))
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

        x = w // 2 - len(row) // 2
        y = h // 2 - len(cur_stat["current_menu_elements"]) // 2 + idx
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


def refresh_screen(stdscr, cur_stat):
    new_all_menu_elements = cur_stat["all_menu_elements"]
    new_all_menu_elements[main_menu_value] = menuOneGetValues()
    new_all_menu_elements[ip_menu_value] = menuIpGetValues(get_ssid(), get_ipaddr())
    new_all_menu_elements[arduino_menu_value] = menuArduinoGetValues()
    new_all_menu_elements[camera_menu_value] = menuCamGetValues(
        is_NetworkTables_init(), check_cam()
    )

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
    all_menu_elements.append(menuOneGetValues())
    all_menu_elements.append(menuIpGetValues())
    all_menu_elements.append(menuArduinoGetValues())
    all_menu_elements.append(menuCamGetValues())
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

    board = curses_functions.import_arduino()

    swt1 = board.get_pin("a:1:i")
    pot1 = board.get_pin("a:2:i")
    inp1 = board.get_pin("a:6:i")
    out1 = board.get_pin("d:10:i")
    but1 = board.get_pin("d:2:i")
    but2 = board.get_pin("d:7:i")
    led1 = board.get_pin("d:11:p")

    iterator = pyfirmata.util.Iterator(board)
    iterator.start()
    time.sleep(0.2)

    # endregion

    # Potansiyometreden okunan degerin kaca bolunecegi
    max_v = 30
    # Gonderilecek Ayar 2 (Kamera Toleransi)
    cam_tol = None
    # Gonderilecek Ayar 1 (Robot Konumu)
    robo_loc = None
    # Gonderme isleminin sonucu
    send_func_msg = None

    global main_menu_value
    global ip_menu_value
    global arduino_menu_value
    global camera_menu_value
    main_menu_value = 0
    ip_menu_value = 1
    arduino_menu_value = 2
    camera_menu_value = 3

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
    # print_menu(stdscr, all_menu_elements[0][0], all_menu_elements[0][1])
    # endregion

    while True:
        # Ekran yenilenmesi
        cur_stat["all_menu_elements"] = refresh_screen(stdscr, cur_stat)

        # Basilan key deger okundu
        key = curses_functions.whichIsChanged(but1, but2, pot1)

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
        elif (
            key == "button0"
            and cur_stat["current_row"] == 2
            and cur_stat["current_menu"] == main_menu_value
        ):
            cur_stat["current_menu"] = camera_menu_value
            cur_stat["current_row"] = 0
        # endregion

        # region Programi kapatmak icin,
        if (
            key == "button0"
            and cur_stat["current_row"] == 3
            and cur_stat["current_menu"] == main_menu_value
        ):
            exit()
        # endregion

        # region arduino menu ozel
        if cur_stat["current_menu"] == 2:
            if key != "button1" and key != "button0" and cur_stat["current_row"] == 0:
                robo_loc = curses_functions.get_robo_loc2(key, max_v)

            elif key != "button1" and key != "button0" and cur_stat["current_row"] == 1:
                cam_tol = key
                cam_tol = str(max_v - cam_tol)

            # Send tuşu
            if (
                key == "button0"
                and cur_stat["current_row"] == 2
                and (not (robo_loc is None))
            ):
                if cam_tol is not None:
                    send_func_msg = sendValuesToCamera(robo_loc, get_ipaddr(), cam_tol)
                    saveCamTol(cam_tol)
                else:
                    send_func_msg = sendValuesToCamera(robo_loc, get_ipaddr())

            all_menu_elements[2] = menuArduinoGetValues(
                send_func_msg, robo_loc, cam_tol
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

