from config import *
import ssd1306
from machine import SoftI2C, Pin
import time

class Display():
    
    def __init__(self) -> None:
        pins = SoftI2C(scl=Pin(DISPLAY_SCL_GPIO), sda=Pin(DISPLAY_SDA_GPIO))
        oled = ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, pins)
        self.oled = oled

    @staticmethod
    def split_string(input: str, breakpoint: int) -> list:
        words = input.split()
        final = []
        for word in words:
            if len(word) > breakpoint:
                for i in range(0, len(word), breakpoint):
                    final.append(word[i:i+breakpoint])
            else:
                final.append(word)

        return final

    def display(self,msg : str, x: int = 0, y: int = 0, *, erase: bool = True) -> None:
        if erase: self.oled.fill(0)
        if len(msg) > 16 and x == 0:
            abc = self.split_string(msg,16)
            y-=8
            for ms in abc:
             if y < DISPLAY_HEIGHT:
                self.oled.text(ms,x,y)
                self.oled.show()
                y+=8
             else:
                 self.display_center('Out of space')
                 break
            return
                 
        self.oled.text(msg,x,y)
        self.oled.show()

    def display_center(self,text : str ,*, erase = True) -> None:
        if erase : self.oled.fill(0)
        self.display(text,0,25)

    def shutter_display(self, arg: list ,position : ['center','default'], delay : int = 0) -> None:
        if position == 'center': 
            [self.display_center(x) for x in arg if time.sleep(delay) is None] 
        elif position[0] == 'default':
            [self.display(x) for x in arg if time.sleep(delay) is None]
    
    def clear_display(self) -> None:
        self.oled.fill(0)

        
