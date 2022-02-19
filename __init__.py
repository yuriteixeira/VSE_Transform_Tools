import bpy
from bpy.types import WorkSpaceTool
from bpy.utils import register_class
from bpy.utils import unregister_class

from .addon import CropOperator, AutoCropOperator

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


def addon_sequencer_preview_crop_menu_registration(self, context):
    layout = self.layout
    st = context.space_data

    if st.view_type in {'PREVIEW', 'SEQUENCER_PREVIEW'}:
        layout.menu("vsc.crop_menu")


class AddonSequencerPreviewCropMenu(bpy.types.Menu):
    bl_label = "Crop (VSC)"
    bl_idname = "vsc.crop_menu"

    @classmethod
    def poll(cls, context):
        st = context.space_data
        return st.view_type in {'PREVIEW', 'SEQUENCER_PREVIEW'}

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_PREVIEW'
        layout.separator()
        layout.operator("vsc.crop_operator")
        layout.operator("vsc.autocrop_operator")
        layout.operator_context = 'INVOKE_DEFAULT'


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


classes = [
    AutoCropOperator,
    CropOperator,
    AddonSequencerPreviewCropMenu,
]

addon_keymaps = []


def register():
    for cls in classes:
        register_class(cls)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="SequencerPreview", space_type="SEQUENCE_EDITOR", region_type="WINDOW")

    km.keymap_items.new("vsc.autocrop_operator", 'C', 'PRESS', shift=True)
    km.keymap_items.new("vsc.crop_operator", 'C', 'PRESS', alt=True)
    km.keymap_items.new("vsc.crop_operator", 'C', 'PRESS')
    addon_keymaps.append(km)

    bpy.utils.register_tool(AddonSequencerPreviewCropTool)
    bpy.types.SEQUENCER_MT_editor_menus.append(addon_sequencer_preview_crop_menu_registration)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    wm = bpy.context.window_manager

    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)

    addon_keymaps.clear()
    bpy.utils.unregister_tool(AddonSequencerPreviewCropTool)
    bpy.types.SEQUENCER_MT_editor_menus.remove(addon_sequencer_preview_crop_menu_registration)
