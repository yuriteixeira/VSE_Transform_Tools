import bpy

def set_pos_y(seq,pos):
    if seq.translation_unit == 'PERCENT':
        pos = pos*100/bpy.context.scene.render.resolution_y
    return pos 
