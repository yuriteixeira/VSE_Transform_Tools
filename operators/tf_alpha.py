import bpy
import mathutils

from .tools.func_key_val import func_key_val

from .tools.draw_callback_px_alpha import draw_callback_px_alpha

class TF_Alpha(bpy.types.Operator):
    bl_idname = "sequencer.tf_draw_alpha"
    bl_label = "Draw the selection"
    bl_options = {'REGISTER', 'UNDO'}
    
    quad_list = []
    first_mouse = mathutils.Vector((0,0))
    pos = mathutils.Vector((0,0))
    alpha_init = 0
    fac = 0
    key_val = '+0'

    _handle_alpha = None

    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            if context.scene.sequence_editor.active_strip:
                if context.scene.sequence_editor.active_strip.type == 'TRANSFORM':
                    if context.scene.sequence_editor.active_strip.select:
                        ret = True
        return ret and context.space_data.type == 'SEQUENCE_EDITOR' and context.region.type == 'PREVIEW'

    def modal(self, context, event):
        context.area.tag_redraw()
        w = context.region.width
        self.pos = mathutils.Vector((event.mouse_region_x + self.alpha_init * w/5,event.mouse_region_y)) - self.first_mouse
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > w/5:
            self.pos.x = w/5
        self.fac = self.pos.x / (w/5)

        func_key_val(self, event.type, event.value)
        if self.key_val != '+0':
            self.fac = abs(float(self.key_val))
            self.pos.x =  self.fac*(w/5)

        precision = 1 if event.ctrl else 3

        self.fac = round(self.fac,precision)
        context.scene.sequence_editor.active_strip.blend_alpha = self.fac

        if event.type == 'LEFTMOUSE' or event.type == 'RET' or event.type == 'NUMPAD_ENTER':
            bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_alpha, 'PREVIEW')
            return {'FINISHED'}

        if event.type == 'ESC' or event.type == 'RIGHTMOUSE':
            context.scene.sequence_editor.active_strip.blend_alpha = self.alpha_init
            bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_alpha, 'PREVIEW')
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if event.alt :
            for seq in context.scene.sequence_editor.sequences:
                if seq.select and seq.type == 'TRANSFORM':
                    seq.blend_alpha = 1.0
            ret = 'FINISHED'
        else :
            self.first_mouse = mathutils.Vector((event.mouse_region_x,event.mouse_region_y))
            self.alpha_init = context.scene.sequence_editor.active_strip.blend_alpha
            self.key_val != '+0'

            args = (self, context)
            self._handle_alpha = bpy.types.SpaceSequenceEditor.draw_handler_add(draw_callback_px_alpha, args, 'PREVIEW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            ret = 'RUNNING_MODAL'

        return {ret}
