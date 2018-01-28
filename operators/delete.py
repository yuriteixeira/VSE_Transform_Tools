import bpy
from .utils import get_children


class Delete(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/B0L7XoV.gif)
    
    Deletes all selected strips as well as any strips that are inputs
    of those strips.
    For example, deleting a transform strip with this operator will
    also delete the strip it was transforming.
    """
    bl_idname = "vse_transform_tools.delete"
    bl_label = "Delete"
    bl_description = "Delete selected and their inputs recursively"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if (scene.sequence_editor and
           scene.sequence_editor.active_strip):
            return True
        return False

    def invoke(self, context, event):
        selected = []

        for strip in context.selected_sequences:
            if strip not in selected:
                selected.extend(get_children(strip, select=True))

        bpy.ops.sequencer.delete()

        selection_length = len(selected)
        report_message = 'Deleted ' + str(selection_length) + ' sequence'
        report_message += 's' if selection_length > 1 else ''
        self.report({'INFO'}, report_message)
        return {"FINISHED"}
