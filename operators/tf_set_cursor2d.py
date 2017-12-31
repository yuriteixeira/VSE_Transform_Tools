import bpy

class TF_Set_Cursor2D(bpy.types.Operator):
    bl_label = "Set le Cursor2D"
    bl_idname = "sequencer.tf_set_cursor2d"
    
    @classmethod
    def poll(cls, context):
        print(context.scene.seq_pivot_type)
        if (context.scene.sequence_editor and
            context.space_data.type == 'SEQUENCE_EDITOR' and
            context.region.type == 'PREVIEW' and
            context.scene.seq_pivot_type == '2'):
            return True
        return False
                
    def invoke(self, context, event):
        temp = context.region.view2d.region_to_view(event.mouse_region_x,event.mouse_region_y)
        context.scene.seq_cursor2d_loc = [round(temp[0]),round(temp[1])]
        return {'FINISHED'} 
