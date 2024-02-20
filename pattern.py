
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
    def __init__(self, leds:int, ticks:int, tick_durartion_ms:int, code:str, definition:dict):
        self.leds = leds
        self.max_ticks = ticks
        self.tick_duration_ms = tick_durartion_ms
        self.code = code
        self.name:str = definition["name"]
        self._red = ColorParameters(**definition["red"])
        self._green = ColorParameters(**definition["green"])
        self._blue = ColorParameters(**definition["blue"])
        self._colors = (self._red, self._green, self._blue)
    
    def calculate_color(self, led, tick):
        color = tuple(
            int((sin(led + tick) + 1) / 2 * color.amplitude + color.offset)
            for color in self._colors)
        return color

    def color_functions(self):
        amplitude_r = int(self._red.amplitude / 2)
        amplitude_g = int(self._green.amplitude / 2)
        amplitude_b = int(self._blue.amplitude / 2)
        offset_r = self._red.offset
        offset_g = self._green.offset
        offset_b = self._blue.offset

        def calculate_color(led:int, tick:int) -> list[int]:
            colors = [
                ((int(sin(led + tick)) + 1) * amplitude_r + offset_r),
                ((int(sin(led + tick)) + 1) * amplitude_g + offset_g),
                ((int(sin(led + tick)) + 1) * amplitude_b + offset_b),
                ]
            return colors
        return calculate_color



WHITE100_DEFINITION = {
    "name": "White 100",
    "red": {
        "amplitude": 0,
        "offset": 100
    },
    "blue": {
        "amplitude": 0,
        "offset": 100
    },
    "green": {
        "amplitude": 0,
        "offset": 100
    }
}

PATTERN_WHITE100 = Pattern(100, 1, 1000, "white100", WHITE100_DEFINITION)


DARK_DEFINITION = {
    "name": "Dark",
    "red": {
        "amplitude": 0,
        "offset": 0
    },
    "blue": {
        "amplitude": 0,
        "offset": 0
    },
    "green": {
        "amplitude": 0,
        "offset": 0
    }
}

PATTERN_DARK = Pattern(100, 1, 1000, "dark", DARK_DEFINITION)
