import bpy


class SetCursor2d(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/1uTD9C1.gif)
    Set the pivot point (point of origin) location. This will affect 
    how strips are rotated and scaled.
    """
    bl_label = "Set Cursor2D"
    bl_idname = "vse_transform_tools.set_cursor2d"
    bl_description = "Set the pivot point location"

    @classmethod
    def poll(cls, context):
        if (context.scene.sequence_editor and
                context.scene.seq_pivot_type == '2'):
            return True
        return False

    def invoke(self, context, event):
        bpy.ops.vse_transform_tools.initialize_pivot()

        mouse_x = event.mouse_region_x
        mouse_y = event.mouse_region_y

        pos = context.region.view2d.region_to_view(mouse_x, mouse_y)

        context.scene.seq_cursor2d_loc = [round(pos[0]), round(pos[1])]

        return {'PASS_THROUGH'}
