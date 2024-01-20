import bpy
from bpy.types import Panel


class AP_PT_ExportTab(Panel):
    bl_parent_id = "AP_PT_MainPanel"
    bl_idname = "TAB_PT_ExportTextures"
    bl_label = "Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Asset Packer"

    def draw(self, context):
        # Decimate
        layout = self.layout

        # layout.operator("asset_packer.pbr_textures_export")
        # layout.prop(context.scene.decimate_settings, "lod_ratio_1", text="LOD 1 ratio")
        # layout.prop(context.scene.decimate_settings, "lod_ratio_2", text="LOD 2 ratio")
        # layout.prop(context.scene.decimate_settings, "lod_ratio_3", text="LOD 3 ratio")
