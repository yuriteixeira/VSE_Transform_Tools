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
    "wiki_url": "https://github.com/yuriteixeira/blender-vsc#readme",
    "tracker_url": "https://github.com/yuriteixeira/blender-vsc/discussions",
    "category": "Sequencer"
}

"""
RegEx Classname
===============
[A-Z][A-Z0-9_]*_{ABBREV}_[A-Za-z0-9_]+

Abbrev
------
Header:   _HT_
Menu:     _MT_
Operator: _OT_
Panel:    _PT_
UIList:   _UL_
"""

handle_2d_cursor = None


def Add_Menu(self, context):
    layout = self.layout
    st = context.space_data

    if st.view_type in {'PREVIEW', 'SEQUENCER_PREVIEW'}:
        layout.menu("SEQUENCER_MT_transform_tools_menu")


class SEQUENCER_MT_transform_tools_menu(bpy.types.Menu):
    bl_label = "Transform"
    bl_idname = "SEQUENCER_MT_transform_tools_menu"

    @classmethod
    def poll(cls, context):
        st = context.space_data
        return st.view_type in {'PREVIEW', 'SEQUENCER_PREVIEW'}

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_PREVIEW'
        # st = context.space_data

        # if st.view_type in {'PREVIEW', 'SEQUENCER_PREVIEW'}:

        layout.separator()
        layout.operator("vse_transform_tools.crop")
        layout.operator("vse_transform_tools.autocrop")
        layout.operator_context = 'INVOKE_DEFAULT'


class vse_transform_tools_crop(WorkSpaceTool):
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

    def draw_settings(context, layout, tool):
        tool.operator_properties("vse_transform_tools.crop")
        scene = context.scene
        strip = scene.sequence_editor.active_strip
        if scene and strip and strip.type == 'TRANSFORM':
            layout.label(text=strip.name)


def get_tracker_list(self, context):
    tracks = [("None", "None", "")]
    for movieclip in bpy.data.movieclips:
        for track in movieclip.tracking.tracks:
            tracks.append((track.name, track.name, ""))
    return tracks


classes = [
    PREV_OT_autocrop,
    PREV_OT_crop,
    SEQUENCER_MT_transform_tools_menu,
]

addon_keymaps = []


def register():
    for cls in classes:
        register_class(cls)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="SequencerPreview", space_type="SEQUENCE_EDITOR", region_type="WINDOW")

    kmi = km.keymap_items.new("vse_transform_tools.autocrop", 'C', 'PRESS', shift=True)

    kmi = km.keymap_items.new("vse_transform_tools.crop", 'C', 'PRESS', alt=True)
    kmi = km.keymap_items.new("vse_transform_tools.crop", 'C', 'PRESS')

    addon_keymaps.append(km)

    bpy.utils.register_tool(vse_transform_tools_crop)

    bpy.types.SEQUENCER_MT_editor_menus.append(Add_Menu)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()

    bpy.utils.unregister_tool(vse_transform_tools_crop)

    bpy.types.SEQUENCER_MT_editor_menus.remove(Add_Menu)
