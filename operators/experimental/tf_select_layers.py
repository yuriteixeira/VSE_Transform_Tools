class TF_Select_Layers(bpy.types.Operator):
    bl_label = "Select Layers"
    bl_idname = "sequencer.select_layers"

    name = StringProperty()
    
    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            ret = True
        return ret and context.space_data.type == 'SEQUENCE_EDITOR'
                
    def execute(self, context):
        seq = context.scene.sequence_editor.sequences[self.name]
        if not multi :
            bpy.ops.sequencer.select_all(action='DESELECT')
            seq.select = True
        else :
            seq.select = False if seq.select else True
            
        bpy.context.scene.sequence_editor.active_strip = context.scene.sequence_editor.sequences[self.name]
        bpy.ops.sequencer.tf_draw_selection('INVOKE_DEFAULT') 
        return {'FINISHED'}
