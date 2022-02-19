from bpy.types import WorkSpaceTool


class AddonSequencerPreviewCropTool(WorkSpaceTool):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_context_mode = 'PREVIEW'
    bl_idname = "vsc.crop_tool"
    bl_label = "Crop Tool (VSC)"
    bl_description = (
        "Crop active strip"
    )
    bl_icon = "ops.sequencer.blade"
    bl_widget = None
    operator = "transform.translate",
    bl_keymap = (
        ("vsc.crop_operator", {"type": 'LEFTMOUSE', "value": 'PRESS'}, None),
        ("vsc.crop_operator", {"type": 'LEFTMOUSE', "value": 'PRESS', "ctrl": True},
         {"properties": []}),
    )

    @classmethod
    def poll(cls, context):
        if context.scene and context.scene.sequence_editor and context.scene.sequence_editor.active_strip:
            return context.scene.sequence_editor.active_strip.type == 'TRANSFORM'
        else:
            return False
