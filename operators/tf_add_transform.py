import bpy


class TF_Add_Transform(bpy.types.Operator):
    bl_idname = "sequencer.tf_add_transform"
    bl_label = "Add Transform Effect"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if (context.scene.sequence_editor and
           context.space_data.type == 'SEQUENCE_EDITOR'):
            return True
        return False

    def execute(self, context):
        scene = context.scene
        selected_strips = []
        for strip in scene.sequence_editor.sequences:
            if strip.select and strip.type not in ['SOUND', 'TRANSFORM']:
                selected_strips.append(strip)

        for strip in selected_strips:
            bpy.ops.sequencer.select_all(action='DESELECT')
            scene.sequence_editor.active_strip = strip
            bpy.ops.sequencer.effect_strip_add(type="TRANSFORM")

            transform_strip = context.scene.sequence_editor.active_strip
            transform_strip.name = "[TR]-%s" % strip.name

            strip.mute = True

            transform_strip.blend_type = 'ALPHA_OVER'
            transform_strip.blend_alpha = strip.blend_alpha

            if strip.type in ['MOVIE', 'IMAGE']:
                if not strip.use_crop:
                    strip.use_crop = True
                    strip.crop.min_x = 0
                    strip.crop.max_x = 0
                    strip.crop.min_y = 0
                    strip.crop.max_y = 0

                if strip.use_translation:
                    width = strip.elements[0].orig_width
                    height = strip.elements[0].orig_height

                    len_crop_x = width - (strip.crop.min_x + strip.crop.max_x)
                    len_crop_y = height - (strip.crop.min_y + strip.crop.max_y)

                    res_x = context.scene.render.resolution_x
                    res_y = context.scene.render.resolution_y

                    ratio_x = len_crop_x / res_x
                    ratio_y = len_crop_y / res_y

                    transform_strip.scale_start_x = ratio_x
                    transform_strip.scale_start_y = ratio_y

                    offset_x = strip.transform.offset_x
                    offset_y = strip.transform.offset_y

                    pos_x = offset_x + (len_crop_x / 2) - (res_x / 2)
                    pos_y = offset_y + (len_crop_y / 2) - (res_y / 2)

                    if transform_strip.translation_unit == 'PERCENT':
                        pos_x = (pos_x / res_x) * 100
                        pos_y = (pos_y / res_y) * 100

                    transform_strip.translate_start_x = pos_x
                    transform_strip.translate_start_y = pos_y

                    strip.use_translation = False

        return {'FINISHED'}
