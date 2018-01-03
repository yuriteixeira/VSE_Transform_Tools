def get_strip_box(scene, strip, transform_parent=False):
    '''Gets the left, right, bottom, top of an IMAGE or MOVIE strip'''
    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y
    
    if ((not strip.use_translation and not strip.use_crop) or 
        (transform_parent and not strip.use_translation)):
        left = 0
        right = res_x
        bottom = 0
        top = res_y
    
    elif strip.use_crop and not strip.use_translation:
        left = 0
        right = res_x - (strip.crop.min_x + strip.crop.max_x)
        bottom = 0
        top = res_y - (strip.crop.min_y + strip.crop.min_x)
    
    elif not hasattr(strip, 'elements'):
        len_crop_x = res_x
        len_crop_y = res_y
        if strip.use_crop:
            len_crop_x -= (strip.crop.min_x + strip.crop.max_x)
            len_crop_y -= (strip.crop.min_y + strip.crop.max_y)
        
        left = strip.transform.offset_x
        right = left + len_crop_x
        bottom = strip.transform.offset_y
        top = strip.transform.offset_y + len_crop_y
    
    elif strip.use_translation and not strip.use_crop:
        left = strip.transform.offset_x
        right = left + strip.elements[0].orig_width
        bottom = strip.transform.offset_y
        top = bottom + strip.elements[0].orig_height
    
    else:
        len_crop_x = strip.elements[0].orig_width - (strip.crop.min_x + strip.crop.max_x)
        len_crop_y = strip.elements[0].orig_height - (strip.crop.min_y + strip.crop.max_y)
        
        left = strip.transform.offset_x
        right = left + len_crop_x
        bottom = strip.transform.offset_y
        top = bottom + len_crop_y

    return left, right, bottom, top
