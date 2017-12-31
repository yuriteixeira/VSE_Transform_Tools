import bpy

from .tools.make_quad import make_quad
from .tools.draw_callback_px_select import draw_callback_px_select

class TF_Draw_Selection(bpy.types.Operator):
    bl_idname = "sequencer.tf_draw_selection"
    bl_label = "Draw the selection"
    quad_list = []

    t = 0
    close = False
    _timer = None
    _handle_select = None

    def modal(self, context, event):
        context.area.tag_redraw()
        mb = bpy.context.user_preferences.inputs.select_mouse

        if event.type == 'TIMER':
            self.t += 1

        if self.t>20:
            context.window_manager.event_timer_remove(self._timer)
            bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_select, 'PREVIEW')

            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        
        args = (self, context)
        
        self._handle_select = bpy.types.SpaceSequenceEditor.draw_handler_add(draw_callback_px_select, args, 'PREVIEW', 'POST_PIXEL')
        
        self._timer = context.window_manager.event_timer_add(0.01, context.window)
        
        context.window_manager.modal_handler_add(self)
        
        self.quad_list=[]
        
        for seq in reversed(context.scene.sequence_editor.sequences):
            if seq.type == 'TRANSFORM':
                self.quad_list.append([seq, make_quad(seq)])
        
        return {'RUNNING_MODAL'}
