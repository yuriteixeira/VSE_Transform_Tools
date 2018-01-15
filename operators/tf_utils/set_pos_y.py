import bpy

def set_pos_y(strip, pos):
    '''Set the Y position of a strip'''
    res_y = bpy.context.scene.render.resolution_y
    if strip.translation_unit == 'PERCENT':
        pos = pos * 100 / res_y
    return pos 
