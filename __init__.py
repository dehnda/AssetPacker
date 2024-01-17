bl_info = {
    "name": "asset_exporter",
    "author": "Daniel Dehne",
    "description": "",
    "blender": (4, 0, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, FloatProperty
from bpy_extras.io_utils import ImportHelper

from asset_packer.gui.main_panel import MainPanel
from asset_packer.gui.decimate_tab import TabDecimate
from asset_packer.operators.import_fbx import ImportFbxOperator


LAYOUTS = (MainPanel, TabDecimate)
OPERATORS = (ImportFbxOperator,)


# Define a property group
class DecimateSettings(bpy.types.PropertyGroup):
    lod_ratio_1: bpy.props.FloatProperty(
        name="lod_ratio_1",
        description="This sets the ratio for LOD 1",
        default=0.7,
        min=0.0,
        max=1.0,
    )
    lod_ratio_2: bpy.props.FloatProperty(
        name="LOD ratio 2",
        description="This sets the ratio for LOD 2",
        default=0.7,
        min=0.0,
        max=1.0,
    )
    lod_ratio_3: bpy.props.FloatProperty(
        name="LOD ratio 3",
        description="This sets the ratio for LOD 1",
        default=0.7,
        min=0.0,
        max=1.0,
    )


# Register classes
def register():
    for item in LAYOUTS:
        bpy.utils.register_class(item)

    for operator in OPERATORS:
        bpy.utils.register_class(operator)

    bpy.utils.register_class(DecimateSettings)
    bpy.types.Scene.decimate_settings = bpy.props.PointerProperty(type=DecimateSettings)


def unregister():
    for item in LAYOUTS:
        bpy.utils.unregister_class(item)

    for operator in OPERATORS:
        bpy.utils.unregister_class(operator)

    bpy.utils.unregister_class(DecimateSettings)
    del bpy.types.Scene.decimate_settings
