import socket
from setup import net
from machine import Pin, SoftI2C
import _thread
from config import *
import machine
import time
import sys
from setup.display import Display

# Setting up oled
# 16 characters max width
# min y axis space 8
# max 8 lines y axis
oled = Display()

LED = machine.Pin(ON_BOARD_LED_GPIO, machine.Pin.OUT)
RELAY = machine.Pin(RELAY_OUT_GPIO, machine.Pin.OUT)
LED1 = machine.Pin(SIGNAL_LED_1_GPIO, machine.Pin.OUT)
LED2 = machine.Pin(SIGNAL_LED_2_GPIO, machine.Pin.OUT)

oled.shutter_display(
    ["Mentioner!", "Starting.", "Starting..", "Starting.", "Connecting to Wifi"],
    "center",
    1,
)

nets = net.net(ssid=WIFI_NAME, password=WIFI_PASS)

oled.shutter_display(
    [
        f"Connected with {nets.connection_name()}",
        "Starting socket.",
        "Starting socket...",
        "Starting socket.",
    ],
    "center",
    1,
)

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = (nets.deviceip(), 80)

soc.bind(addr)


def blink(pin, sec: float):
    pin.value(1)
    time.sleep(sec)
    pin.value(0)


blink(LED, 1)


def handle_client(conn, addr):
    data = {}
    mentions = {}
    oled.display_center(f"Connected with {addr[0]}")
    LED1.value(1)
    y = 0
    while True:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            if len(mentions) == 0:
                oled.clear_display()
            msgg = conn.recv(int(msg_len)).decode(FORMAT)
            msg = msgg.split()
            # TODO : Scroll feature
            if len(mentions) > 8:
                print("Mention limit reached")
                sys.exit()
            blink(RELAY, 1)
            blink(LED2, 1)
            if msg[0] not in mentions.keys():
                mentions.update({msg[0]: [1, y]})
                y += 8
            else:
                mentions.update(
                    {msg[0]: [mentions[msg[0]][0] + 1, mentions[msg[0]][1]]}
                )
            msge = f"{mentions[msg[0]][0]}*{msg[1]} {msg[2]}"
            if msg[0] not in mentions.keys():
                data[y] = msge
            else:
                data[mentions[msg[0]][1]] = msge
            oled.clear_display()
            for x in data:
                oled.display(data[x], 0, x, erase=False)


def start():
    soc.listen(1)
    while True:
        con, addr = soc.accept()
        _thread.start_new_thread(handle_client, (con, addr))


print("Server starting on ", addr)
blink(LED, 1)
oled.shutter_display(["Socket Initialized", "Listening."], "center", 2)
start()
