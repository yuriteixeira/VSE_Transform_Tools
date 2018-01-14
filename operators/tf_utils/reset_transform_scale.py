import bpy

def reset_transform_scale(strip, factor=1.0):
    '''Reset a strip to it's factor'''
    strip_in = strip.input_1
    if hasattr(strip_in, 'elements'):
        len_crop_x = strip_in.elements[0].orig_width
        len_crop_y = strip_in.elements[0].orig_height
        
        if strip_in.use_crop:
            len_crop_x -= (strip_in.crop.min_x + strip_in.crop.max_x)
            len_crop_y -= (strip_in.crop.min_y + strip_in.crop.max_y)
        
        res_x = bpy.context.scene.render.resolution_x
        res_y = bpy.context.scene.render.resolution_y
        
        ratio_x = len_crop_x / res_x
        ratio_y = len_crop_y / res_y
        
        if ratio_x == 0:
            ratio_x = 0.00000001
        if ratio_y == 0:
            ratio_y = 0.00000001
        
        if ratio_x > ratio_y:
            ratio_y *= factor / ratio_x
            ratio_x = factor
        else:
            
            ratio_x *= factor / ratio_y
            ratio_y = factor
            
        strip.scale_start_x = ratio_x
        strip.scale_start_y = ratio_y
        
    else:
        strip.scale_start_x = 1.0
        strip.scale_start_y = 1.0
    
