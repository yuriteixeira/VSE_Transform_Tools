import bpy

def get_pos_x(seq):
    if seq.translation_unit == 'PERCENT':
        pos = seq.translate_start_x*bpy.context.scene.render.resolution_x/100
    else:
        pos = seq.translate_start_x    
    return pos
