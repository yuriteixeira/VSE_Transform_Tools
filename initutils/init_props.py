import bpy


def Add_Icon_Pivot_Point(self, context):
    layout = self.layout
    layout.prop(
        context.scene, "seq_pivot_type", text='',
        expand=False,  icon_only=True
    )


def update_pivot_point(self, context):
    bpy.ops.vse_transform_tools.initialize_pivot()


def update_seq_cursor2d_loc(self, context):
    context.area.tag_redraw()


def init_props():
    bpy.types.Scene.seq_cursor2d_loc = bpy.props.IntVectorProperty(
        name="Scales",
        description="location of the cursor2d",
        subtype='XYZ',
        default=(50, 50),
        size=2,
        step=1,
        update=update_seq_cursor2d_loc
    )

    item_pivot_point = (
        ('0', 'Median Point', '', 'ROTATECENTER', 0),
        ('1', 'Individual Origins', '', 'ROTATECOLLECTION', 1),
        ('2', '2D Cursor', '', 'CURSOR', 2),
        ('3', 'Active Strip', '', 'ROTACTIVE', 3)
    )
    bpy.types.Scene.seq_pivot_type = bpy.props.EnumProperty(
        name="Pivot Point",
        default="1",
        items=item_pivot_point,
        update=update_pivot_point
    )

    bpy.types.SEQUENCER_HT_header.append(Add_Icon_Pivot_Point)
