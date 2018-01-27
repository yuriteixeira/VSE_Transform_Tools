import bpy
from mathutils import Vector

from .utils import get_pos_x
from .utils import get_pos_y
from .utils import set_pos_x
from .utils import set_pos_y

from .utils import func_constrain_axis_mmb
from .utils import func_constrain_axis
from .utils import process_input
from .utils import reset_transform_scale
from .utils import get_res_factor

from .utils import draw_callback_px_point


class Scale(bpy.types.Operator):
    bl_idname = "vse_transform_tools.scale"
    bl_label = "Transform Scale"
    bl_options = {'REGISTER', 'UNDO'}

    axis_x = True
    axis_y = True
    choose_axis = False

    first_mouse = Vector([0, 0])
    pos_clic = Vector([0, 0])
    mouse_pos = Vector([0, 0])

    vec_init = Vector([0, 0])
    vec_act = Vector([0, 0])

    center_area = Vector([0, 0])
    center_real = Vector([0, 0])

    key_val = ''

    handle_axes = None
    handle_line = None

    group_width = 0
    group_height = 0

    slow_factor = 10
    pre_slow_vec = Vector([0, 0])
    length_subtraction = 0
    slow_diff = 0

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if (scene.sequence_editor and
           scene.sequence_editor.active_strip):
            return True
        return False

    def modal(self, context, event):
        scene = context.scene

        res_x = scene.render.resolution_x
        res_y = scene.render.resolution_y

        if self.tab:
            self.mouse_pos = Vector(
                (event.mouse_region_x, event.mouse_region_y))

            self.vec_act = self.mouse_pos - self.center_area
            diff = (self.vec_act.length - self.length_subtraction) / self.vec_init.length

            func_constrain_axis_mmb(
                self, context, event.type, event.value,
                self.sign_rot * context.scene.sequence_editor.active_strip.rotation_start)

            func_constrain_axis(
                self, context, event.type, event.value,
                self.sign_rot * context.scene.sequence_editor.active_strip.rotation_start)

            process_input(self, event.type, event.value)
            if self.key_val != '':
                try:
                    diff = abs(float(self.key_val))
                except ValueError:
                    pass

            if 'SHIFT' in event.type and event.value == 'PRESS' and self.key_val == '':
                self.pre_slow_vec = self.vec_act

            elif 'SHIFT' in event.type and event.value == 'RELEASE' and self.key_val == '':
                diff = ((self.pre_slow_vec.length - self.length_subtraction) / self.vec_init.length) + self.slow_diff
                self.length_subtraction += ((self.vec_act.length - self.pre_slow_vec.length) * (self.slow_factor - 1)) / self.slow_factor

            elif event.shift and self.key_val == '':
                len_diff = self.vec_act.length - self.pre_slow_vec.length
                adjusted_len_diff = (len_diff / self.slow_factor) + self.pre_slow_vec.length
                self.slow_diff = (adjusted_len_diff / self.pre_slow_vec.length) - 1
                diff = ((self.pre_slow_vec.length - self.length_subtraction) / self.vec_init.length) + self.slow_diff

            diff_x = 1
            if self.axis_x:
                diff_x = diff

            diff_y = 1
            if self.axis_y:
                diff_y = diff

            precision = 5
            if event.ctrl:
                precision = 1

            info_x = round(diff_x, precision)
            info_y = round(diff_y, precision)
            if not self.axis_x:
                context.area.header_text_set("Scale: %.4f along local Y" % info_y)
            if not self.axis_y:
                context.area.header_text_set("Scale: %.4f along local X" % info_x)
            if self.axis_x and self.axis_y :
                context.area.header_text_set("Scale X:%.4f Y: %.4f" % (info_x, info_y))

            for strip, init_s, init_t in zip(self.tab, self.tab_init_s, self.tab_init_t):
                strip.scale_start_x =  init_s[0] * round(diff_x, precision)
                strip.scale_start_y =  init_s[1] * round(diff_y, precision)

                flip_x = 1
                if strip.use_flip_x:
                    flip_x = -1

                flip_y = 1
                if strip.use_flip_y:
                    flip_y = -1

                if context.scene.seq_pivot_type in ['0', '3']:
                    strip.translate_start_x = set_pos_x(strip, (init_t[0] - flip_x * self.center_real.x) * round(diff_x, precision) + flip_x * self.center_real.x)
                    strip.translate_start_y = set_pos_y(strip, (init_t[1] - flip_y * self.center_real.y) * round(diff_y, precision) + flip_y * self.center_real.y)

                if context.scene.seq_pivot_type == '2':
                    fac = get_res_factor()
                    center_c2d = Vector((flip_x * context.scene.seq_cursor2d_loc[0], flip_y * context.scene.seq_cursor2d_loc[1])) / fac
                    strip.translate_start_x = set_pos_x(strip, (init_t[0] - center_c2d.x) * round(diff_x, precision) + center_c2d.x)
                    strip.translate_start_y = set_pos_y(strip, (init_t[1] - center_c2d.y) * round(diff_y, precision) + center_c2d.y)

            if (event.type == 'LEFTMOUSE' or
               event.type == 'RET' or
               event.type == 'NUMPAD_ENTER' or
               not self.tab):

                bpy.types.SpaceSequenceEditor.draw_handler_remove(self.handle_line, 'PREVIEW')

                scene = context.scene
                if scene.tool_settings.use_keyframe_insert_auto:
                    cf = context.scene.frame_current
                    pivot_type = context.scene.seq_pivot_type
                    if (pivot_type == '0' and len(self.tab) > 1) or pivot_type == '2':
                        for strip in self.tab:
                            strip.keyframe_insert(data_path='translate_start_x', frame=cf)
                            strip.keyframe_insert(data_path='translate_start_y', frame=cf)
                            strip.keyframe_insert(data_path='scale_start_x', frame=cf)
                            strip.keyframe_insert(data_path='scale_start_y', frame=cf)
                    elif pivot_type == '1' or pivot_type == '3' or (pivot_type == '0' and len(self.tab) == 1):
                        for strip in self.tab:
                            strip.keyframe_insert(data_path='scale_start_x', frame=cf)
                            strip.keyframe_insert(data_path='scale_start_y', frame=cf)

                if self.handle_axes:
                    bpy.types.SpaceSequenceEditor.draw_handler_remove(self.handle_axes, 'PREVIEW')
                context.area.header_text_set()
                return {'FINISHED'}

            if event.type == 'ESC' or event.type == 'RIGHTMOUSE':
                for strip, init_s, init_t in zip(self.tab, self.tab_init_s, self.tab_init_t):
                    strip.scale_start_x = init_s[0]
                    strip.scale_start_y = init_s[1]
                    strip.translate_start_x = set_pos_x(strip, init_t[0])
                    strip.translate_start_y = set_pos_y(strip, init_t[1])

                bpy.types.SpaceSequenceEditor.draw_handler_remove(self.handle_line, 'PREVIEW')
                if self.handle_axes:
                    bpy.types.SpaceSequenceEditor.draw_handler_remove(self.handle_axes, 'PREVIEW')
                context.area.header_text_set()
                return {'FINISHED'}

        else:
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        scene = context.scene
        bpy.ops.vse_transform_tools.initialize_pivot()

        res_x = scene.render.resolution_x
        res_y = scene.render.resolution_y

        self.horizontal_interests = [0, res_x]
        self.vertical_interests = [0, res_y]

        if event.alt :
            for strip in context.selected_sequences:
                if strip.type == 'TRANSFORM':
                    reset_transform_scale(strip)
            return {'FINISHED'}

        else:
            self.tab_init_s = []
            self.tab_init_t = []

            self.tab = []

            self.center_real = Vector([0, 0])
            self.center_area = Vector([0, 0])

            self.key_val = ''
            self.old_key_val = '0'

            fac = get_res_factor()

            scaled_count = 0

            original_selected = context.selected_sequences
            final_selected = []
            for strip in original_selected:
                bpy.ops.sequencer.select_all(action="DESELECT")
                if not strip.type == "TRANSFORM":
                    strip.select = True
                    bpy.ops.vse_transform_tools.add_transform()
                    active = scene.sequence_editor.active_strip
                    final_selected.append(active)
                else:
                    final_selected.append(strip)
                    
            for strip in final_selected:
                strip.select = True
                self.tab.append(strip)

            for strip in self.tab:
                self.tab_init_s.append([strip.scale_start_x, strip.scale_start_y])
                self.tab_init_t.append([get_pos_x(strip), get_pos_y(strip)])

                flip_x = 1
                if strip.use_flip_x:
                    flip_x = -1

                flip_y = 1
                if strip.use_flip_y:
                    flip_y = -1

                self.sign_rot = flip_x * flip_y

                center_x = flip_x * get_pos_x(strip)
                center_y = flip_y * get_pos_y(strip)
                self.center_real += Vector([center_x, center_y])
                self.center_area += Vector([center_x, center_y])

            if self.tab:
                self.center_real /= len(self.tab)
                if scene.seq_pivot_type == '2':
                    cursor_x = context.scene.seq_cursor2d_loc[0]
                    cursor_y = context.scene.seq_cursor2d_loc[1]
                    cursor_pos = context.region.view2d.view_to_region(cursor_x, cursor_y)
                    self.center_area = Vector(cursor_pos)

                elif scene.seq_pivot_type == '3':
                    active_strip = scene.sequence_editor.active_strip

                    flip_x = 1
                    if active_strip.use_flip_x:
                        flip_x = -1

                    flip_y = 1
                    if active_strip.use_flip_y:
                        flip_y = -1

                    pos_x = flip_x * get_pos_x(active_strip)
                    pos_y = flip_y * get_pos_y(active_strip)

                    self.center_real = Vector([pos_x, pos_y])

                    pos = context.region.view2d.view_to_region(pos_x * fac, pos_y * fac)
                    self.center_area = Vector(pos)

                else:
                    self.center_area /= len(self.tab)

                    pos_x = self.center_area.x * fac
                    pos_y = self.center_area.y * fac
                    pos = context.region.view2d.view_to_region(pos_x, pos_y,clip=False)
                    self.center_area = Vector(pos)

                self.vec_init = Vector(
                    (event.mouse_region_x, event.mouse_region_y))
                self.vec_init -= self.center_area

            args = (self, context)
            self.handle_line = bpy.types.SpaceSequenceEditor.draw_handler_add(
                draw_callback_px_point, args, 'PREVIEW', 'POST_PIXEL')

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        return {'FINISHED'}
