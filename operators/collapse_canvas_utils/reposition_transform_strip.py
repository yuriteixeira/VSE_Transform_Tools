import math

from .get_transform_box import get_transform_box
from .get_strip_box import get_strip_box
from .calculate_bounding_box import calculate_bounding_box


def reposition_transform_strip(scene, strip, group_box):
    """Reposition a transform strip"""
    min_left, max_right, min_bottom, max_top = group_box

    total_width = max_right - min_left
    total_height = max_top - min_bottom

    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y

    scale_ratio_x = res_x / total_width
    scale_ratio_y = res_y / total_height
    min_left, max_right, min_bottom, max_top = group_box

    left, right, bottom, top = get_transform_box(scene, strip)

    width = right - left
    height = top - bottom
    rot = math.radians(strip.rotation_start)

    bbox = calculate_bounding_box(
        left, right, bottom, top, rot)
    bb_left = bbox[0]
    bb_right = bbox[1]
    bb_bottom = bbox[2]
    bb_top = bbox[3]

    primary_offset_x = bb_left - min_left
    primary_offset_y = bb_bottom - min_bottom

    bb_width = bb_right - bb_left
    bb_height = bb_top - bb_bottom
    
    # After resizing scene resolution, video size is altered
    current_width = width / scale_ratio_x
    current_height = height / scale_ratio_y
    current_left = (left / res_x) * total_width
    current_right = current_left + current_width
    current_bottom = (bottom / res_y) * total_height
    current_top = current_bottom + current_height

    bbox = calculate_bounding_box(
        current_left, current_right, current_bottom, current_top, rot)
    current_bb_left = bbox[0]
    current_bb_right = bbox[1]
    current_bb_bottom = bbox[2]
    current_bb_top = bbox[3]

    current_bb_width = current_bb_right - current_bb_left
    current_bb_height = current_bb_top - current_bb_bottom

    collapse_offset_x = -current_bb_left
    collapse_offset_y = -current_bb_bottom
    
    scale_offset_x = (bb_width - current_bb_width) / 2
    scale_offset_y = (bb_height - current_bb_height) / 2
    
    offset_x, null, offset_y, null = get_strip_box(scene, strip)
    if strip.use_translation:
        strip.transform.offset_x = 0
        strip.transform.offset_y = 0
    
    if strip.translation_unit == 'PERCENT':
        primary_offset_x = (primary_offset_x / total_width) * 100
        primary_offset_y = (primary_offset_y / total_height) * 100
        
        collapse_offset_x = (collapse_offset_x / total_width) * 100
        collapse_offset_y = (collapse_offset_y / total_height) * 100
        
        scale_offset_x = (scale_offset_x / total_width) * 100
        scale_offset_y = (scale_offset_y / total_height) * 100
        
        offset_x = (offset_x / res_x) * 100
        offset_y = (offset_y / res_y) * 100
    
    combo_offset_x = sum([primary_offset_x, collapse_offset_x, scale_offset_x, offset_x])
    combo_offset_y = sum([primary_offset_y, collapse_offset_y, scale_offset_y, offset_y])

    strip.translate_start_x += combo_offset_x
    strip.translate_start_y += combo_offset_y
    
    strip.scale_start_x = scale_ratio_x * strip.scale_start_x
    strip.scale_start_y = scale_ratio_y * strip.scale_start_y
    
