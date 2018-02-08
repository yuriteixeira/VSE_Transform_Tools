import bpy
import bgl
import math

from .operators import *

from . import addon_updater_ops
from .updater_preferences import UpdaterPreferences

from .initutils import CheckUpdate
from .initutils import InitializePivot
from .initutils import init_props


bl_info = {
    "name": "VSE Transform tool",
    "description": "",
    "author": "kgeogeo, DoubleZ, doakey3",
    "version": (1, 1, 4),
    "blender": (2, 7, 9),
    "wiki_url": "",
    "tracker_url": "",
    "category": "Sequencer"
    }


def register():
    addon_updater_ops.register(bl_info)
    bpy.utils.register_class(UpdaterPreferences)

    init_props()

    keyconfig = bpy.context.window_manager.keyconfigs['Blender Addon']
    try:
        km = keyconfig.keymaps["SequencerPreview"]
    except KeyError:
        km = keyconfig.keymaps.new("SequencerPreview", space_type="SEQUENCE_EDITOR", region_type="WINDOW")

    kmi = km.keymap_items.new("vse_transform_tools.add_transform", 'T', 'PRESS')
    kmi = km.keymap_items.new("vse_transform_tools.grab", 'G', 'PRESS')
    kmi = km.keymap_items.new("vse_transform_tools.grab", 'G', 'PRESS', alt=True)
    kmi = km.keymap_items.new("vse_transform_tools.scale", 'S', 'PRESS')
    kmi = km.keymap_items.new("vse_transform_tools.scale", 'S', 'PRESS', alt=True)
    kmi = km.keymap_items.new("vse_transform_tools.rotate", 'R', 'PRESS')
    kmi = km.keymap_items.new("vse_transform_tools.rotate", 'R', 'PRESS', alt=True)
    kmi = km.keymap_items.new("vse_transform_tools.adjust_alpha", 'Q', 'PRESS')
    kmi = km.keymap_items.new("vse_transform_tools.adjust_alpha", 'Q', 'PRESS', alt=True)
    kmi = km.keymap_items.new("vse_transform_tools.crop", 'C', 'PRESS')
    kmi = km.keymap_items.new("vse_transform_tools.crop", 'C', 'PRESS', alt=True)
    kmi = km.keymap_items.new("vse_transform_tools.autocrop", 'C', 'PRESS', shift=True)
    kmi = km.keymap_items.new("vse_transform_tools.call_menu", 'I', 'PRESS')
    kmi = km.keymap_items.new("vse_transform_tools.duplicate", "D", 'PRESS', shift=True)
    kmi = km.keymap_items.new("vse_transform_tools.delete", "DEL", "PRESS")
    kmi = km.keymap_items.new("vse_transform_tools.meta_toggle", "TAB", "PRESS")

    mouse_buttons = ['LEFT', 'RIGHT']
    rmb = bpy.context.user_preferences.inputs.select_mouse

    mouse_buttons.pop(mouse_buttons.index(rmb))
    lmb = mouse_buttons[0]

    kmi = km.keymap_items.new("vse_transform_tools.select", rmb + 'MOUSE', 'PRESS')
    kmi = km.keymap_items.new("vse_transform_tools.select", rmb + 'MOUSE', 'PRESS', shift=True)
    kmi = km.keymap_items.new("vse_transform_tools.select", 'A', 'PRESS')
    kmi = km.keymap_items.new("vse_transform_tools.set_cursor2d", lmb + 'MOUSE', 'PRESS')
    kmi = km.keymap_items.new("vse_transform_tools.set_cursor2d", lmb + 'MOUSE', 'PRESS', ctrl=True)

    bpy.utils.register_module(__name__)


def unregister():
    addon_updater_ops.unregister()
    bpy.utils.unregister_class(UpdaterPreferences)

    bpy.types.SEQUENCER_HT_header.remove(Add_Icon_Pivot_Point)

    operators = [
        "vse_transform_tools.add_transform",
        "vse_transform_tools.grab",
        "vse_transform_tools.scale",
        "vse_transform_tools.rotate",
        "vse_transform_tools.adjust_alpha",
        "vse_transform_tools.draw_crop",
        "vse_transform_tools.autocrop",
        "vse_transform_tools.select",
        "vse_transform_tools.set_cursor2d",
        "vse_transform_tools.duplicate",
        "vse_transform_tools.delete",
        "vse_transform_tools.meta_toggle",
    ]
    keyconfig = bpy.context.window_manager.keyconfigs['Blender Addon']
    try:
        km = keyconfig.keymaps["SequencerPreview"]
    except KeyError:
        km = keyconfig.keymaps.new("SequencerPreview", space_type="SEQUENCE_EDITOR", region_type="WINDOW")
    for kmi in km.keymap_items:
        if kmi.idname in operators:
            km.keymap_items.remove(kmi)

    bpy.utils.unregister_module(__name__)
