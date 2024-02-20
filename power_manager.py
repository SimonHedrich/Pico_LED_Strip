from machine import Pin


class PowerManager:
    def __init__(self, relay_pin):
        self._relay_pin = relay_pin
        self._relay = Pin(self._relay_pin, Pin.OUT)
        self._relay_on = False
    
    def power_on(self):
        self._relay_on = True
        self._relay.on()
    
    def power_off(self):
        self._relay_on = False
        self._relay.off()

    def status_on(self):
        return self._relay_on
