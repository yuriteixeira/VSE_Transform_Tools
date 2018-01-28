import bpy
from .get_highest_transform import get_highest_transform

def get_highest_transforms():
    """
    Go through each strip and get the highest transform for each
    """
    selected = bpy.context.selected_sequences
    
    transform_strips = []
    
    for strip in selected:
        transform_strip = get_highest_transform(strip)
        if transform_strip not in transform_strips:
            transform_strips.append(transform_strip)
    
    return transform_strips
    
def ensure_transforms():
    """
    Ensure the selected strips only consist of transform strips
    """
    context = bpy.context
    scene = context.scene
    
    transforms = get_highest_transforms()
    
    for strip in context.selected_sequences:
        if not strip in transforms:
            strip.select = False
    for strip in transforms:
        strip.select = True
    new_active = get_highest_transform(scene.sequence_editor.active_strip)
    scene.sequence_editor.active_strip = new_active
    
    final_selected = []
    for strip in transforms:
        bpy.ops.sequencer.select_all(action="DESELECT")
        if not strip.type == "TRANSFORM":
            strip.select = True
            bpy.ops.vse_transform_tools.add_transform()
            active = scene.sequence_editor.active_strip
            final_selected.append(active)
        else:
            final_selected.append(strip)
    
    return final_selected
    
