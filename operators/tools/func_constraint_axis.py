import bpy
from .draw_callback_draw_axes import draw_callback_draw_axes

def func_constraint_axis(self, context, key, value, angle):
    if len(self.tab)>1:
        angle = 0
    if key in ['X','Y']:
        if self._handle_axes == None:
            args = (self, context,angle)
            self._handle_axes = bpy.types.SpaceSequenceEditor.draw_handler_add(
                draw_callback_draw_axes, args, 'PREVIEW', 'POST_PIXEL')
        if key == 'X' and value == 'PRESS':
            if self.axe_x == True and self.axe_y == True:
                self.axe_y = False
            elif self.axe_x == True and self.axe_y == False:
                self.axe_y = True
            elif self.axe_x == False and self.axe_y == True:
                self.axe_y = False
                self.axe_x = True

        if key == 'Y' and value == 'PRESS':
            if self.axe_x == True and self.axe_y == True:
                self.axe_x = False
            elif self.axe_x == False and self.axe_y == True:
                self.axe_x = True
            elif self.axe_x == True and self.axe_y == False:
                self.axe_y = True
                self.axe_x = False

        if self.axe_x and self.axe_y:
            if self._handle_axes:
                bpy.types.SpaceSequenceEditor.draw_handler_remove(
                    self._handle_axes, 'PREVIEW')
                self._handle_axes = None
