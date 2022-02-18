import math

import bpy


def get_strip_box(strip):
    """
    Gets the box of a non-transform strip

    Args
        :strip: A strip from the vse (bpy.types.Sequence)
    Returns
        :box: A list comprising the strip's left, right, bottom, top
              (list of int)
    """
    scene = bpy.context.scene

    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y

    proxy_facs = {
        'NONE': 1.0,
        'SCENE': 1.0,
        'FULL': 1.0,
        'PROXY_100': 1.0,
        'PROXY_75': 0.75,
        'PROXY_50': 0.5,
        'PROXY_25': 0.25
    }

    if not hasattr(strip, 'elements'):
        len_crop_x = res_x
        len_crop_y = res_y

        if strip.type == "SCENE":
            factor = strip.scene.render.resolution_percentage / 100
            len_crop_x = strip.scene.render.resolution_x * factor
            len_crop_y = strip.scene.render.resolution_y * factor

        len_crop_x -= (strip.crop.min_x + strip.crop.max_x)
        len_crop_y -= (strip.crop.min_y + strip.crop.max_y)

        if len_crop_x < 0:
            len_crop_x = 0
        if len_crop_y < 0:
            len_crop_y = 0

        left = strip.transform.offset_x
        right = left + len_crop_x
        bottom = strip.transform.offset_y
        top = strip.transform.offset_y + len_crop_y
    else:
        distance_right = (strip.elements[0].orig_width / 2 - strip.crop.max_x) * strip.transform.scale_x
        distance_left = (strip.elements[0].orig_width / 2 - strip.crop.min_x) * strip.transform.scale_x
        distance_top = (strip.elements[0].orig_height / 2 - strip.crop.max_y) * strip.transform.scale_y
        distance_bottom = (strip.elements[0].orig_height / 2 - strip.crop.min_y) * strip.transform.scale_y

        cos_angle = math.cos(strip.transform.rotation)
        sin_angle = math.sin(strip.transform.rotation)

        all_x = [distance_right * cos_angle - distance_top * sin_angle,
                 distance_right * cos_angle + distance_bottom * sin_angle,
                 - distance_left * cos_angle - distance_top * sin_angle,
                 - distance_left * cos_angle + distance_bottom * sin_angle]
        all_y = [distance_right * sin_angle + distance_top * cos_angle,
                 - distance_left * sin_angle + distance_top * cos_angle,
                 distance_right * sin_angle - distance_bottom * cos_angle,
                 - distance_left * sin_angle - distance_bottom * cos_angle]

        right = max(all_x) + res_x / 2 + strip.transform.offset_x
        left = min(all_x) + res_x / 2 + strip.transform.offset_x

        top = max(all_y) + res_y / 2 + strip.transform.offset_y
        bottom = min(all_y) + res_y / 2 + strip.transform.offset_y

    box = [left, right, bottom, top]

    return box
