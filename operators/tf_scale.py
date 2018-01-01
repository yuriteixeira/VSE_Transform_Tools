import bpy
import mathutils

from .tools.func_key_val import func_key_val
from .tools.get_fac import get_fac
from .tools.get_pos_x import get_pos_x
from .tools.get_pos_y import get_pos_y
from .tools.set_pos_x import set_pos_x
from .tools.set_pos_y import set_pos_y
from .tools.crop_scale import crop_scale

from .tools.func_constraint_axis import func_constraint_axis
from .tools.func_constraint_axis_mmb import func_constraint_axis_mmb

from .tools.draw_callback_px_point import draw_callback_px_point

class TF_Scale(bpy.types.Operator):
    bl_idname = "sequencer.tf_scale"
    bl_label = "Transform Scale"
    bl_options = {'REGISTER', 'UNDO'}

    axe_x = True
    axe_y = True
    choose_axe = False

    first_mouse = mathutils.Vector((0, 0))
    pos_clic = mathutils.Vector((0, 0))
    pos_mouse = mathutils.Vector((0, 0))

    tab_init = []
    tab_init_t = []
    tab = []

    center_area = mathutils.Vector((0, 0))
    center_real = mathutils.Vector((0, 0))
    vec_init = mathutils.Vector((0, 0))
    vec_act = mathutils.Vector((0, 0))

    key_val = '+0'
    key_period = False
    key_period_val = 1

    _handle_line = None
    _handle_axes = None
    
    slow_factor = 10
    pre_slow_vec = mathutils.Vector((0,0))
    length_subtraction = 0
    slow_diff = 0

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
            self.pos_mouse = mathutils.Vector(
                (event.mouse_region_x, event.mouse_region_y))
            self.vec_act = self.pos_mouse - self.center_area
            diff = (self.vec_act.length - self.length_subtraction) / self.vec_init.length

            func_constraint_axis_mmb(
                self, context, event.type, event.value,
                self.sign_rot * context.scene.sequence_editor.active_strip.rotation_start)

            func_key_val(self, event.type, event.value)
            if self.key_val != '+0':
                diff = abs(float(self.key_val))

            func_constraint_axis(
                self, context, event.type, event.value,
                self.sign_rot*context.scene.sequence_editor.active_strip.rotation_start)

            if 'SHIFT' in event.type and event.value == 'PRESS':
                self.pre_slow_vec = self.vec_act
            
            elif 'SHIFT' in event.type and event.value == 'RELEASE':
                diff = ((self.pre_slow_vec.length - self.length_subtraction) / self.vec_init.length) + self.slow_diff
                self.length_subtraction += ((self.vec_act.length - self.pre_slow_vec.length) * (self.slow_factor - 1)) / self.slow_factor
                
            
            elif event.shift:
                len_diff = self.vec_act.length - self.pre_slow_vec.length
                adjusted_len_diff = (len_diff / self.slow_factor) + self.pre_slow_vec.length
                self.slow_diff = (adjusted_len_diff / self.pre_slow_vec.length) - 1
                diff = ((self.pre_slow_vec.length - self.length_subtraction) / self.vec_init.length) + self.slow_diff
                
            diff_x = diff if self.axe_x else 1

            diff_y = diff if self.axe_y else 1

            precision = 1 if event.ctrl else 5


            info_x = round(diff_x, precision)
            info_y = round(diff_y, precision)
            if not self.axe_x:
                context.area.header_text_set("Scale: %.4f along local Y" % info_y)#
            if not self.axe_y:
                context.area.header_text_set("Scale: %.4f along local X" % info_x)#
            if self.axe_x and self.axe_y :
                context.area.header_text_set("Scale X:%.4f Y: %.4f" % (info_x, info_y))#

            for seq, init_s, init_t in zip(self.tab, self.tab_init, self.tab_init_t):
                seq.scale_start_x =  init_s[0] * round(diff_x, precision)
                seq.scale_start_y =  init_s[1] * round(diff_y, precision)

                sign_x = -1 if seq.use_flip_x else 1
                sign_y = -1 if seq.use_flip_y else 1
                if context.scene.seq_pivot_type in ['0','3']:
                    seq.translate_start_x = set_pos_x(seq, (init_t[0] - sign_x*self.center_real.x) * round(diff_x, precision) + sign_x*self.center_real.x)
                    seq.translate_start_y = set_pos_y(seq, (init_t[1] - sign_y*self.center_real.y) * round(diff_y, precision) + sign_y*self.center_real.y)

                if context.scene.seq_pivot_type == '2':
                    fac = get_fac()
                    center_c2d = mathutils.Vector((sign_x*context.scene.seq_cursor2d_loc[0],sign_y*context.scene.seq_cursor2d_loc[1]))/fac
                    seq.translate_start_x = set_pos_x(seq, (init_t[0] - center_c2d.x) * round(diff_x, precision) + center_c2d.x)
                    seq.translate_start_y = set_pos_y(seq, (init_t[1] - center_c2d.y) * round(diff_y, precision) + center_c2d.y)

        if event.type == 'LEFTMOUSE' or event.type == 'RET' or event.type == 'NUMPAD_ENTER' or not self.tab:
            bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_line, 'PREVIEW')
            if self._handle_axes:
                bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_axes, 'PREVIEW')
            context.area.header_text_set()
            return {'FINISHED'}

        if event.type == 'ESC' or event.type == 'RIGHTMOUSE':
            for seq, init_s, init_t in zip(self.tab, self.tab_init, self.tab_init_t):
                seq.scale_start_x = init_s[0]
                seq.scale_start_y = init_s[1]
                seq.translate_start_x = set_pos_x(seq, init_t[0])
                seq.translate_start_y = set_pos_y(seq, init_t[1])

            bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_line, 'PREVIEW')
            if self._handle_axes:
                bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_axes, 'PREVIEW')
            context.area.header_text_set()
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):

        if event.alt :
            for seq in context.scene.sequence_editor.sequences:
                if seq.select and seq.type == 'TRANSFORM':
                    if seq.input_1.type in ['MOVIE','IMAGE']:
                        crop_scale(seq,1)
                    else:
                        seq.scale_start_x = 1
                        seq.scale_start_y = 1
            ret = 'FINISHED'
        else:
            fac = get_fac()
            self.tab_init = []
            self.tab_init_t = []
            self.tab = []
            self.center_real = mathutils.Vector((0,0))
            self.center_area = mathutils.Vector((0,0))
            key_val = '+0'
            x = 0

            for seq in context.scene.sequence_editor.sequences:
                if seq.select and seq.type == 'TRANSFORM':
                    self.tab_init.append([seq.scale_start_x,seq.scale_start_y])
                    self.tab_init_t.append([get_pos_x(seq),get_pos_y(seq)])
                    self.tab.append(seq)
                    sign_x = -1 if seq.use_flip_x else 1
                    sign_y = -1 if seq.use_flip_y else 1
                    self.sign_rot = sign_x*sign_y
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
                    self.center_area = mathutils.Vector(context.region.view2d.view_to_region(self.center_area.x*fac, self.center_area.y*fac,clip=False))
                self.vec_init = mathutils.Vector((event.mouse_region_x, event.mouse_region_y)) - self.center_area

            args = (self, context)
            self._handle_line = bpy.types.SpaceSequenceEditor.draw_handler_add(draw_callback_px_point, args, 'PREVIEW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            ret = 'RUNNING_MODAL'
        return {ret}
