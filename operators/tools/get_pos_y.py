import bpy

def get_pos_y(seq):
    if seq.translation_unit == 'PERCENT':
        pos = seq.translate_start_y*bpy.context.scene.render.resolution_y/100
    else:
        pos = seq.translate_start_y    
    return pos
