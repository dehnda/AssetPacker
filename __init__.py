bl_info = {
    "name": "Asset Packer",
    "author": "Daniel Dehne",
    "description": "Decimate, PBR Setup and export multiple texture resolutions",
    "blender": (4, 0, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}

import bpy
from bpy.types import PropertyGroup, Image
from bpy.props import FloatProperty, PointerProperty, StringProperty, BoolProperty

from AssetPacker.gui.main_panel import AP_PT_MainPanel
from AssetPacker.gui.decimate_tab import AP_PT_TabDecimate
from AssetPacker.gui.export_tab import AP_PT_ExportTab
from AssetPacker.operators.import_fbx import ImportFbxOperator


LAYOUTS = (AP_PT_MainPanel, AP_PT_TabDecimate, AP_PT_ExportTab)
OPERATORS = (ImportFbxOperator,)


# Define a property group
class DecimateSettings(PropertyGroup):
    lod_ratio_1: FloatProperty(
        name="lod_ratio_1",
        description="This sets the ratio for LOD 1",
        default=0.7,
        min=0.0,
        max=1.0,
    )
    lod_ratio_2: FloatProperty(
        name="LOD ratio 2",
        description="This sets the ratio for LOD 2",
        default=0.7,
        min=0.0,
        max=1.0,
    )
    lod_ratio_3: FloatProperty(
        name="LOD ratio 3",
        description="This sets the ratio for LOD 1",
        default=0.7,
        min=0.0,
        max=1.0,
    )


class PBRTexturesSettings(PropertyGroup):
    base_color: PointerProperty(name="Base Color", type=Image)
    metallic: PointerProperty(name="Metallic", type=Image)
    normal: PointerProperty(name="Normal", type=Image)
    emission: PointerProperty(name="Emission", type=Image)
    ao: PointerProperty(name="Ambient Occlusion", type=Image)
    roughness: PointerProperty(name="Roughness", type=Image)
    opacity: PointerProperty(name="Opacity", type=Image)
    folder_export_path: StringProperty(name="folder_export_path")
    export_lods: BoolProperty(name="export_lods")


SETTINGS: dict = {
    "decimate_settings": DecimateSettings,
    "pbr_texture_settings": PBRTexturesSettings,
}


# Register classes
def register():
    bpy.utils.register_class(DecimateSettings)
    bpy.types.Scene.decimate_settings = bpy.props.PointerProperty(type=DecimateSettings)

    bpy.utils.register_class(PBRTexturesSettings)
    bpy.types.Scene.pbr_textures_settings = bpy.props.PointerProperty(
        type=PBRTexturesSettings
    )

    for item in LAYOUTS:
        bpy.utils.register_class(item)

    for operator in OPERATORS:
        bpy.utils.register_class(operator)


def unregister():
    bpy.utils.unregister_class(PBRTexturesSettings)
    del bpy.types.Scene.pbr_textures_settings
    bpy.utils.unregister_class(DecimateSettings)
    del bpy.types.Scene.decimate_settings

    for item in LAYOUTS:
        bpy.utils.unregister_class(item)

    for operator in OPERATORS:
        bpy.utils.unregister_class(operator)
