def reposition_strip(scene, strip, group_box):
    """Reposition a strip"""
    min_left, max_right, min_bottom, max_top = group_box 
    
    total_width = max_right - min_left
    total_height = max_top - min_bottom
    
    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y
    
    if strip.use_translation:
        strip.transform.offset_x -= min_left
        strip.transform.offset_y -= min_bottom
    
    if not hasattr(strip, 'elements') and strip.use_crop:
        strip.crop.min_x -= min_left
        strip.crop.max_x -= (res_x - total_width)
        strip.crop.min_y -= (res_y - total_height)
        strip.crop.max_y -= min_bottom
