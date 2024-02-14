from math import sin, cos, pi

class ColorParameters:
    __slots__ = [
        'frequency', 
        'phase_shift', 
        'amplitude', 
        'offset', 
        'time_multiplier', 
        'spatial_multiplier']

    def __init__(
            self, 
            frequency=1, 
            phase_shift=0, 
            amplitude=255, 
            offset=0, 
            time_multiplier=1, 
            spatial_multiplier=1,
            **_,
        ):
        self.frequency = frequency
        self.phase_shift = phase_shift
        self.amplitude = amplitude
        self.offset = offset
        self.time_multiplier = time_multiplier
        self.spatial_multiplier = spatial_multiplier

class Pattern:
    def __init__(self, leds, ticks, code, definition):
        self._leds = leds
        self._max_ticks = ticks
        self._code = code
        self._name = definition["name"]
        self._duration = definition["duration"]
        self._red = ColorParameters(**definition["red"])
        self._green = ColorParameters(**definition["green"])
        self._blue = ColorParameters(**definition["blue"])
        self._colors = (self._red, self._green, self._blue)
    
    def calculate_color(self, led_position, tick_count):
        color = tuple(
            int((sin(led_position + tick_count) + 1) / 2 * color.amplitude + color.offset)
            for color in self._colors)
        return color

