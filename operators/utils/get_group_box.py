import bpy
import math
from operator import attrgetter

from .get_nontransformed_strips import get_nontransformed_strips
from .get_transform_strips import get_transform_strips

from .get_strip_box import get_strip_box
from .get_transform_box import get_transform_box

from .get_strip_corners import get_strip_corners

def get_group_box(strips):
    '''
    Get the left-most, right-most, bottom-most, top-most edges of a
    group of strips
    '''
    scene = bpy.context.scene
    boxes = []

    nontransformed = get_nontransformed_strips(strips)

    for strip in nontransformed:
        boxes.append(get_strip_box(strip))

    transformed = get_transform_strips(strips)

    for strip in transformed:
        bl, tl, tr, br = get_strip_corners(strip)
        vectors = [bl, tl, tr, br]
        left = min(vectors, key=attrgetter('x')).x
        right = max(vectors, key=attrgetter('x')).x

        bottom = min(vectors, key=attrgetter('y')).y
        top = max(vectors, key=attrgetter('y')).y
        boxes.append([left, right, bottom, top])

    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y

    min_left = res_x
    max_right = 0
    min_bottom = res_y
    max_top = 0

    for box in boxes:
        if box[0] < min_left:
            min_left = box[0]
        if box[1] > max_right:
            max_right = box[1]
        if box[2] < min_bottom:
            min_bottom = box[2]
        if box[3] > max_top:
            max_top = box[3]

    return min_left, max_right, min_bottom, max_top
