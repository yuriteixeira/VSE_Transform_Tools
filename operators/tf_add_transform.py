import bpy

from .tools.set_pos_x import set_pos_x
from .tools.set_pos_y import set_pos_y
from .tools.crop_scale import crop_scale

class TF_Add_Transform(bpy.types.Operator):
    bl_idname = "sequencer.tf_add_transform"
    bl_label = "Add Transform Effect"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            ret = True
        return ret and context.space_data.type == 'SEQUENCE_EDITOR'

    def execute(self, context):
        selection = [seq for seq in context.scene.sequence_editor.sequences if seq.select and seq.type not in ['SOUND','TRANSFORM']]

        for seq in selection:
            bpy.ops.sequencer.select_all(action='DESELECT')
            context.scene.sequence_editor.active_strip = seq
            bpy.ops.sequencer.effect_strip_add(type = "TRANSFORM")
            active_seq = context.scene.sequence_editor.active_strip
            active_seq.name = "[TR]-%s" % seq.name
            seq.mute = True
            active_seq.blend_alpha = seq.blend_alpha

            active_seq.blend_type = seq.blend_type
            seq.blend_alpha = 1
            if seq.type in ['MOVIE','IMAGE']:
                if not seq.use_crop:
                    seq.use_crop = True
                    seq.crop.min_x = seq.crop.min_y = seq.crop.max_x = seq.crop.max_y = 0

                if seq.use_translation:
                    len_crop_x = seq.elements[0].orig_width - (seq.crop.min_x + seq.crop.max_x)
                    len_crop_y = seq.elements[0].orig_height - (seq.crop.min_y + seq.crop.max_y)
                    res_x = context.scene.render.resolution_x
                    res_y = context.scene.render.resolution_y

                    ratio_x = len_crop_x/res_x
                    ratio_y = len_crop_y/res_y
                    if ratio_x > 1:
                        ratio_y *= 1/ratio_x
                    if ratio_y > 1:
                        ratio_x *= 1/ratio_y
                    active_seq.scale_start_x = ratio_x
                    active_seq.scale_start_y = ratio_y
                    
                    active_seq.translate_start_x = set_pos_x(active_seq, seq.transform.offset_x + len_crop_x/2 - context.scene.render.resolution_x/2)
                    active_seq.translate_start_y = set_pos_y(active_seq, seq.transform.offset_y + len_crop_y/2 - context.scene.render.resolution_y/2)
                    seq.use_translation = False
                else:
                    crop_scale(active_seq,1)

        return {'FINISHED'}
