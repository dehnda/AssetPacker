import bpy
from bpy.types import Context, UILayout

from asset_packer.gui.decimate_tab import TabDecimate


# Define main panel for all tabs
class MainPanel(bpy.types.Panel):
    bl_label = "Asset Packer"
    # bl_idname = "PANEL_PT_Asset_Packer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Asset Packer"

    def draw(self, context: Context):
        pass
        # layout = self.layout
