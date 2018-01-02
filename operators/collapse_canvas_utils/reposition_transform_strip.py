import math

from .get_transform_box import get_transform_box
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
    rot_left = bbox[0]
    rot_right = bbox[1]
    rot_bottom = bbox[2]
    rot_top = bbox[3]
    
    primary_offset_x = ((rot_left - min_left) / total_width) * 100
    primary_offset_y = ((rot_bottom - min_bottom) / total_height) * 100
    
    rot_width = rot_right - rot_left
    rot_height = rot_top - rot_bottom
    
    current_width = width / scale_ratio_x
    current_height = height / scale_ratio_y
    current_left = (left / res_x) * total_width
    current_right = current_left + current_width
    current_bottom = (bottom / res_y) * total_height
    current_top = current_bottom + current_height
    
    bbox = calculate_bounding_box(
        current_left, current_right, current_bottom, current_top, rot)
    current_rot_left = bbox[0]
    current_rot_right = bbox[1]
    current_rot_bottom = bbox[2]
    current_rot_top = bbox[3]
    
    current_rot_width = current_rot_right - current_rot_left
    current_rot_height = current_rot_top - current_rot_bottom
    
    offset_x = (current_rot_left / total_width) * 100
    offset_y = (current_rot_bottom / total_height) * 100
    
    scale_offset_x = (((rot_width - current_rot_width) / 2) / total_width) * 100
    scale_offset_y = (((rot_height - current_rot_height) / 2) / total_height) * 100
    
    strip.translate_start_x += primary_offset_x - offset_x + scale_offset_x
    strip.translate_start_y += primary_offset_y - offset_y + scale_offset_y
    
    strip.scale_start_x = scale_ratio_x * strip.scale_start_x
    strip.scale_start_y = scale_ratio_y * strip.scale_start_y
