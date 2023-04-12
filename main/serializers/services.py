import re


def is_hex_color(input_string):
    HEX_COLOR_REGEX = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    regexp = re.compile(HEX_COLOR_REGEX)
    if regexp.search(input_string):
        return True
    return False
