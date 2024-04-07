# Esp32-Discord-Notifier

Script to get mentions using discord api and transfering packets locally via socket to the module and display on the oled and beep the buzzer

client.py  -> will be run on the computer

Steps :
1) provide the wifi credentials on the config.py file and change the gpio pins accordingly 
2) run the client.py with the token
3) start the esp32 with the code provided 



External libs used: (in the esp module)
1. ssd1306 

