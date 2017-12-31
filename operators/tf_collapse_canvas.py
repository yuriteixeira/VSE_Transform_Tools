import bpy
import math

class TF_Collapse_Canvas(bpy.types.Operator):
    bl_idname = "sequencer.tf_collapse_canvas"
    bl_label = "Collapse scene resolution to match clip size"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        ret = False
        if (context.scene.sequence_editor and
            context.space_data.type == 'SEQUENCE_EDITOR' and
            context.space_data.view_type == 'PREVIEW' and
            context.space_data.display_mode == 'IMAGE' and
            context.scene.sequence_editor.active_strip and
            context.scene.sequence_editor.active_strip.type == 'TRANSFORM' and
            context.scene.sequence_editor.active_strip.select and
            context.scene.sequence_editor.active_strip.input_1.type in ['MOVIE', 'IMAGE']):
            return True
        return False
    
    def execute(self, context):
        scene = context.scene
        active_seq = context.scene.sequence_editor.active_strip
        seq = active_seq.input_1
        
        res_x = scene.render.resolution_x
        res_y = scene.render.resolution_y
        
        crop_res_x = seq.elements[0].orig_width - (seq.crop.min_x + seq.crop.max_x)
        crop_res_y = seq.elements[0].orig_height - (seq.crop.min_y + seq.crop.max_y)
        
        crop_ratio_x = res_x / crop_res_x
        crop_ratio_y = res_y / crop_res_y
        
        scale_ratio_x = crop_ratio_x * active_seq.scale_start_x
        scale_ratio_y = crop_ratio_y * active_seq.scale_start_y
        
        scale_res_x = scale_ratio_x * crop_res_x
        scale_res_y = scale_ratio_y * crop_res_y

        rot = math.radians(abs(active_seq.rotation_start))
        rot_res_x = (math.sin(rot) * scale_res_y) + (math.cos(rot) * scale_res_x)
        rot_res_y = (math.sin(rot) * scale_res_x) + (math.cos(rot) * scale_res_y)
        
        rot_ratio_x = scale_res_x / rot_res_x 
        rot_ratio_y = scale_res_y /rot_res_y
        
        active_seq.translate_start_x = 0
        active_seq.translate_start_y = 0
        
        scene.render.resolution_x = rot_res_x
        scene.render.resolution_y = rot_res_y
        
        active_seq.scale_start_x = rot_ratio_x
        active_seq.scale_start_y = rot_ratio_y
        
        return {'FINISHED'}
            
