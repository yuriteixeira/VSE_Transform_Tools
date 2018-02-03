import bpy

from .keymap import keymap

from .utils import get_potential_hotkeys
from .utils import get_conflicts
from .utils import print_conflicts
from .utils import kmi_props_setattr


def register_keymap():
    """
    Setup hotkeys for this addon
    """
    keymap_data = keymap()

    keymap_paths, potential_hotkeys = get_potential_hotkeys(keymap_data)

    conflicts = get_conflicts(keymap_paths, potential_hotkeys)
    print_conflicts(conflicts)

    keyconfig = bpy.context.window_manager.keyconfigs.addon
    if not keyconfig:
        keyconfig = bpy.context.window_manager.keyconfigs.new(
            "Blender Addon")
    for keymap_path in keymap_paths:
        group = keymap_path[0]
        space = keymap_path[1]
        region = keymap_path[2]

        try:
            km = keyconfig.keymaps[group]
        except KeyError:
            km = keyconfig.keymaps.new(
                group, space_type=space, region_type=region)

        for kmi in potential_hotkeys:
            new_keymap_item = km.keymap_items.new(
                kmi.idname, kmi.type, kmi.value,
                any=kmi.any, shift=kmi.shift, ctrl=kmi.ctrl,
                alt=kmi.alt, oskey=kmi.oskey,
                key_modifier=kmi.key_modifier, head=kmi.head)

            for attribute in kmi.properties.keys():
                value = kmi.properties[attribute]
                kmi_props_setattr(
                    new_keymap_item.properties, attribute, value)






