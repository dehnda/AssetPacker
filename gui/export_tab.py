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

        layout.prop(
            context.scene.pbr_textures_settings, "export_lods", text="Export LODs"
        )
        layout.prop(
            context.scene.pbr_textures_settings,
            "folder_export_path",
            text="Export Dir",
        )
        layout.prop(
            context.scene.pbr_textures_settings,
            "export_resolutions",
            text="Resolutions",
        )
        layout.separator()
        layout.operator("asset_packer.pbr_textures_export")
