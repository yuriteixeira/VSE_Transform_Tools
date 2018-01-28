import bpy
import math

from .utils import get_group_box
from .utils import reposition_strip
from .utils import reposition_transform_strip
from .utils import get_nontransformed_strips
from .utils import get_transform_strips


class Autocrop(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/IarxF14.gif)
    
    Sets the scene resolution to fit all visible selected content in 
    the preview window without changing strip sizes.
    """
    bl_idname = "vse_transform_tools.autocrop"
    bl_label = "Autocrop"
    bl_description = "Collapse canvas to fit visible content"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if scene.sequence_editor:
            return True
        return False

    def execute(self, context):
        scene = context.scene
        sequences = list(scene.sequence_editor.sequences_all)
        
        strips = []
        
        for seq in sequences:
            if (seq.frame_start < scene.frame_current and 
                    seq.frame_final_end > scene.frame_current):
                if not seq.mute and not seq.type == "SOUND" and seq.select:
                    strips.append(seq)


        group_box = get_group_box(strips)

        min_left, max_right, min_bottom, max_top = group_box

        total_width = max_right - min_left
        total_height = max_top - min_bottom

        nontransformed_strips = get_nontransformed_strips(strips)
        for strip in nontransformed_strips:
            reposition_strip(strip, group_box)

        transform_strips = get_transform_strips(strips)
        for strip in transform_strips:
            reposition_transform_strip(strip, group_box)

        scene.render.resolution_x = total_width
        scene.render.resolution_y = total_height

        return {'FINISHED'}
