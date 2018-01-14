import bpy

def get_pos_y(strip):
    '''Get a Strip's Y position'''
    res_y = bpy.context.scene.render.resolution_y
    if strip.translation_unit == 'PERCENT':
        pos = strip.translate_start_y * res_y / 100
    else:
        pos = strip.translate_start_y    
    return pos
