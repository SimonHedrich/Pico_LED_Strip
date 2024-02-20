import time
import _thread
from machine import Pin

class ButtonSignal:
    NO_PRESS = 0
    SHORT_PRESS = 1
    LONG_PRESS = 2

PRESS_TOLERANCE = 50 # in ms

class ControlInterface:
    def __init__(self, button_pin:int, pot_pin:int, long_press_duration_ms:int=3000):
        self.button_pin = button_pin
        self.button = Pin(self.button_pin, Pin.IN, Pin.PULL_UP)
        self.button.irq(self.button_pressed, Pin.IRQ_RISING)
        self.button.irq(self.button_released, Pin.IRQ_FALLING)
        self.button_lock = _thread.allocate_lock()
        self.long_press_duration_ms = long_press_duration_ms
        self.last_press = time.ticks_ms()
        self.last_release = time.ticks_ms()
        self.last_button_signal = ButtonSignal.NO_PRESS

        self.pot_pin = pot_pin
        self.pot_lock = _thread.allocate_lock()
    
    def button_pressed(self):
        with self.button_lock:
            self.last_press = time.ticks_ms()

    def button_released(self):
        with self.button_lock:
            self.last_release = time.ticks_ms()
            press_duration = time.ticks_diff(self.last_release, self.last_press)
            if press_duration < PRESS_TOLERANCE: 
                self.last_button_signal = ButtonSignal.NO_PRESS
            elif press_duration < self.long_press_duration_ms:
                self.last_button_signal = ButtonSignal.SHORT_PRESS
            else:
                self.last_button_signal = ButtonSignal.LONG_PRESS

    def update_check(self) -> bool:
        return not self.last_button_signal

    def get_changes(self):
        changes = {"button": self.last_button_signal}
        self.last_button_signal = ButtonSignal.NO_PRESS
        return changes
