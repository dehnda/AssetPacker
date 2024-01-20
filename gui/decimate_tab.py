import bpy
from bpy.types import Panel


class AP_PT_TabDecimate(Panel):
    bl_parent_id = "AP_PT_MainPanel"
    bl_idname = "TAB_PT_Decimate"
    bl_label = "Decimate"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Asset Packer"

    def draw(self, context):
        # Decimate
        layout = self.layout

        layout.operator("asset_packer.import_fbx")
        layout.prop(context.scene.decimate_settings, "lod_ratio_1", text="LOD 1 ratio")
        layout.prop(context.scene.decimate_settings, "lod_ratio_2", text="LOD 2 ratio")
        layout.prop(context.scene.decimate_settings, "lod_ratio_3", text="LOD 3 ratio")
