import bpy
import bgl
import blf

from mathutils import Vector

from .tf_utils import process_input

def draw_callback_px_alpha(self, context):
    w = context.region.width
    h = context.region.height
    line_width = 2 * (w / 10)
    offset_x = (line_width / 2) - (line_width * self.alpha_init)
    x = self.first_mouse.x + offset_x
    y = self.first_mouse.y + self.pos.y

    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(1)

    bgl.glColor4f(0, 1, 1, 1)

    # Numbers
    bgl.glPushMatrix()
    bgl.glTranslatef(x - (w / 10) + self.pos.x, y, 0)
    font_id = 0
    blf.position(font_id, 0, 10, 0)
    blf.size(font_id, 20, 72)
    blf.draw(font_id, str(self.fac))
    bgl.glPopMatrix()

    # The Line
    bgl.glPushMatrix()
    bgl.glTranslatef(x, y, 0)
    bgl.glBegin(bgl.GL_LINE_LOOP)
    bgl.glVertex2f(-w / 10, 0)
    bgl.glVertex2f(w / 10, 0)
    bgl.glEnd()
    bgl.glPopMatrix()

    bgl.glEnable(bgl.GL_POINT_SMOOTH)
    bgl.glPointSize(10)

    # End Squares
    bgl.glPushMatrix()
    bgl.glTranslatef(x, y, 0)
    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex2f(-w / 10, 0)
    bgl.glVertex2f(w / 10, 0)
    bgl.glEnd()
    bgl.glPopMatrix()

    # Control Square
    bgl.glColor4f(1, 0, 0, 1)
    bgl.glPushMatrix()
    bgl.glTranslatef(x - (w / 10) + self.pos.x, y, 0)
    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex2f(0, 0)
    bgl.glEnd()
    bgl.glPopMatrix()

    bgl.glDisable(bgl.GL_POINT_SMOOTH)
    bgl.glPointSize(1)

    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

class TF_Adjust_Alpha(bpy.types.Operator):
    bl_idname = "sequencer.tf_adjust_alpha"
    bl_label = "Draw the selection"
    bl_options = {'REGISTER', 'UNDO'}

    quad_list = []
    first_mouse = Vector((0, 0))
    pos = Vector((0, 0))
    alpha_init = 0
    fac = 0
    key_val = ''

    handle_alpha = None

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if (scene.sequence_editor and
           scene.sequence_editor.active_strip and
           scene.sequence_editor.active_strip.select and
           context.space_data.type == 'SEQUENCE_EDITOR' and
           context.region.type == 'PREVIEW'):
            return True
        return False

    def modal(self, context, event):
        context.area.tag_redraw()
        w = context.region.width

        mouse_x = event.mouse_region_x
        mouse_x += (self.alpha_init * w) / 5
        mouse_y = event.mouse_region_y

        self.pos = Vector((mouse_x, mouse_y))
        self.pos -= self.first_mouse

        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > w/5:
            self.pos.x = w/5
        self.fac = self.pos.x / (w/5)

        process_input(self, event.type, event.value)
        if self.key_val != '':
            try:
                self.fac = abs(float(self.key_val))
                if self.fac > 1:
                    self.fac = abs(float('0.' + self.key_val.replace('.', '')))
                self.pos.x = self.fac * (w / 5)
            except ValueError:
                pass

        precision = 3
        if event.ctrl:
            precision = 1

        self.fac = round(self.fac, precision)
        context.scene.sequence_editor.active_strip.blend_alpha = self.fac

        if (event.type == 'LEFTMOUSE' or
           event.type == 'RET' or
           event.type == 'NUMPAD_ENTER'):
            bpy.types.SpaceSequenceEditor.draw_handler_remove(
                self.handle_alpha, 'PREVIEW')
            
            scene = context.scene
            if scene.tool_settings.use_keyframe_insert_auto:
                cf = context.scene.frame_current
                active_strip = context.scene.sequence_editor.active_strip
                active_strip.keyframe_insert(data_path='blend_alpha', frame=cf)
                
            
            return {'FINISHED'}

        if event.type == 'ESC' or event.type == 'RIGHTMOUSE':
            active_strip = context.scene.sequence_editor.active_strip
            active_strip.blend_alpha = self.alpha_init
            bpy.types.SpaceSequenceEditor.draw_handler_remove(
                self.handle_alpha, 'PREVIEW')
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if event.alt:
            for strip in context.selected_sequences:
                strip.blend_alpha = 1.0
            return {'FINISHED'}

        else:
            mouse_x = event.mouse_region_x
            mouse_y = event.mouse_region_y
            self.first_mouse = Vector((mouse_x, mouse_y))

            active_strip = context.scene.sequence_editor.active_strip
            self.alpha_init = active_strip.blend_alpha
            self.key_val != ''

            args = (self, context)
            self.handle_alpha = bpy.types.SpaceSequenceEditor.draw_handler_add(
                draw_callback_px_alpha, args, 'PREVIEW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
