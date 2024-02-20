import time
import _thread

from led_strip import LEDStrip
from pattern_manager import PatternManager
from control_interface import ControlInterface, ButtonSignal
from power_manager import PowerManager
from display import Display
# from wifi_manager import WiFiManager

LED_PIN = const(3)
BUTTON_PIN = const(4)
POT_PIN = const(5)
OLED_SCL_PIN = const(6)
OLED_SDA_PIN = const(7)
RELAY_PIN = const(8)
DISPLAY_SCL_PIN = const(9)
DISPLAY_SDA_PIN = const(10)
PATTERNS_FILE = "patterns.json"
WIFI_SSID = "ssid"
WIFI_PASSWORD = "password"

class MainController():
    def __init__(self):
        self.pattern_manager = PatternManager(PATTERNS_FILE)
        led_count, ticks, tick_duration_ms = self.pattern_manager.settings()
        self.led_strip = LEDStrip(LED_PIN, led_count, ticks, tick_duration_ms)
        self.control_interface = ControlInterface(BUTTON_PIN, POT_PIN)
        self.power_manager = PowerManager(RELAY_PIN)
        self.display = Display(DISPLAY_SCL_PIN, DISPLAY_SDA_PIN)
        # self.wifi_manager = WiFiManager(WIFI_SSID, WIFI_PASSWORD)

    def _switch(self):
        if not self.power_manager.status_on():
            self.led_strip.set_dark()
        self.power_manager.power_on()   # fade on
        self.led_strip.set_active()
        self.cuttent_pattern = self.pattern_manager.set_next_pattern()

    def _power_down(self):
        self.led_strip.set_dark()   # fade off
        self.led_strip.set_inactive()
        time.sleep(1)
        self.power_manager.power_off()

    def run(self):
        self.led_tread = _thread.start_new_thread(self.led_strip.update_continuously, ())

        self.current_pattern = self.pattern_manager.current_pattern()
        self.led_strip.update_pattern(self.current_pattern)

        while True:
            for _ in range(10):
                if self.control_interface.update_check():
                    button_signal = self.control_interface.get_changes()
                    if button_signal == ButtonSignal.SHORT_PRESS:
                        self._switch()
                    elif button_signal == ButtonSignal.LONG_PRESS:
                        self._power_down()
                time.sleep_ms(100)
            if False and self.wifi_manager.listen_for_connections(): # INACTIVE
                pass # update pattern


def main():
    main_controller = MainController()
    main_controller.run()

if __name__ == "__main__":
    main()


