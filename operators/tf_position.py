import bpy
import mathutils

from .tools.func_key_val import func_key_val
from .tools.get_fac import get_fac
from .tools.get_pos_x import get_pos_x
from .tools.get_pos_y import get_pos_y
from .tools.set_pos_x import set_pos_x
from .tools.set_pos_y import set_pos_y
from .tools.view_zoom_preview import view_zoom_preview

from .tools.func_constraint_axis import func_constraint_axis
from .tools.func_constraint_axis_mmb import func_constraint_axis_mmb

class TF_Position(bpy.types.Operator):
    bl_idname = "sequencer.tf_position"
    bl_label = "Transform Position"
    bl_options = {'REGISTER', 'UNDO'}

    axe_x = True
    axe_y = True
    choose_axe = False

    first_mouse = mathutils.Vector((0,0))
    pos_clic = mathutils.Vector((0,0))
    pos_mouse = mathutils.Vector((0,0))
    center_area = mathutils.Vector((0,0))
    vec_act = mathutils.Vector((0,0))

    tab_init = []
    tab = []

    key_val = '+0'
    key_period = False
    key_period_val = 1

    _handle_axes = None

    slow_factor = 10
    pre_slow_vec = mathutils.Vector((0,0))
    reduction_vec = mathutils.Vector((0,0))
    slow_act_fm = mathutils.Vector((0,0))

    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            if context.scene.sequence_editor.active_strip:
                if context.scene.sequence_editor.active_strip.type == 'TRANSFORM':
                    ret = True
        return ret and context.space_data.type == 'SEQUENCE_EDITOR' and context.region.type == 'PREVIEW'

    def modal(self, context, event):
        if self.tab:
            self.pos_mouse = mathutils.Vector((event.mouse_region_x,event.mouse_region_y))
            self.vec_act = self.pos_mouse  - self.center_area
            vec_act_fm = self.pos_mouse - self.reduction_vec - self.first_mouse

            func_constraint_axis_mmb(self, context, event.type, event.value, 0)

            func_key_val(self, event.type, event.value)
            if self.key_val != '+0' and (not self.axe_x or not self.axe_y):
                    vec_act_fm = mathutils.Vector((float(self.key_val) / view_zoom_preview(), float(self.key_val) / view_zoom_preview()))

            func_constraint_axis(self, context, event.type, event.value, 0)

            if 'SHIFT' in event.type and event.value == 'PRESS':
                self.pre_slow_vec = self.pos_mouse

            elif 'SHIFT' in event.type and event.value == 'RELEASE':
                vec_act_fm = (self.pre_slow_vec - self.first_mouse - self.reduction_vec) + self.slow_act_fm
                self.reduction_vec = self.reduction_vec + ((self.pos_mouse - self.pre_slow_vec) * (self.slow_factor - 1)) / self.slow_factor

            elif event.shift:
                self.slow_act_fm = (self.pos_mouse - self.pre_slow_vec) / self.slow_factor
                vec_act_fm = (self.pre_slow_vec - self.first_mouse - self.reduction_vec) + self.slow_act_fm

            precision = -1 if event.ctrl else 5

            info_x = round(vec_act_fm.x * view_zoom_preview(), precision)
            info_y = round(vec_act_fm.y * view_zoom_preview(), precision)
            if not self.axe_x:
                vec_act_fm  = mathutils.Vector((0, vec_act_fm.y))
                context.area.header_text_set("D: %.4f along global Y" % info_y)
            if not self.axe_y:
                vec_act_fm = mathutils.Vector((vec_act_fm.x, 0))
                context.area.header_text_set("D: %.4f along global X" % info_x)
            if self.axe_x and self.axe_y :
                context.area.header_text_set("Dx: %.4f Dy: %.4f" % (info_x, info_y))

            for seq, init_g in zip(self.tab, self.tab_init):
                    sign_x = sign_y = 1
                    if seq.use_flip_x:
                        sign_x = -1
                    if seq.use_flip_y:
                        sign_y = -1

                    seq.translate_start_x = set_pos_x(seq, init_g[0] + round(sign_x*vec_act_fm.x * view_zoom_preview(), precision))
                    seq.translate_start_y = set_pos_y(seq, init_g[1] + round(sign_y*vec_act_fm.y * view_zoom_preview(), precision))

        if event.type == 'LEFTMOUSE' or event.type == 'RET' or event.type == 'NUMPAD_ENTER' or not self.tab:
            if self._handle_axes:
                bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_axes, 'PREVIEW')
            context.area.header_text_set()
            return {'FINISHED'}

        if event.type == 'ESC' or event.type == 'RIGHTMOUSE':
            if self._handle_axes:
                bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_axes, 'PREVIEW')
            context.area.header_text_set()
            for seq, init_g in zip(self.tab, self.tab_init):
                seq.translate_start_x = set_pos_x(seq, init_g[0])
                seq.translate_start_y = set_pos_y(seq, init_g[1])
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):

        if event.alt :
            for seq in context.scene.sequence_editor.sequences:
                if seq.select and seq.type == 'TRANSFORM':
                    seq.translate_start_x = 0
                    seq.translate_start_y = 0
            ret = 'FINISHED'
        else:
            self.first_mouse.x = event.mouse_region_x
            self.first_mouse.y = event.mouse_region_y
            self.key_val = '+0'
            fac = get_fac()
            self.tab = []
            self.tab_init = []
            self.center_area = mathutils.Vector((0,0))
            x = 0
            for seq in context.scene.sequence_editor.sequences:
                if seq.select and seq.type == 'TRANSFORM':
                    self.tab_init.append([get_pos_x(seq),get_pos_y(seq)])
                    self.tab.append(seq)
                    sign_x = -1 if seq.use_flip_x else 1
                    sign_y = -1 if seq.use_flip_y else 1
                    self.center_area += mathutils.Vector((sign_x*get_pos_x(seq), sign_y*get_pos_y(seq)))
                    x += 1

            if self.tab:
                self.center_area /= x
                self.center_area = mathutils.Vector(context.region.view2d.view_to_region(self.center_area.x*fac, self.center_area.y*fac,clip=False))
            context.window_manager.modal_handler_add(self)
            ret = 'RUNNING_MODAL'

        return {ret}
