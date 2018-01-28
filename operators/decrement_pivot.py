import bpy


class DecrementPivot(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/3ru1Xl6.gif)
    
    Changes how strips are rotated and scaled. (sets the point of 
    origin).
    """
    bl_idname = "vse_transform_tools.decrement_pivot"
    bl_label = "Decrement Pivot"
    bl_description = "Changes the pivot mode"

    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            return True
        return False

    def execute(self, context):
        if context.scene.seq_pivot_type == '0':
            context.scene.seq_pivot_type = '3'
        else:
            context.scene.seq_pivot_type = str(int(context.scene.seq_pivot_type) - 1)
        return {'FINISHED'}
