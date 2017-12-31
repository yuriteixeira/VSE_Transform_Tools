import bpy
import mathutils
import math

from .tools.func_key_val import func_key_val
from .tools.get_fac import get_fac
from .tools.rotate_point import rotate_point
from .tools.get_pos_x import get_pos_x
from .tools.get_pos_y import get_pos_y
from .tools.set_pos_x import set_pos_x
from .tools.set_pos_y import set_pos_y

from .tools.draw_callback_px_point import draw_callback_px_point

class TF_Rotation(bpy.types.Operator):
    bl_idname = "sequencer.tf_rotation"
    bl_label = "Transform Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    first_mouse = mathutils.Vector((0,0))
    tab_init = []
    tab_init_t = []
    tab = []

    center_area = mathutils.Vector((0,0))
    center_real = mathutils.Vector((0,0))
    vec_init = mathutils.Vector((0,0))
    vec_act = mathutils.Vector((0,0))

    key_val = '+0'
    key_period = False
    key_period_val = 1
    
    rot_marker = 0
    revolutions = 0
    
    slow_factor = 10
    pre_slow_rot = 0
    post_slow_rot = 0

    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            if context.scene.sequence_editor.active_strip:
                if context.scene.sequence_editor.active_strip.type == 'TRANSFORM':
                    ret = True
        return ret and context.space_data.type == 'SEQUENCE_EDITOR' and context.region.type == 'PREVIEW'

    def modal(self, context, event):
        context.area.tag_redraw()

        if self.tab:
            self.vec_act = mathutils.Vector((event.mouse_region_x, event.mouse_region_y)) - self.center_area
            
            rot =  math.degrees(-self.vec_init.angle_signed(self.vec_act)) + self.post_slow_rot

            if rot < 0 and self.rot_marker > 0:
                rot = 360 + rot
            elif rot > 0 and self.rot_marker < 0:
                rot = rot - 360
            
            if self.rot_marker < rot and self.rot_marker - rot <= -180:
                self.revolutions -= 1
            elif self.rot_marker > rot and self.rot_marker - rot >= 180:
                self.revolutions += 1
            
            self.rot_marker = rot
            
            if event.ctrl:
                rot -= rot % 5
            
            elif 'SHIFT' in event.type and event.value == 'PRESS':
                self.pre_slow_rot = rot + (self.revolutions * 360)
            
            elif 'SHIFT' in event.type and event.value == 'RELEASE':
                self.post_slow_rot = self.post_slow_rot + (((self.pre_slow_rot - rot - (self.revolutions * 360)) * (self.slow_factor - 1)) / self.slow_factor)
                rot = (((self.revolutions * 360) + (rot - self.pre_slow_rot)) / self.slow_factor) + self.pre_slow_rot
                
                self.pre_slow_rot = 0

            elif event.shift:
                rot = (((self.revolutions * 360) + (rot - self.pre_slow_rot)) / self.slow_factor) + self.pre_slow_rot
            
            rot = rot % 360
            if rot < -180:
                rot = rot + 360
            elif rot > 180:
                rot = rot - 360
            
            func_key_val(self, event.type, event.value)
            if self.key_val != '+0':
                rot = float(self.key_val)

            for seq, init_rot, init_t in zip(self.tab, self.tab_init, self.tab_init_t):
                if init_rot <-180:
                    init_rot = 360 + init_rot
                if init_rot > 180:
                    init_rot = -360 + init_rot
                sign_x = -1 if seq.use_flip_x else 1
                sign_y = -1 if seq.use_flip_y else 1

                seq.rotation_start = init_rot + sign_x*sign_y*rot

                if context.scene.seq_pivot_type in ['0','3']:
                    np = rotate_point(mathutils.Vector((init_t[0], init_t[1])) - mathutils.Vector((sign_x*self.center_real.x,sign_y*self.center_real.y)), sign_x*sign_y*math.radians(rot))
                    seq.translate_start_x = set_pos_x(seq, np.x + sign_x*self.center_real.x)
                    seq.translate_start_y = set_pos_y(seq, np.y + sign_y*self.center_real.y)

                if context.scene.seq_pivot_type == '2':
                    fac = get_fac()
                    center_c2d = mathutils.Vector((sign_x*context.scene.seq_cursor2d_loc[0],sign_y*context.scene.seq_cursor2d_loc[1]))/fac
                    np = rotate_point(mathutils.Vector((init_t[0], init_t[1])) - center_c2d, sign_x*sign_y*math.radians(rot))
                    seq.translate_start_x = set_pos_x(seq, np.x + center_c2d.x)
                    seq.translate_start_y = set_pos_y(seq, np.y + center_c2d.y)

            info_rot = (rot)
            context.area.header_text_set("Rotation %.4f " % info_rot)

        if event.type == 'LEFTMOUSE' or event.type == 'RET' or event.type == 'NUMPAD_ENTER' or not self.tab:
            bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_line, 'PREVIEW')
            context.area.header_text_set()
            return {'FINISHED'}

        if event.type == 'ESC' or event.type == 'RIGHTMOUSE':
            for seq, init_rot, init_t in zip(self.tab, self.tab_init, self.tab_init_t):
                seq.rotation_start = init_rot
                seq.translate_start_x = set_pos_x(seq, init_t[0])
                seq.translate_start_y = set_pos_y(seq, init_t[1])
            bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_line, 'PREVIEW')
            context.area.header_text_set()
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if event.alt :
            for seq in context.scene.sequence_editor.sequences:
                if seq.select and seq.type == 'TRANSFORM':
                    seq.rotation_start = 0.0
            ret = 'FINISHED'
        else:

            fac = get_fac()
            self.tab_init = []
            self.tab = []
            self.tab_init_t = []
            self.center_real = mathutils.Vector((0,0))
            self.center_area = mathutils.Vector((0,0))
            self.key_val = '+0'
            x = 0

            for seq in context.scene.sequence_editor.sequences:
                if seq.select and seq.type == 'TRANSFORM':
                    self.tab_init.append(seq.rotation_start)
                    self.tab_init_t.append([get_pos_x(seq),get_pos_y(seq)])
                    self.tab.append(seq)

                    sign_x = -1 if seq.use_flip_x else 1
                    sign_y = -1 if seq.use_flip_y else 1
                    self.center_real += mathutils.Vector((sign_x*get_pos_x(seq), sign_y*get_pos_y(seq)))
                    self.center_area += mathutils.Vector((sign_x*get_pos_x(seq), sign_y*get_pos_y(seq)))
                    x += 1

            if self.tab:
                self.center_real /= x
                if context.scene.seq_pivot_type == '2':
                    self.center_area = mathutils.Vector(context.region.view2d.view_to_region(context.scene.seq_cursor2d_loc[0],context.scene.seq_cursor2d_loc[1]))
                elif context.scene.seq_pivot_type == '3':
                    act_seq = context.scene.sequence_editor.active_strip
                    sign_x = -1 if act_seq.use_flip_x else 1
                    sign_y = -1 if act_seq.use_flip_y else 1
                    self.center_real = mathutils.Vector((sign_x*get_pos_x(act_seq), sign_y*get_pos_y(act_seq)))
                    self.center_area = mathutils.Vector(context.region.view2d.view_to_region(sign_x*get_pos_x(act_seq)*fac,sign_y*get_pos_y(act_seq)*fac))
                else:
                    self.center_area /= x
                    self.center_area = mathutils.Vector(context.region.view2d.view_to_region(self.center_area.x*fac,self.center_area.y*fac,clip=False))
                self.vec_init = mathutils.Vector((event.mouse_region_x, event.mouse_region_y)) - self.center_area
                
            args = (self, context)
            self._handle_line = bpy.types.SpaceSequenceEditor.draw_handler_add(draw_callback_px_point, args, 'PREVIEW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            ret = 'RUNNING_MODAL'

        return {ret}
