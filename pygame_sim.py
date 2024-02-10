import pygame
import sys
import json
import time
from math import radians, sin, pi

def get_patterns():
    with open("patterns.json", 'r') as file:
        json_content = json.load(file)
    led_count = json_content["led_count"]
    ticks = json_content["ticks"]
    patterns = json_content["patterns"]
    return led_count, ticks, patterns


def get_color(
        red_formula, 
        green_formula, 
        blue_formula, 
        led_position, 
        tick_count
    ):
    expressions = {
        'i': led_position, 
        't': tick_count,
        'sin': sin,
        'pi': pi
        }
    color = (
        int(eval(red_formula, {'__builtins__': None}, expressions)),
        int(eval(green_formula, {'__builtins__': None}, expressions)),
        int(eval(blue_formula, {'__builtins__': None}, expressions))
        )
    return color


def main():
    led_count, ticks, patterns = get_patterns()

    pygame.init()

    # Window dimensions
    num_squares = led_count  # Total number of squares
    window_width = 1400  # Calculate the total window width
    square_size = int(window_width / num_squares)  # Size of each square
    window_height = square_size  # Only one row of squares
    screen = pygame.display.set_mode((window_width, window_height))

    pattern = patterns["rainbow"]
    name = pattern["name"]
    duration = pattern["duration"]
    red = pattern["red"]
    blue = pattern["blue"]
    green = pattern["green"]

    tick_duration = duration / ticks
    loop_start = time.time()
    tick_start = time.time()
    # Main loop
    tick_count = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for i in range(led_count):
            color = get_color(red, green, blue, i, tick_count)
            pygame.draw.rect(screen, color, (i*square_size, 0, square_size, square_size))

        pygame.display.flip()


        if tick_count >= ticks: 
            tick_count = 1
            print(time.time() - loop_start)
            loop_start = time.time()
        else: 
            tick_count += 1

        elapsed_time = time.time() - tick_start 
        time_to_sleep = max(tick_duration - elapsed_time, 0)
        time.sleep(time_to_sleep)
        tick_start = time.time()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()