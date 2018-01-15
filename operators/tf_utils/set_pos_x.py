import bpy

def set_pos_x(strip, pos):
    '''Set the X position of a strip'''
    res_x = bpy.context.scene.render.resolution_x
    if strip.translation_unit == 'PERCENT':
        pos = pos * 100 / res_x
    return pos 
