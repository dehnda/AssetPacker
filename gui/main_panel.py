import bpy
from bpy.types import Context, UILayout


# Define main panel for all tabs
class AP_PT_MainPanel(bpy.types.Panel):
    bl_label = "Asset Packer"
    # bl_idname = "PANEL_PT_Asset_Packer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Asset Packer"

    # TODO duplicate move out
    texture_names = [
        "base_color",
        "metallic",
        "normal",
        "emission",
        "displacement",
        "ao",
        "roughness",
        "opacity",
    ]

    def draw(self, context: Context):
        layout = self.layout
        layout.label(text="Import Settings")
        row = layout.row()
        row.separator()
        box = row.box()
        box.prop(
            context.scene.general_settings,
            "import_folder",
            text="Texture Path",
        )
        box.separator()
        box.prop(
            context.scene.general_settings,
            "decimate_on_import",
            text="Decimate LODs on import automatically",
        )
        box.separator()
        box.label(text="Suffix Settings")
        for name in self.texture_names:
            box.prop(context.scene.suffix_settings, name, text=name)
