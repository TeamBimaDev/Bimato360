def get_enum_value(enum_class, input_str):
    for item in enum_class:
        if input_str.lower() in [item.name.lower(), item.value.lower()]:
            return item.name
    return None
