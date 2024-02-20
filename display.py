from machine import Pin, SoftI2C
import ssd1306

class Display:
    def __init__(self, pin_scl, pin_sda, pixel_width=128, pixel_height=32):
        self.i2c = SoftI2C(scl=Pin(6), sda=Pin(7))
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.driver = ssd1306.SSD1306_I2C(self.pixel_width, self.pixel_height, self.i2c)

    def print(self, text):
        self.driver.text(text, 0, 0)
        self.driver.show()

        # self.driver.text('Hello, W0rld 123', 0, 0) # max lenth
        # self.driver.text('Hello, World 2!', 0, 10)
        # self.driver.text('Hello, World 3!', 0, 20)
        # self.driver.show()