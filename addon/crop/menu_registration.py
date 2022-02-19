import bpy


def addon_sequencer_preview_crop_menu_registration(self, context):
    layout = self.layout
    st = context.space_data

    if st.view_type in {'PREVIEW', 'SEQUENCER_PREVIEW'}:
        layout.menu("vsc.crop_menu")


class AddonSequencerPreviewCropMenu(bpy.types.Menu):
    bl_label = "Crop (VSC)"
    bl_idname = "vsc.crop_menu"

    @classmethod
    def poll(cls, context):
        st = context.space_data
        return st.view_type in {'PREVIEW', 'SEQUENCER_PREVIEW'}

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_PREVIEW'
        layout.separator()
        layout.operator("vsc.crop_operator")
        layout.operator("vsc.autocrop_operator")
        layout.operator_context = 'INVOKE_DEFAULT'
