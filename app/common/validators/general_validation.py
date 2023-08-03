import re


def string_is_valid_hex_color(hex_color_string):
    return re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_color_string)
