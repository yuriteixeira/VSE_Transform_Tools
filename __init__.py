import bpy
import bgl
import math

from .operators import TF_Add_Transform
from .operators import TF_Grab
from .operators import TF_Scale
from .operators import TF_Rotate
from .operators import TF_Adjust_Alpha
from .operators import TF_Crop

from .operators import TF_Select

from .operators import TF_Call_Menu
from .operators import TF_Menu_Insert_KF
from .operators import TF_Insert_Keyframe

from .operators import TF_Set_Cursor2d
from .operators import TF_Increment_Pivot
from .operators import TF_Decrement_Pivot

from .operators import TF_Autocrop

from datetime import datetime, timedelta
from . import addon_updater_ops
from .updater_preferences import Updater_Preferences

handle_2d_cursor = None

bl_info = {
    "name": "VSE Transform tool",
    "description": "",
    "author": "kgeogeo, DoubleZ, doakey3",
    "version": (1, 1, 1),
    "blender": (2, 7, 9),
    "wiki_url": "",
    "tracker_url":"",
    "category": "Sequencer"}

def draw_callback_px_2d_cursor(self, context):
    c2d = context.region.view2d.view_to_region(
        context.scene.seq_cursor2d_loc[0],
        context.scene.seq_cursor2d_loc[1],clip=False)

    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(1)
    bgl.glColor4f(0.7, 0.7, 0.7, 1.0)
    bgl.glPushMatrix()          
    bgl.glTranslatef(c2d[0],c2d[1],0)
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2i(0, -15)   
    bgl.glVertex2i(0, -5)    
    bgl.glVertex2i(0, 15)
    bgl.glVertex2i(0, 5)
    bgl.glVertex2i(-15, 0)   
    bgl.glVertex2i(-5, 0)
    bgl.glVertex2i(15, 0)    
    bgl.glVertex2i(5, 0)
    bgl.glEnd()
    
    size = 10
    c = []
    s = []
    for i in range(16):
        c.append(math.cos(i*math.pi/8))
        s.append(math.sin(i*math.pi/8)) 
    bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
    bgl.glBegin(bgl.GL_LINE_LOOP)
    for i in range(16):
        bgl.glVertex2f(size*c[i], size*s[i])         
    bgl.glEnd()
    
    bgl.glEnable(bgl.GL_LINE_STIPPLE)
    bgl.glLineStipple(4, 0x5555)
    bgl.glColor4f(1.0, 0.0, 0.0, 1.0)
    
    bgl.glBegin(bgl.GL_LINE_LOOP)
    for i in range(16):
        bgl.glVertex2f(size*c[i], size*s[i])         
    bgl.glEnd()
    
    bgl.glPopMatrix()
    
    bgl.glDisable(bgl.GL_LINE_STIPPLE)            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


def Add_Icon_Pivot_Point(self, context):
    layout = self.layout
    layout.prop(
        context.scene, "seq_pivot_type", text='',
        expand=False,  icon_only=True
    )

def update_seq_cursor2d_loc(self,context):
    context.area.tag_redraw()

def update_pivot_point(self, context):
    bpy.ops.sequencer.tf_initialize_pivot()

class TF_Initialize_Pivot(bpy.types.Operator):
    """
    The pivot icon won't show up if blender opens already on pivot type
    2. This operator should be called whenever an action occurs on a
    strip.
    
    This has to be in the init file because of the global variable 
    "handle_2d_cursor"
    """
    bl_idname = "sequencer.tf_initialize_pivot"
    bl_label = "Make the pivot point appear if pivot styles is currently 2D cursor"
    
    @classmethod
    def poll(cls, context):
        ret = False
        if (context.scene.sequence_editor and 
            context.space_data.type == 'SEQUENCE_EDITOR'):
            return True
        return False
    
    def execute(self, context):
        global handle_2d_cursor
        scene = context.scene
        args = (self, context)
        
        if scene.seq_pivot_type == '2' and not handle_2d_cursor:
            handle_2d_cursor = bpy.types.SpaceSequenceEditor.draw_handler_add(
                draw_callback_px_2d_cursor, args, 'PREVIEW', 'POST_PIXEL')
        elif not scene.seq_pivot_type == '2' and handle_2d_cursor:
            bpy.types.SpaceSequenceEditor.draw_handler_remove(
                handle_2d_cursor, 'PREVIEW')
            handle_2d_cursor = None
        
        return {'FINISHED'}

