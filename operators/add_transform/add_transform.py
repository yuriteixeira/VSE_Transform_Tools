import bpy

from ..utils.geometry import get_strip_box, get_transform_box
from ..utils.selection import get_input_tree


class PREV_OT_add_transform(bpy.types.Operator):
    """
    Adds a transform modifier to the selected strip(s)
    """
    bl_idname = "vse_transform_tools.add_transform"
    bl_label = "Add Transform"
    bl_description = "Add transform modifier to the selected strip(s)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.scene.sequence_editor:
            return True
        return False

    def execute(self, context):

        scene = context.scene

        selected_strips = []
        for strip in context.selected_sequences:
            if not strip.type == 'SOUND':
                selected_strips.append(strip)

        for strip in selected_strips:
            strip.use_float = True

            bpy.ops.sequencer.select_all(action='DESELECT')
            scene.sequence_editor.active_strip = strip
            bpy.ops.sequencer.effect_strip_add(type="TRANSFORM")

            transform_strip = context.scene.sequence_editor.active_strip
            transform_strip.name = "[TR]-%s" % strip.name

            transform_strip.blend_type = 'ALPHA_OVER'
            transform_strip.blend_alpha = strip.blend_alpha

            transform_strip.translation_unit = "PIXELS"

            tree = get_input_tree(transform_strip)[1::]
            for child in tree:
                child.mute = True

            strip.crop.min_x = 0
            strip.crop.max_x = 0
            strip.crop.min_y = 0
            strip.crop.max_y = 0

            if strip.type == 'TRANSFORM':
                left, right, bottom, top = get_transform_box(strip)
            else:
                left, right, bottom, top = get_strip_box(strip)

            width = right - left
            height = top - bottom

            res_x = context.scene.render.resolution_x
            res_y = context.scene.render.resolution_y

            # ratio_x = width / res_x
            # ratio_y = height / res_y
            #
            # transform_strip.scale_start_x = ratio_x
            # transform_strip.scale_start_y = ratio_y
            #
            # offset_x = strip.transform.offset_x
            # offset_y = strip.transform.offset_y

            # Transform operation are now cumulated, no need to mimic them in the transform strip

            transform_strip.scale_start_x = 1
            transform_strip.scale_start_y = 1

            # offset_x = 0
            # offset_y = 0
            #
            # flip_x = 1
            # if strip.use_flip_x:
            #     flip_x = -1
            #
            # flip_y = 1
            # if strip.use_flip_y:
            #     flip_y = -1
            #
            # pos_x = offset_x + (width / 2) - (res_x / 2)
            # pos_x *= flip_x
            #
            # pos_y = offset_y + (height / 2) - (res_y / 2)
            # pos_y *= flip_y

            # if transform_strip.translation_unit == 'PERCENT':
            #     pos_x = (pos_x / res_x) * 100
            #     pos_y = (pos_y / res_y) * 100

            # transform_strip.translate_start_x = pos_x
            # transform_strip.translate_start_y = pos_y

            transform_strip.translate_start_x = 0
            transform_strip.translate_start_y = 0

        return {'FINISHED'}
