import _thread
from machine import Pin
from neopixel import NeoPixel


class LEDStrip:
    def __init__(self, pin:int, led_count:int):
        self.pin = pin
        self.led_count = led_count
        self.leds = NeoPixel(Pin(self.pin, Pin.OUT), self.led_count)
        self.pattern = None
        self.update_lock = _thread.allocate_lock()
    
    def update_pattern(self, pattern):
        with self.update_lock:
            self.pattern = pattern

    def update_strip(self, time_step):
        # Update each LED based on the current pattern and time step
        if not self.pattern:
            print("No pattern set!")
            return
        with self.update_lock:
            for led_position in range(self.led_count):
                red, green, blue = self.pattern.calculate_color(led_position, time_step)
                self.leds[led_position] = (red, green, blue)
            self.leds.write()
