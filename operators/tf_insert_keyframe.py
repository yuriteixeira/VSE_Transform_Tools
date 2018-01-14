import bpy

class TF_Insert_Keyframe(bpy.types.Operator):
    bl_idname = "sequencer.tf_insert_keyframe"
    bl_label = "Transform Insert KeyFrame"
    bl_options = {'REGISTER', 'UNDO'}
    
    ch = bpy.props.IntVectorProperty(name="ch",default=(0,0,0,0,0),size=5)
    
    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            ret = True
        return ret and context.space_data.type == 'SEQUENCE_EDITOR'
                
    def execute(self, context):   
        cf = context.scene.frame_current
        
        for seq in context.scene.sequence_editor.sequences:
            if seq.select and seq.type == 'TRANSFORM':
                if self.ch[0] ==1:
                    seq.keyframe_insert(data_path="translate_start_x", frame=cf)
                    seq.keyframe_insert(data_path="translate_start_y", frame=cf)
                if self.ch[1] == 1:
                    seq.keyframe_insert(data_path="rotation_start", frame=cf)
                if self.ch[2] == 1:
                    seq.keyframe_insert(data_path="scale_start_x", frame=cf)
                    seq.keyframe_insert(data_path="scale_start_y", frame=cf)
                if self.ch[3] == 1:
                    seq.keyframe_insert(data_path="blend_alpha", frame=cf)
                if self.ch[4] == 1 and seq.input_1.use_crop:
                    seq.input_1.crop.keyframe_insert(data_path="min_x", frame=cf)
                    seq.input_1.crop.keyframe_insert(data_path="max_x", frame=cf)
                    seq.input_1.crop.keyframe_insert(data_path="min_y", frame=cf)
                    seq.input_1.crop.keyframe_insert(data_path="max_y", frame=cf)    
                
        return {'FINISHED'}
