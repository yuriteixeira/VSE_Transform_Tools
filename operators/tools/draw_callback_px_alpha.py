import bgl
import blf

def draw_callback_px_alpha(self, context):    
    w = context.region.width
    h = context.region.height
    line_width = 2 * (w / 10)
    x = self.first_mouse.x + (line_width / 2) - (line_width * self.alpha_init)
    y = self.first_mouse.y + self.pos.y
    
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(1)
    
    bgl.glColor4f(0, 1, 1, 1)
    
    # Numbers
    bgl.glPushMatrix()    
    bgl.glTranslatef(x - w/10 + self.pos.x,y,0)
    font_id = 0 
    blf.position(font_id, 0, 10, 0)
    blf.size(font_id, 20, 72)
    blf.draw(font_id, str(self.fac))
    bgl.glPopMatrix()
    
    # The Line
    bgl.glPushMatrix()   
    bgl.glTranslatef(x,y,0)
    bgl.glBegin(bgl.GL_LINE_LOOP)
    bgl.glVertex2f(-w/10, 0)
    bgl.glVertex2f(w/10, 0)   
    bgl.glEnd()
    bgl.glPopMatrix()

    bgl.glEnable(bgl.GL_POINT_SMOOTH)
    bgl.glPointSize(10)

    # End Squares
    bgl.glPushMatrix()    
    bgl.glTranslatef(x,y,0)
    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex2f(-w/10, 0)
    bgl.glVertex2f(w/10, 0)   
    bgl.glEnd()
    bgl.glPopMatrix()
    
    # Control Square
    bgl.glColor4f(1, 0, 0, 1)
    bgl.glPushMatrix()    
    bgl.glTranslatef(x - w/10 + self.pos.x,y,0)
    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex2f(0, 0) 
    bgl.glEnd()
    bgl.glPopMatrix()
    
    bgl.glDisable(bgl.GL_POINT_SMOOTH)
    bgl.glPointSize(1)
                
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
