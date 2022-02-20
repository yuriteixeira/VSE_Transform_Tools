import bpy
from bpy.utils import register_class, unregister_class

from .addon.crop.autocrop_operator import AutoCropOperator
from .addon.crop.crop_operator import CropOperator
from .addon.crop.keymap_registration import keymaps_register, keymaps_unregister
from .addon.crop.menu_registration import AddonSequencerPreviewCropMenu, addon_sequencer_preview_crop_menu_registration
from .addon.crop.toolbar_registration import AddonSequencerPreviewCropTool

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


def register():
    for cls in classes:
        register_class(cls)

    keymaps_register()
    bpy.utils.register_tool(AddonSequencerPreviewCropTool)
    bpy.types.SEQUENCER_MT_editor_menus.append(addon_sequencer_preview_crop_menu_registration)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    keymaps_unregister()
    bpy.utils.unregister_tool(AddonSequencerPreviewCropTool)
    bpy.types.SEQUENCER_MT_editor_menus.remove(addon_sequencer_preview_crop_menu_registration)
