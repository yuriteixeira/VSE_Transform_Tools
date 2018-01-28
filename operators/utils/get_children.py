def get_children(strip, select=False):
    """
    Recursively ensure all input_1 and input_2 strips are selected
    """
    if select:
        strip.select = True
    checked_strips = [strip]

    if hasattr(strip, 'input_1'):
        checked_strips.extend(get_children(strip.input_1, select))
    if hasattr(strip, 'input_2'):
        checked_strips.extend(get_children(strip.input_2, select))

    return checked_strips
