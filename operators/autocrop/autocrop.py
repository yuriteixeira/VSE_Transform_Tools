import bpy

from ..utils.geometry import get_group_box
from ..utils.geometry import reposition_strip
from ..utils.geometry import reposition_transform_strip
from ..utils.selection import get_nontransforms
from ..utils.selection import get_transforms
from ..utils.selection import get_visible_strips


class AutoCropOperator(bpy.types.Operator):
    bl_idname = "vsc.autocrop_operator"
    bl_label = "Auto-crop Operator"
    bl_description = "Fit all visible content into the scene by changing its resolution"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if scene.sequence_editor:
            return True
        return False

    def execute(self, context):
        scene = context.scene

        strips = get_visible_strips()

        if len(strips) == 0:
            return {'FINISHED'}

        group_box = get_group_box(strips)

        min_left, max_right, min_bottom, max_top = group_box
        total_width = max_right - min_left
        total_height = max_top - min_bottom

        nontransforms = get_nontransforms(strips)
        for strip in nontransforms:
            reposition_strip(strip, group_box)

        transforms = get_transforms(strips)
        for strip in transforms:
            reposition_transform_strip(strip, group_box)

        scene.render.resolution_x = total_width
        scene.render.resolution_y = total_height

        return {'FINISHED'}
