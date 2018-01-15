import bpy

class TF_Decrement_Pivot(bpy.types.Operator):
    bl_idname = "sequencer.tf_decrement_pivot"
    bl_label = "Change the pivot mode (decrease it)"
    
    @classmethod
    def poll(cls, context):
        ret = False
        if (context.scene.sequence_editor and 
            context.space_data.type == 'SEQUENCE_EDITOR'):
            return True
        return False

    def execute(self, context):
        if context.scene.seq_pivot_type == '0':
            context.scene.seq_pivot_type = '3'
        else:
            context.scene.seq_pivot_type = str(int(context.scene.seq_pivot_type) - 1)
        return {'FINISHED'}
    
