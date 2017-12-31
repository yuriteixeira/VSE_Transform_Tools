class TF_Call_Menu_Layers(bpy.types.Operator):
    bl_label = "Transform Call Menu Layers"
    bl_idname = "sequencer.tf_call_menu_layers"
       
    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            ret = True
        return ret and context.space_data.type == 'SEQUENCE_EDITOR' and context.region.type == 'PREVIEW'
                
    def invoke(self, context,event):   
        global multi
        global po
                
        pos = context.region.view2d.region_to_view(event.mouse_region_x,event.mouse_region_y)
        po = Vector((pos[0],pos[1]))
        
        multi = True if event.shift else False 
           
        bpy.ops.wm.call_menu(name="VSE_MT_Menu_Layers")
        return {'FINISHED'}
