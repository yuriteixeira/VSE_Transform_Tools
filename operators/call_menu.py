import bpy


class CallMenu(bpy.types.Operator):
    bl_idname = "vse_transform_tools.call_menu"
    bl_label = "Transform Call Menu"

    @classmethod
    def poll(cls, context):
        if (context.scene.sequence_editor and
           context.space_data.type == 'SEQUENCE_EDITOR' and
           context.region.type == 'PREVIEW'):
            return True
        return False

    def execute(self, context):
        bpy.ops.wm.call_menu(name="VSE_MT_Insert_keyframe_Menu")
        return {'FINISHED'}
