import bpy
from bpy.types import WorkSpaceTool
from bpy.utils import register_class
from bpy.utils import unregister_class

from .operators import *

bl_info = {
    "name": "Video Strip Crop (VSC)",
    "description": "Crop video strips in Video Sequence Editor (VSE)",
    "author": "yuriteixeira",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "wiki_url": "http://www.yuriteixeira.com.br/blender-vsc/",
    "tracker_url": "https://github.com/yuriteixeira/blender-vsc/discussions",
    "category": "Sequencer"
}


def addon_sequencer_menu(self, context):
    layout = self.layout
    st = context.space_data

    if st.view_type in {'PREVIEW', 'SEQUENCER_PREVIEW'}:
        layout.menu("AddonSequencerPreviewToolbar")


class AddonSequencerPreviewToolbar(bpy.types.Menu):
    bl_label = "Transform"
    bl_idname = "AddonSequencerPreviewToolbar"

    @classmethod
    def poll(cls, context):
        st = context.space_data
        return st.view_type in {'PREVIEW', 'SEQUENCER_PREVIEW'}

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_PREVIEW'
        layout.separator()
        layout.operator("vse_transform_tools.crop")
        layout.operator("vse_transform_tools.autocrop")
        layout.operator_context = 'INVOKE_DEFAULT'


class AddonSequencerPreviewCropTool(WorkSpaceTool):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_context_mode = 'PREVIEW'
    bl_idname = "transform_tool.crop"
    bl_label = "Crop"
    bl_description = (
        "Crop Strip in Preview"
    )
    bl_icon = "ops.sequencer.blade"
    bl_widget = None
    operator = "transform.translate",
    bl_keymap = (
        ("vse_transform_tools.crop", {"type": 'LEFTMOUSE', "value": 'PRESS'}, None),
        ("vse_transform_tools.crop", {"type": 'LEFTMOUSE', "value": 'PRESS', "ctrl": True},
         {"properties": []}),
    )

    @classmethod
    def poll(cls, context):
        if context.scene and context.scene.sequence_editor and context.scene.sequence_editor.active_strip:
            return context.scene.sequence_editor.active_strip.type == 'TRANSFORM'
        else:
            return False


classes = [
    AutoCropOperator,
    CropOperator,
    AddonSequencerPreviewToolbar,
]

addon_keymaps = []


def register():
    for cls in classes:
        register_class(cls)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="SequencerPreview", space_type="SEQUENCE_EDITOR", region_type="WINDOW")

    km.keymap_items.new("vse_transform_tools.autocrop", 'C', 'PRESS', shift=True)
    km.keymap_items.new("vse_transform_tools.crop", 'C', 'PRESS', alt=True)
    km.keymap_items.new("vse_transform_tools.crop", 'C', 'PRESS')
    addon_keymaps.append(km)

    bpy.utils.register_tool(AddonSequencerPreviewCropTool)
    bpy.types.SEQUENCER_MT_editor_menus.append(addon_sequencer_menu)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    wm = bpy.context.window_manager

    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)

    addon_keymaps.clear()
    bpy.utils.unregister_tool(AddonSequencerPreviewCropTool)
    bpy.types.SEQUENCER_MT_editor_menus.remove(addon_sequencer_menu)
