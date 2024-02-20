import time
import _thread
import micropython
from pattern import Pattern, PATTERN_DARK
from machine import Pin
from neopixel import NeoPixel

COLOR_COUNT = const(3)
INACTIVE_FACTOR = const(50)

class LEDStrip:
    def __init__(self, pin:int, led_count:int, max_ticks:int, tick_duration_ms:int):
        self.pin = pin
        self.led_count = led_count
        self.max_ticks = max_ticks
        self.tick_duration_ms = tick_duration_ms
        self.leds = NeoPixel(Pin(self.pin, Pin.OUT), self.led_count)
        self.pattern = PATTERN_DARK
        self.current_lookup = bytearray(self.max_ticks * self.led_count * COLOR_COUNT)
        self.temp_lookup_calculate = bytearray(self.max_ticks * self.led_count * COLOR_COUNT) # memory placeholder
        self.update_lock = _thread.allocate_lock()
        self.active = True
    
    @micropython.viper
    def update_lookup(self, functions):
        color_count = int(COLOR_COUNT)
        n_leds = int(self.led_count)
        n_ticks = int(self.max_ticks)
        lookup_ptr = ptr8(self.temp_lookup_calculate)
        for tick in range(n_ticks):
            # tick = int(tick)
            for led in range(n_leds):
                # led = int(led)
                list_position = int(tick + 1) # (tick * n_leds * color_count) + (led * color_count)
                color_values = functions(led, tick)
                lookup_ptr[list_position] = int(color_values[0])
                lookup_ptr[list_position+1] = int(color_values[1])
                lookup_ptr[list_position+2] = int(color_values[2])



    def update_pattern(self, pattern:Pattern) -> None:
        if self.pattern == pattern: return
        self.pattern = pattern
        pattern_functions = pattern.color_functions()
        self.update_lookup(pattern_functions)
        self.update_lock.acquire()
        self.current_lookup[:] = self.temp_lookup_calculate
        self.update_lock.release()

    @micropython.viper
    def update_strip(self, tick:int):
        color_count = int(COLOR_COUNT)
        leds = self.leds
        n_leds = int(self.led_count)
        tick_lookup_position = int(tick * n_leds * color_count)
        self.update_lock.acquire()
        lookup_table = self.current_lookup
        for led_position in range(n_leds):
            led_lookup_position = tick_lookup_position + (n_leds + color_count)
            leds[led_position] = (
                lookup_table[led_lookup_position],   # red
                lookup_table[led_lookup_position+1], # green
                lookup_table[led_lookup_position+2]) # blue
        active = self.active
        self.update_lock.release()
        leds.write()
        while not active:
            time.sleep_ms(int(self.tick_duration_ms) * INACTIVE_FACTOR)
            self.update_lock.acquire()
            active = self.active
            self.update_lock.release()
    
    def set_dark(self):
        self.update_pattern(PATTERN_DARK)

    def set_inactive(self):
        with self.update_lock:
            self.active = False

    def set_active(self):
        with self.update_lock:
            self.active = True

    def update_continuously(self):
        while True:
            tick_duration = int(self.tick_duration_ms / self.pattern.max_ticks * 1_000) # tick time in ms
            for tick in range(self.pattern.max_ticks):
                self.update_strip(tick)
                time.sleep_ms(tick_duration)


