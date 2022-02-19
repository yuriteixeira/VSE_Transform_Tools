import bpy
from bpy.utils import register_class, unregister_class

from addon import CropOperator, AutoCropOperator
from addon.crop.menu_registration import AddonSequencerPreviewCropMenu, addon_sequencer_preview_crop_menu_registration
from addon.crop.toolbar_registration import AddonSequencerPreviewCropTool

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
