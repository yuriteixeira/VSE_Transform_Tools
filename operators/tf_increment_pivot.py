import bpy

class TF_Increment_Pivot(bpy.types.Operator):
    bl_idname = "sequencer.tf_increment_pivot"
    bl_label = "Change the pivot mode"
    
    @classmethod
    def poll(cls, context):
        ret = False
        if (context.scene.sequence_editor and 
            context.space_data.type == 'SEQUENCE_EDITOR'):
            return True
        return False

    def execute(self, context):
        if context.scene.seq_pivot_type == '3':
            context.scene.seq_pivot_type = '0'
        else:
            context.scene.seq_pivot_type = str(int(context.scene.seq_pivot_type) + 1)
        return {'FINISHED'}
    
