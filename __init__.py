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
from bpy.types import PropertyGroup, Image, Object
from bpy.props import (
    FloatProperty,
    PointerProperty,
    StringProperty,
    BoolProperty,
    EnumProperty,
    CollectionProperty,
)

from .gui.main_panel import AP_PT_MainPanel
from .gui.decimate_tab import AP_PT_TabDecimate
from .gui.export_tab import AP_PT_ExportTab
from .operators.import_fbx import ImportFbxOperator
from .operators.export_textures import TextureExporterOperator


LAYOUTS = (AP_PT_MainPanel, AP_PT_TabDecimate, AP_PT_ExportTab)
OPERATORS = (ImportFbxOperator, TextureExporterOperator)


# Define a property groups


class GeneralSettings(PropertyGroup):
    import_folder: StringProperty(
        name="texture_import_folder",
        description="Folder to look for textures when importing.",
        default="textures/",
    )
    decimate_on_import: BoolProperty(
        name="decimate_on_import",
        description="Apply decimate modifier on LODs automatically.",
        default=True,
    )


class SuffixSettings(PropertyGroup):
    albedo: StringProperty(
        name="albedeo",
        description="Suffix for albedo texture.",
        default="albedo",
    )
    metallic: StringProperty(
        name="metallic", description="Suffix for metallic texture.", default="metallic"
    )
    ao: StringProperty(
        name="ao_suffix", description="Suffix for AO texture.", default="ao"
    )
    normal: StringProperty(
        name="normal_suffix", description="Suffix for normal texture.", default="normal"
    )
    emission: StringProperty(
        name="emission_suffix",
        description="Suffix for emission texture.",
        default="emission",
    )
    displacement: StringProperty(
        name="displacement_suffix",
        description="Suffix for displacement texture.",
        default="displacement",
    )
    roughness: StringProperty(
        name="roughness_suffix",
        description="Suffix for roughness texture.",
        default="roughness",
    )
    opacity: StringProperty(
        name="opacity_suffix",
        description="Suffix for opacity texture.",
        default="opacity",
    )


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
        default=0.4,
        min=0.0,
        max=1.0,
    )
    lod_ratio_3: FloatProperty(
        name="LOD ratio 3",
        description="This sets the ratio for LOD 1",
        default=0.2,
        min=0.0,
        max=1.0,
    )
    lod_mesh_0: PointerProperty(name="lod0", type=Object)
    lod_mesh_1: PointerProperty(name="lod1", type=Object)
    lod_mesh_2: PointerProperty(name="lod2", type=Object)
    lod_mesh_3: PointerProperty(name="lod3", type=Object)


class PBRTexturesSettings(PropertyGroup):
    albedo: PointerProperty(name="Base Color", type=Image)
    metallic: PointerProperty(name="Metallic", type=Image)
    normal: PointerProperty(name="Normal", type=Image)
    emission: PointerProperty(name="Emission", type=Image)
    displacement: PointerProperty(name="Displacement", type=Image)
    ao: PointerProperty(name="Ambient Occlusion", type=Image)
    roughness: PointerProperty(name="Roughness", type=Image)
    opacity: PointerProperty(name="Opacity", type=Image)
    folder_export_path: StringProperty(name="folder_export_path", default="export/")
    export_lods: BoolProperty(name="export_lods", default=True)
    export_resolutions: EnumProperty(
        name="export_resolutions",
        items=[
            ("4096", "4k", "4096x4096"),
            ("2048", "2k", "2048x2048"),
            ("1024", "1k", "1024x1024"),
            ("512", "512", "512x512"),
        ],
        options={"ENUM_FLAG"},
        default={"4096", "2048", "1024", "512"},
    )
    folder_export_base_path: StringProperty(name="folder_export_base_path")


def register():
    # move settings to its own file
    bpy.utils.register_class(SuffixSettings)
    bpy.types.Scene.suffix_settings = bpy.props.PointerProperty(type=SuffixSettings)

    bpy.utils.register_class(GeneralSettings)
    bpy.types.Scene.general_settings = bpy.props.PointerProperty(type=GeneralSettings)

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
    bpy.utils.unregister_class(SuffixSettings)
    del bpy.types.Scene.suffix_settings
    bpy.utils.unregister_class(GeneralSettings)
    del bpy.types.Scene.general_settings
    bpy.utils.unregister_class(PBRTexturesSettings)
    del bpy.types.Scene.pbr_textures_settings
    bpy.utils.unregister_class(DecimateSettings)
    del bpy.types.Scene.decimate_settings

    for item in LAYOUTS:
        bpy.utils.unregister_class(item)

    for operator in OPERATORS:
        bpy.utils.unregister_class(operator)
