import os
from pathlib import Path

import bpy
from bpy.types import Operator, Context, Image


class TextureExporterOperator(Operator):
    bl_idname = "asset_packer.pbr_textures_export"
    bl_label = "Export Textures"
    texture_names = [
        "base_color",
        "metallic",
        "normal",
        "displacement",
        "emission",
        "ao",
        "roughness",
        "opacity",
    ]
    resolutions = ["4k", "2k", "1k", "512"]

    def execute(self, context: Context):
        settings = context.scene.pbr_textures_settings
        self.resize_and_save_image(
            settings.base_color, settings.folder_export_path, 512, context
        )
        # TODO check if textures are set
        # context.scene.pbr_textures_settings.ao = texture_nodes["ao"]
        # context.scene.pbr_textures_settings.displacement = texture_nodes["displacement"]
        # context.scene.pbr_textures_settings.metallic = texture_nodes["metallic"]
        # context.scene.pbr_textures_settings.normal = texture_nodes["normal"]
        # context.scene.pbr_textures_settings.roughness = texture_nodes["roughness"]
        # context.scene.pbr_textures_settings.emission = texture_nodes["emission"]
        return {"FINISHED"}

    def resize_and_save_image(
        self, image: Image, target_path, resolution, context: Context
    ):
        try:
            # TODO export path checking
            # TODO different solutions
            bpy.context.area.type = "IMAGE_EDITOR"
            bpy.context.area.spaces.active.image = image
            bpy.ops.image.resize(size=(resolution, resolution))
            image.file_format = "PNG"
            path = (
                context.scene.pbr_textures_settings.folder_export_base_path
                + "/"
                + target_path
                + "/test.png"
            )
            image.save_render(filepath=path)
            bpy.data.images.remove(image)
        except Exception as e:
            print(f"Error resizing image: {e}")
            return False
        bpy.context.area.type = "VIEW_3D"
        return True
