import math

def calculate_bounding_box(left, right, bottom, top, rotation):
    '''
    Return bounding box of a rotated box
    The rotation must be in radians
    '''
    rotation = abs(rotation)
    width = right - left
    height = top - bottom

    b_width = (math.sin(rotation) * height) + (math.cos(rotation) * width)
    b_height = (math.sin(rotation) * width) + (math.cos(rotation) * height)

    diff_x = (b_width - width) / 2
    b_left = left - diff_x
    b_right = right + diff_x

    diff_y = (b_height - height) / 2
    b_bottom = bottom - diff_y
    b_top = top + diff_y

    return b_left, b_right, b_bottom, b_top