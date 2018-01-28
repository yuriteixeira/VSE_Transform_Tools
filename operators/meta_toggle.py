import bpy
from .utils import get_children

class MetaToggle(bpy.types.Operator):
    bl_idname = "vse_transform_tools.meta_toggle"
    bl_label = "Toggle Meta"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if (scene.sequence_editor):
            return True
        return False

    def invoke(self, context, event):
        scene = context.scene
        
        active = scene.sequence_editor.active_strip
        
        children = get_children(active)
        for child in children:
            try:
                if child.type == "META":
                    bpy.ops.sequencer.select_all(action="DESELECT")
                    scene.sequence_editor.active_strip = child
                    child.select = True
                    return bpy.ops.sequencer.meta_toggle('INVOKE_DEFAULT')
            except AttributeError:
                pass
                
        return bpy.ops.sequencer.meta_toggle('INVOKE_DEFAULT')
