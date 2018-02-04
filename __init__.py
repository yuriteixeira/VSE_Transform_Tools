import bpy
import bgl
import math

from .keymap import register_keymap
from .keymap import unregister_keymap

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

    bpy.utils.register_module(__name__)

    init_props()

    register_keymap()


def unregister():
    addon_updater_ops.unregister()
    bpy.utils.unregister_class(UpdaterPreferences)

    bpy.types.SEQUENCER_HT_header.remove(Add_Icon_Pivot_Point)

    unregister_keymap()

    bpy.utils.unregister_module(__name__)
