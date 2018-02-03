import bpy

from .keymap import keymap


def unregister_keymap():
    """
    Remove the hotkeys associated with this addon from Blender
    """

    keymap_data = keymap()

    keymap_names = keymap_data.keys()
    for name in keymap_names:
        space_types = keymap_data[name].keys()
        for space_type in space_types:
            region_types = keymap_data[name][space_type].keys()
            for region in region_types:
                operator_names = keymap_data[name][space_type][region].keys()

                kc = bpy.context.window_manager.keyconfigs.addon
                km = kc.keymaps.new(
                    name, space_type=space_type, region_type=region)
                current_hotkeys = km.keymap_items

                for hotkey in current_hotkeys:
                    if hotkey.idname in operator_names:
                        km.keymap_items.remove(hotkey)
