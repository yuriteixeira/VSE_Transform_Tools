import bpy
from .clear_rejects import clear_rejects


def get_visible_strips():
    """
    Get a list of the strips currently visible in the preview window
    """
    scene = bpy.context.scene
    sequence_editor = scene.sequence_editor

    if len(scene.sequence_editor.meta_stack) > 0:
            strips = list(sequence_editor.meta_stack[-1].sequences)
    else:
        strips = list(scene.sequence_editor.sequences)

    rejects = []
    for strip in strips:
        if strip.frame_start > scene.frame_current:
            rejects.append(strip)
        if strip.frame_final_end <= scene.frame_current:
            rejects.append(strip)
        if strip.type == 'SOUND':
            rejects.append(strip)
        if hasattr(strip, 'input_1'):
            rejects.append(strip.input_1)
        if hasattr(strip, 'input_2'):
            rejects.append(strip.input_2)

    strips = sorted(strips, key=lambda strip: strip.channel)
    strips = clear_rejects(strips, rejects)
    
    blocked_visibility = False
    for strip in reversed(strips):
        if blocked_visibility:
                rejects.append(strip)
        if strip.blend_type in ['CROSS', 'REPLACE']:
            blocked_visibility = True

    strips = clear_rejects(strips, rejects)
    
    return strips

        
