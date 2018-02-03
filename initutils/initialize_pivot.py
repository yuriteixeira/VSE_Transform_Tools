import bpy
from .draw_2d_cursor import draw_2d_cursor


class InitializePivot(bpy.types.Operator):
    """
    The pivot icon won't show up if blender opens already on pivot type
    2. This operator should be called whenever an action occurs on a
    strip.

    This has to be in the init file because of the global variable
    "handle_2d_cursor"
    """
    bl_idname = "vse_transform_tools.initialize_pivot"
    bl_label = "Make the pivot point appear if pivot style is currently '2D cursor'"

    handle_2d_cursor = None

    @classmethod
    def poll(cls, context):
        ret = False
        if (context.scene.sequence_editor and
                context.space_data.type == 'SEQUENCE_EDITOR'):
            return True
        return False

    def execute(self, context):
        global handle_2d_cursor
        scene = context.scene
        args = (self, context)

        if scene.seq_pivot_type == '2' and not self.handle_2d_cursor:
            seq_editor = bpy.types.SpaceSequenceEditor
            self.handle_2d_cursor = seq_editor.draw_handler_add(
                draw_2d_cursor, args, 'PREVIEW', 'POST_PIXEL')
        elif not scene.seq_pivot_type == '2' and handle_2d_cursor:
            bpy.types.SpaceSequenceEditor.draw_handler_remove(
                self.handle_2d_cursor, 'PREVIEW')
            self.handle_2d_cursor = None

        return {'FINISHED'}
