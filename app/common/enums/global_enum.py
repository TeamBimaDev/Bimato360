<<<<<<< HEAD
def get_enum_value(enum_class, input_str):
    if not isinstance(input_str, str):
        return None
    for item in enum_class:
        if input_str.lower() in [item.name.lower(), str(item.value).lower()]:
            return item.name
    return None

=======
def get_enum_value(enum_class, input_str):
    if not isinstance(input_str, str):
        return None
    for item in enum_class:
        if input_str.lower() in [item.name.lower(), str(item.value).lower()]:
            return item.name
    return None

>>>>>>> origin/ma-branch
