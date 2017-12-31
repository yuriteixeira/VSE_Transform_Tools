import bgl

def draw_callback_draw_axes(self, context, angle):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(2)
    
    bgl.glPushMatrix()
    bgl.glTranslatef(self.center_area.x, self.center_area.y, 0)
    bgl.glRotatef(angle, 0, 0, 1)
    
    bgl.glBegin(bgl.GL_LINES)
    bgl.glColor4f(1.0, 0.0, 0.0, 0.2 * self.choose_axe + self.axe_x * 0.8)
    bgl.glVertex2f(-10000, 0)   
    bgl.glVertex2f(10000, 0)   
    bgl.glColor4f(0.0, 1.0, 0.0, 0.2 * self.choose_axe + self.axe_y * 0.8)
    bgl.glVertex2f(0, -10000)   
    bgl.glVertex2f(0, 10000)
    bgl.glEnd()
    
    bgl.glPopMatrix()
            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
