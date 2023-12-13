import socket
import _thread
import machine
import time
import sys
from machine import Pin
from setup import net
from setup.display import Display
from config import *

def initialize_hardware():
    """
    Initializes OLED display and GPIO pins.
    """
    oled_display = Display()
    on_board_led = Pin(ON_BOARD_LED_GPIO, Pin.OUT)
    relay_pin = Pin(RELAY_OUT_GPIO, Pin.OUT)
    signal_led_1 = Pin(SIGNAL_LED_1_GPIO, Pin.OUT)
    signal_led_2 = Pin(SIGNAL_LED_2_GPIO, Pin.OUT)

    oled_display.shutter_display(
        ["Mentioner!", "Starting.", "Starting..", "Starting.", "Connecting to Wifi"],
        "center",
        1,
    )
    
    return oled_display, on_board_led, relay_pin, signal_led_1, signal_led_2


def connect_to_wifi():
    """
    Connects to Wi-Fi and displays connection status.
    """
    network_manager = net.NetworkManager(ssid=WIFI_NAME, password=WIFI_PASS)
    
    oled_display.shutter_display(
        [
            f"Connected with {network_manager.get_connection_name()}",
            "Starting socket.",
            "Starting socket...",
            "Starting socket.",
        ],
        "center",
        1,
    )
    
    return network_manager


def create_server_socket(network_manager):
    """
    Creates and binds the server socket.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (network_manager.get_device_ip(), 80)
    server_socket.bind(server_address)
    
    return server_socket


def blink(pin, duration: float):
    """
    Blinks the specified GPIO pin for the given duration.

    Args:
        pin: GPIO Pin.
        duration (float): Duration in seconds.
    """
    pin.value(1)
    time.sleep(duration)
    pin.value(0)


def handle_client(connection, client_address, oled_display, signal_led_1, relay_pin, signal_led_2):
    """
    Handles client connections.

    Args:
        connection: Client connection socket.
        client_address: Client address.
        oled_display: Display instance.
        signal_led_1: Signal LED 1 pin.
        relay_pin: Relay pin.
        signal_led_2: Signal LED 2 pin.
    """
    message_data = {}
    mentions = {}
    
    oled_display.display_center(f"Connected with {client_address[0]}")
    signal_led_1.value(1)
    y_position = 0
    
    while True:
        message_length = connection.recv(HEADER).decode(FORMAT)
        if message_length:
            if len(mentions) == 0:
                oled_display.clear_display()
            
            message_text = connection.recv(int(message_length)).decode(FORMAT)
            message = message_text.split()
            
            # TODO: Scroll feature
            if len(mentions) > 8:
                print("Mention limit reached")
                sys.exit()
            
            blink(relay_pin, 1)
            blink(signal_led_2, 1)
            
            if message[0] not in mentions.keys():
                mentions.update({message[0]: [1, y_position]})
                y_position += 8
            else:
                mentions.update(
                    {message[0]: [mentions[message[0]][0] + 1, mentions[message[0]][1]]}
                )
            
            formatted_message = f"{mentions[message[0]][0]}*{message[1]} {message[2]}"
            
            if message[0] not in mentions.keys():
                message_data[y_position] = formatted_message
            else:
                message_data[mentions[message[0]][1]] = formatted_message
            
            oled_display.clear_display()
            
            for position in message_data:
                oled_display.display(message_data[position], 0, position, erase=False)


def start_server(server_socket, oled_display, on_board_led):
    """
    Starts the server to listen for incoming client connections.

    Args:
        server_socket: Server socket.
        oled_display: Display instance.
        on_board_led: On-board LED pin.
    """
    server_socket.listen(1)
    
    while True:
        client_connection, client_address = server_socket.accept()
        _thread.start_new_thread(
            handle_client, (client_connection, client_address, oled_display, signal_led_1, relay_pin, signal_led_2)
        )


def main():
    oled_display, on_board_led, relay_pin, signal_led_1, signal_led_2 = initialize_hardware()
    network_manager = connect_to_wifi()
    server_socket = create_server_socket(network_manager)

    # Blink the on-board LED to indicate server start
    blink(on_board_led, 1)

    # Start the server
    print("Server starting on ", server_address)
    oled_display.shutter_display(["Socket Initialized", "Listening."], "center", 2)
    
    start_server(server_socket, oled_display, on_board_led)


# Execute the main function
if __name__ == "__main__":
    main()
