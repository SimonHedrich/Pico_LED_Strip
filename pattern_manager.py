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
    def __init__(self, file_path:str):
        self.file_path = file_path
        settings = load_json(file_path)
        self.led_count:int = settings["led_count"]
        self.ticks:int = settings["ticks"]
        self.tick_duration_ms:int = settings["tick_duration_ms"]
        self.patterns_definitions:dict[str, dict] = settings["patterns"]
        self.patterns:dict[str, Pattern] = {
            code: Pattern(self.led_count, self.ticks, self.tick_duration_ms, code, definition)
            for code, definition in self.patterns_definitions.items()}
        self.current_pattern_code:str = list(self.patterns.keys())[0]   # first pattern

    def _update_settings_file(self):
        settings = load_json(self.file_path)
        settings["patterns"] = self.patterns
        write_json(self.file_path, settings)

    def add_pattern(self, pattern_code:str, pattern_definition:dict):
        self.patterns_definitions[pattern_code] = pattern_definition
        self.patterns[pattern_code] = Pattern(
            self.led_count, self.ticks, self.tick_duration_ms, pattern_code, pattern_definition)
        self._update_settings_file()

    def remove_pattern(self, pattern_code:str):
        if self.current_pattern_code == pattern_code:
            self.set_next_pattern()
        self.patterns_definitions.pop(pattern_code)
        self.patterns.pop(pattern_code)
        self._update_settings_file()

    def set_next_pattern(self):
        pattern_codes = list(self.patterns.keys())
        current_index = pattern_codes.index(self.current_pattern_code)
        next_pattern_code = pattern_codes[current_index + 1]
        self.current_pattern_code = next_pattern_code
        return self.current_pattern()

    def set_pattern(self, pattern_code:str):
        self.current_pattern_code = pattern_code

    def current_pattern(self) -> Pattern:
        return self.patterns[self.current_pattern_code]

    def settings(self) -> tuple[int, int, int]:
        return (self.led_count, self.ticks, self.tick_duration_ms)
