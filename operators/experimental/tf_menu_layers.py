class TF_Menu_Layers(bpy.types.Menu):
    bl_label = "Select layer menu :"
    bl_idname = "VSE_MT_Menu_Layers"

    global po
    def draw(self, context):
        layout = self.layout
        
        fc = context.scene.frame_current
        
        for seq in reversed(context.scene.sequence_editor.sequences):
            if seq.type == 'TRANSFORM' and not seq.mute:          
                p0,p1,p2,p3 = make_quad(seq)
                if geometry.intersect_point_quad_2d(po, p0, p1, p2, p3) and seq.frame_start <= fc and (seq.frame_start + seq.frame_final_duration) >= fc: 
                    layout.operator("sequencer.select_layers",  text=seq.input_1.name, icon='SEQUENCE' ).name = seq.name