class TF_Check_Update(bpy.types.Operator):
    bl_idname = "sequencer.tf_check_update"
    bl_label = "Check for VSE Transform Tools Update"
    
    def update_check_responder(self, update_ready):
        if update_ready == True:
            addon_updater_ops.background_update_callback(update_ready)
            
        updater = addon_updater_ops.updater
        updater.json["last_check"] = str(datetime.now())
        updater.save_updater_json()
        
    def execute(self, context):
        settings = context.user_preferences.addons[__package__].preferences
        
        if not settings.auto_check_update:
            return {'FINISHED'}
        
        updater = addon_updater_ops.updater
        check_update = False
        
        if "last_check" not in updater.json or updater.json["last_check"] == "":
            check_update = True
        else:
            months = settings.updater_intrval_months
            days = settings.updater_intrval_days
            hours = settings.updater_intrval_hours
            minutes = settings.updater_intrval_minutes
            
            interval = timedelta(
                days=(months * 30) + days, hours=hours, minutes=minutes)
            
            now = datetime.now()
            last_check = datetime.strptime(
                updater.json['last_check'], "%Y-%m-%d %H:%M:%S.%f")
            diff = now - last_check
            
            if diff > interval:
                check_update = True
        
        if check_update:
            if not updater.update_ready and not updater.async_checking:
                updater.start_async_check_update(False, self.update_check_responder)
        
        return {'FINISHED'}

def init_properties():
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
        default="1",
        items=item_pivot_point,
        update = update_pivot_point
    )

    bpy.types.SEQUENCER_HT_header.append(Add_Icon_Pivot_Point)

def register():
    addon_updater_ops.register(bl_info)
    bpy.utils.register_class(Updater_Preferences)
    
    bpy.utils.register_module(__name__)

    init_properties()

    km = bpy.context.window_manager.keyconfigs.default.keymaps['View2D']
    kmi = km.keymap_items.new("sequencer.tf_add_transform", 'T', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_grab", 'G', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_grab", 'G', 'PRESS', alt=True)
    kmi = km.keymap_items.new("sequencer.tf_scale", 'S', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_scale", 'S', 'PRESS',alt=True)
    kmi = km.keymap_items.new("sequencer.tf_rotate", 'R', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_rotate", 'R', 'PRESS',alt=True)
    kmi = km.keymap_items.new("sequencer.tf_adjust_alpha", 'Q', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_adjust_alpha", 'Q', 'PRESS', alt=True)
    kmi = km.keymap_items.new("sequencer.tf_crop", 'C', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_crop", 'C', 'PRESS', alt=True)
    kmi = km.keymap_items.new("sequencer.tf_autocrop", 'C', 'PRESS', shift=True)
    kmi = km.keymap_items.new("sequencer.tf_call_menu", 'I', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_increment_pivot", "PERIOD", 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_decrement_pivot", "COMMA", 'PRESS')
    
    mouse_buttons = ['LEFT', 'RIGHT']
    rmb = bpy.context.user_preferences.inputs.select_mouse
    
    mouse_buttons.pop(mouse_buttons.index(rmb))
    lmb = mouse_buttons[0]
    
    kmi = km.keymap_items.new("sequencer.tf_select", rmb + 'MOUSE', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_select", rmb + 'MOUSE', 'PRESS', shift=True)
    kmi = km.keymap_items.new("sequencer.tf_select", 'A', 'PRESS')
    kmi = km.keymap_items.new("sequencer.tf_set_cursor2d", lmb + 'MOUSE', 'PRESS')
    
def unregister():
    addon_updater_ops.unregister()
    bpy.utils.unregister_class(Updater_Preferences)
    
    bpy.types.SEQUENCER_HT_header.remove(Add_Icon_Pivot_Point)
    
    operators = [
        "sequencer.tf_add_transform",
        "sequencer.tf_grab",
        "sequencer.tf_scale",
        "sequencer.tf_rotate",
        "sequencer.tf_adjust_alpha",
        "sequencer.tf_draw_crop",
        "sequencer.tf_autocrop",
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
