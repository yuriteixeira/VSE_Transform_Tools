import bpy

def get_pos_x(strip):
    '''Get a strips X position'''
    res_x = bpy.context.scene.render.resolution_x
    if strip.translation_unit == 'PERCENT':
        pos = strip.translate_start_x * res_x / 100
    else:
        pos = strip.translate_start_x
    return pos