import math

def calculate_bounding_box(left, right, bottom, top, rotation):
    '''Return bounding box of a rotated box'''
    rotation = abs(rotation)
    width = right - left
    height = top - bottom
    
    rot_width = (math.sin(rotation) * height) + (math.cos(rotation) * width)
    rot_height = (math.sin(rotation) * width) + (math.cos(rotation) * height)
    
    diff_x = (rot_width - width) / 2
    rot_left = left - diff_x
    rot_right = right + diff_x
    
    diff_y = (rot_height - height) / 2
    rot_bottom = bottom - diff_y
    rot_top = top + diff_y
    
    return rot_left, rot_right, rot_bottom, rot_top
