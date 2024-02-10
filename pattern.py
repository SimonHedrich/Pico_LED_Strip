from math import sin, cos, pi

class Pattern:
    def __init__(self, name, code, duration, red_expr, green_expr, blue_expr):
        self._name = name
        self._code = code
        self._duration = duration
        self._red_expr = red_expr
        self._green_expr = green_expr
        self._blue_expr = blue_expr
    
    def calculate_color(self, led_position, tick_count):
        expressions = {
            'i': led_position, 
            't': tick_count,
            'sin': sin,
            'cos': cos,
            'pi': pi
            }
        color = (
            int(eval(self._red_expr, {'__builtins__': None}, expressions)),
            int(eval(self._green_expr, {'__builtins__': None}, expressions)),
            int(eval(self._blue_expr, {'__builtins__': None}, expressions))
            )
        return color
