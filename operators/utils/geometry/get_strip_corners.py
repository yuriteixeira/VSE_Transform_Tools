import bpy
import math
from mathutils import Vector

from .get_strip_box import get_strip_box
from .get_transform_box import get_transform_box
from .rotate_point import rotate_point


def get_strip_corners(strip):
    """
    Get the bottom_left, top_left, top_right, bottom_right corners of a
    strip.

    Args
        :strip: A strip (bpy.types.Sequence)
    Returns
        :corners: The positions of the bottom-left, top-left, top-right,
                  & bottom-right corners (list of mathutils.Vectors)
    """
    scene = bpy.context.scene
    if strip.type == 'TRANSFORM':
        box = get_transform_box(strip)
        left, right, bottom, top = box

        width = right - left
        height = top - bottom

        origin = Vector([left + (width / 2), bottom + (height / 2)])

        off_x = strip.input_1.transform.offset_x
        off_y = strip.input_1.transform.offset_y
        scl_x = strip.scale_start_x
        scl_y = strip.scale_start_y

        origin_x = (width / 2) - (off_x * scl_x) / 2
        origin_y = (height / 2) - (off_y * scl_y) / 2

        origin = Vector([left + origin_x, bottom + origin_y])

        rot = math.radians(strip.rotation_start)
        # if strip.use_translation or strip.use_crop:
        #     rot = 0

        bottom_left = Vector([left, bottom])
        top_left = Vector([left, top])
        top_right = Vector([right, top])
        bottom_right = Vector([right, bottom])

    else:

        scene = bpy.context.scene
        res_x = scene.render.resolution_x
        res_y = scene.render.resolution_y

        try:
            orig_width = strip.elements[0].orig_width
            orig_height = strip.elements[0].orig_height
        except AttributeError:
            # For instance, for text strips, which don't have attached sequence to get their intrinsic size
            orig_width = res_x
            orig_height = res_y

        # distances from the anchor point
        distance_right = (orig_width / 2 - strip.crop.max_x) * strip.transform.scale_x
        distance_left = (orig_width / 2 - strip.crop.min_x) * strip.transform.scale_x
        distance_top = (orig_height / 2 - strip.crop.max_y) * strip.transform.scale_y
        distance_bottom = (orig_height / 2 - strip.crop.min_y) * strip.transform.scale_y

        origin = Vector([res_x / 2 + strip.transform.offset_x, res_y / 2 + strip.transform.offset_y])

        bottom_left = Vector([-distance_left, -distance_bottom]) + origin
        top_left = Vector([-distance_left, distance_top]) + origin
        top_right = Vector([distance_right, distance_top]) + origin
        bottom_right = Vector([distance_right, -distance_bottom]) + origin

        rot = strip.transform.rotation

    corners = [bottom_left, top_left, top_right, bottom_right]
    for i in range(len(corners)):
        corners[i] = rotate_point(corners[i], rot, origin)

    bottom_left, top_left, top_right, bottom_right = corners

    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y

    corners = [bottom_left, top_left, top_right, bottom_right]

    if strip.use_flip_x:
        for i in range(len(corners)):
            corners[i].x = res_x - corners[i].x

    if strip.use_flip_y:
        for i in range(len(corners)):
            corners[i].y = res_y - corners[i].y

    bottom_left, top_left, top_right, bottom_right = corners

    return [bottom_left, top_left, top_right, bottom_right]
