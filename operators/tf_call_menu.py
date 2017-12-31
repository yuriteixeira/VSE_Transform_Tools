import bpy

class TF_Call_Menu(bpy.types.Operator):
    bl_idname = "sequencer.tf_call_menu"
    bl_label = "Transform Call Menu"
       
    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            ret = True
        return ret and context.space_data.type == 'SEQUENCE_EDITOR' and context.region.type == 'PREVIEW'
                
    def execute(self, context):   
        bpy.ops.wm.call_menu(name="VSE_MT_Insert_keyframe_Menu")
        return {'FINISHED'}
