import json
from pattern import Pattern


def load_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        file_content = json.load(file)
    return file_content

def write_json(file_path, content):
    with open(file_path, 'w') as file:
        json.dump(content, file)


class PatternManager:
    def __init__(self, file_path):
        self.file_path = file_path
        settings = load_json(file_path)
        self.led_count = settings["led_count"]
        self.ticks = settings["ticks"]
        self.patterns_definitions = settings["patterns"]
        self.patterns = {
            code: Pattern(self.led_count, self.ticks, code, definition)
            for code, definition in self.patterns_definitions.items()}
        self.current_pattern_code = self.patterns[list(self.patterns.keys())[0]]   # first pattern

    def _update_settings_file(self):
        settings = load_json(self.file_path)
        settings["patterns"] = self.patterns
        write_json(self.file_path, settings)

    def add_pattern(self, pattern_code, pattern_definition):
        self.patterns_definitions[pattern_code] = pattern_definition
        self.patterns[pattern_code] = Pattern(
            self.led_count, self.ticks, pattern_code, pattern_definition)
        self._update_settings_file()

    def remove_pattern(self, pattern_code):
        if self.current_pattern_code == pattern_code:
            self.set_next_pattern()
        self.patterns_definitions.pop(pattern_code)
        self.patterns.pop(pattern_code)
        self._update_settings_file()

    def set_next_pattern(self):
        pattern_codes = list(self.patterns.keys())
        current_index = pattern_codes.index(self.current_pattern_code)
        next_pattern_code = pattern_codes[current_index + 1]
        self.current_pattern_code = self.patterns[next_pattern_code]

    def set_pattern(self, pattern_code):
        self.current_pattern_code = pattern_code

    def current_pattern(self):
        return self.patterns[self.current_pattern_code]

    def settings(self):
        return (self.led_count, self.ticks)
