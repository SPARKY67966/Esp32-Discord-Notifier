from config import *
import ssd1306
from machine import SoftI2C, Pin
import time

class Display:
    
    def __init__(self) -> None:
        # Initialize I2C pins for the OLED display
        i2c_pins = SoftI2C(scl=Pin(DISPLAY_SCL_GPIO), sda=Pin(DISPLAY_SDA_GPIO))
        # Create an OLED display instance
        self.oled = ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c_pins)

    def split_string(input_text: str, breakpoint: int) -> list:
        # Split input text into words
        words = input_text.split()
        split_result = []
        for word in words:
            if len(word) > breakpoint:
                # Split long words into segments
                split_result.extend([word[i:i+breakpoint] for i in range(0, len(word), breakpoint)])
            else:
                split_result.append(word)

        return split_result

    def display_message(self, message: str, x_position: int = 0, y_position: int = 0, *, erase: bool = True) -> None:
        # Display a message on the OLED display
        if erase:
            self.oled.fill(0)
        
        if len(message) > 16 and x_position == 0:
            # Split and display long messages
            split_messages = self.split_string(message, 16)
            y_position -= 8
            for msg_segment in split_messages:
                if y_position < DISPLAY_HEIGHT:
                    self.oled.text(msg_segment, x_position, y_position)
                    self.oled.show()
                    y_position += 8
                else:
                    # If out of space, display a warning
                    self.display_centered_message('Out of space')
                    break
            return
        
        self.oled.text(message, x_position, y_position)
        self.oled.show()

    def display_centered_message(self, message: str, *, erase=True) -> None:
        # Display a message at the center of the OLED display
        self.display_message(message, 0, 25, erase=erase)

    def display_messages(self, messages: list, position: ['center', 'default'], delay: int = 0) -> None:
        # Display a list of messages with optional delay
        display_function = self.display_centered_message if position == 'center' else self.display_message
        [display_function(msg, erase=True) for msg in messages if time.sleep(delay) is None]

    def clear_display(self) -> None:
        # Clear the OLED display
        self.oled.fill(0)
