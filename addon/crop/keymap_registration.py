import bpy

addon_keymaps = []


def keymaps_register():
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="SequencerPreview", space_type="SEQUENCE_EDITOR", region_type="WINDOW")
    km.keymap_items.new("vsc.autocrop_operator", 'C', 'PRESS', shift=True)
    km.keymap_items.new("vsc.crop_operator", 'C', 'PRESS', alt=True)
    km.keymap_items.new("vsc.crop_operator", 'C', 'PRESS')
    addon_keymaps.append(km)


def keymaps_unregister():
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()
