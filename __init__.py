import bpy
import mathutils

from .operators.tf_add_transform import TF_Add_Transform
from .operators.tf_position import TF_Position
from .operators.tf_scale import TF_Scale
from .operators.tf_rotation import TF_Rotation
from .operators.tf_alpha import TF_Alpha
from .operators.tf_crop import TF_Crop

from .operators.tf_draw_selection import TF_Draw_Selection
from .operators.tf_select import TF_Select

from .operators.tf_call_menu import TF_Call_Menu
from .operators.tf_menu_insert_kf import TF_Menu_Insert_KF
from .operators.tf_insert_keyframe import TF_Insert_KeyFrame

from .operators.tf_set_cursor2d import TF_Set_Cursor2D
from .operators.tf_increment_pivot import TF_Increment_Pivot
from .operators.tf_decrement_pivot import TF_Decrement_Pivot

from .operators.tf_collapse_canvas import TF_Collapse_Canvas

from .operators.tools.draw_callback_px_point import draw_callback_px_point
from .operators.tools.draw_callback_px_2d_cursor import draw_callback_px_2d_cursor

_handle_2d_cursor = None

bl_info = {
    "name": "VSE Transform tool",
    "description": "",
    "author": "kgeogeo & DoubleZ",
    "version": (1, 0, 1),
    "blender": (2, 7, 9),
    "wiki_url": "",
    "tracker_url":"",
    "category": "Sequencer"}

def Add_Icon_Pivot_Point(self, context):
    seq = context.scene
    layout = self.layout
    layout.prop(
        context.scene, "seq_pivot_type", text='',
        expand=False,  icon_only=True
    )

def update_seq_cursor2d_loc(self,context):
    context.area.tag_redraw()

def update_pivot_point(self,context):
    global _handle_2d_cursor

    if context.scene.seq_pivot_type == '2':
        args = (self, context)
        _handle_2d_cursor = bpy.types.SpaceSequenceEditor.draw_handler_add(
            draw_callback_px_2d_cursor, args, 'PREVIEW', 'POST_PIXEL')
    else:
        if _handle_2d_cursor:
            bpy.types.SpaceSequenceEditor.draw_handler_remove(
                _handle_2d_cursor, 'PREVIEW')
            _handle_2d_cursor = None

def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.seq_cursor2d_loc = bpy.props.IntVectorProperty(
        name="Scales",
        description="location of the cursor2d",
        subtype = 'XYZ',
        default=(50, 50),
        size=2,
        step=1,
        update = update_seq_cursor2d_loc
    )

    item_pivot_point = (
        ('0','Median Point','', 'ROTATECENTER', 0),
        ('1','Individual Origins','', 'ROTATECOLLECTION', 1),
        ('2','2D Cursor','', 'CURSOR', 2),
        ('3','Active Strip','', 'ROTACTIVE', 3)
    )
    bpy.types.Scene.seq_pivot_type = bpy.props.EnumProperty(
        name="Pivot Point",
        default = "1",
        items=item_pivot_point,
        update = update_pivot_point
    )

    bpy.types.SEQUENCER_HT_header.append(Add_Icon_Pivot_Point)

    km = bpy.context.window_manager.keyconfigs.default.keymaps['View2D']
    kmi = km.keymap_items.new("sequencer.tf_add_transform", 'T', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_position", 'G', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_position", 'G', 'PRESS', alt=True)
    kmi = km.keymap_items.new("sequencer.tf_scale", 'S', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_scale", 'S', 'PRESS',alt=True)
    kmi = km.keymap_items.new("sequencer.tf_rotation", 'R', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_rotation", 'R', 'PRESS',alt=True)
    kmi = km.keymap_items.new("sequencer.tf_draw_alpha", 'Q', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_draw_alpha", 'Q', 'PRESS', alt=True)
    kmi = km.keymap_items.new("sequencer.tf_crop", 'C', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_crop", 'C', 'PRESS', alt=True)
    kmi = km.keymap_items.new("sequencer.tf_collapse_canvas", 'C', 'PRESS', shift=True)
    kmi = km.keymap_items.new("sequencer.tf_call_menu", 'I', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_increment_pivot", "PERIOD", 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_decrement_pivot", "COMMA", 'PRESS')
    
    mb = bpy.context.user_preferences.inputs.select_mouse
    kmi = km.keymap_items.new("sequencer.tf_select", mb + 'MOUSE', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_select", mb + 'MOUSE', 'PRESS', shift=True)
    #kmi = km.keymap_items.new("sequencer.tf_call_menu_layers", mb + 'MOUSE', 'PRESS', alt=True)
    #kmi = km.keymap_items.new("sequencer.tf_call_menu_layers", mb + 'MOUSE', 'PRESS', shift=True, alt=True)
    kmi = km.keymap_items.new("sequencer.tf_set_cursor2d", mb + 'MOUSE', 'PRESS', ctrl=True)
    
def unregister():
    bpy.types.SEQUENCER_HT_header.remove(Add_Icon_Pivot_Point)
    
    operators = [
        "sequencer.tf_add_transform",
        "sequencer.tf_position",
        "sequencer.tf_scale",
        "sequencer.tf_rotation",
        "sequencer.tf_draw_alpha",
        "sequencer.tf_draw_crop",
        "sequencer.tf_collapse_canvas",
        #"sequencer.tf_call_menu",
        "sequencer.tf_select",
        "sequencer.tf_set_cursor2d",
        "sequencer.tf_increment_pivot",
        "sequencer.tf_decrement_pivot",
    ]
    km = bpy.context.window_manager.keyconfigs.default.keymaps['View2D']
    for kmi in km.keymap_items:
        if kmi.idname in operators:
            km.keymap_items.remove(kmi)
    bpy.utils.unregister_module(__name__)
