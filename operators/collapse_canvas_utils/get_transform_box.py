from .get_strip_box import get_strip_box

def get_transform_box(scene, strip):
    '''
    Gets the left, right, top, bottom of a transform strip 
    (including all it's children)
    '''
    #if strip.input_1.type in ['IMAGE', 'MOVIE', 'COLOR', 'META', 'TEXT']:
    left, right, bottom, top = get_strip_box(scene, strip.input_1, transform_parent=True)
    #elif strip.input_1.type == 'TRANSFORM':
    #    left, right, bottom, top = get_transform_box(scene, strip.input_1)
    
    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y
    
    if left < 0:
        left = 0
    if right > res_x:
        right = res_x
    if bottom < 0:
        bottom = 0
    if top > res_y:
        top = res_y
    
    width = right - left
    height = top - bottom
    
    scaled_width = width * strip.scale_start_x
    scaled_height = height * strip.scale_start_y
    
    left_limit = (res_x * (1 - strip.scale_start_x)) / 2
    bottom_limit = (res_y * (1 - strip.scale_start_y)) / 2
    
    width = scaled_width
    height = scaled_height
    
    left = left_limit + left
    right = left + width
    
    bottom = bottom_limit + bottom
    top = bottom + height
    
    if strip.use_translation and strip.use_crop:
        left = left - strip.crop.min_x
        if left < 0:
            width = width + left
            left = 0
        right = left + width
        len_crop_x = res_x - (strip.crop.min_x + strip.crop.max_x)
        if right > len_crop_x:
            right = len_crop_x
            width = len_crop_x
        
        bottom = bottom - strip.crop.min_y
        if bottom < 0:
            height = height + bottom
            bottom = 0
        top = bottom + height
        len_crop_y = res_y - (strip.crop.min_y + strip.crop.max_y)
        if top > len_crop_y:
            top = len_crop_y
            height = len_crop_y
    
    elif strip.use_crop:
        left = left - strip.crop.min_x
        if left < 0:
            left = 0
        right = right - strip.crop.max_x
        if right > res_x:
            right = res_x
        width = right - left
        
        bottom = bottom - strip.crop.min_y
        if bottom < 0:
            bottom = 0
        top = top - strip.crop.max_y
        if top > res_y:
            top = res_y
        height = top - bottom
        
    if strip.use_translation:
        left = left + strip.transform.offset_x
        right = right + strip.transform.offset_x
        bottom = bottom + strip.transform.offset_y
        top = top + strip.transform.offset_y
    
    left = left + ((strip.translate_start_x / 100) * res_x)
    right = left + width
    bottom = bottom + ((strip.translate_start_y / 100) * res_y)
    top = bottom + height

    return left, right, bottom, top
