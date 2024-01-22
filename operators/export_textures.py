import bpy
from bpy.types import Operator, Context


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
        pass

    def resize_and_save_image(source_path, target_path, resolution):
        try:
            img = bpy.data.images.load(source_path)
            bpy.context.area.type = "IMAGE_EDITOR"
            bpy.context.area.spaces.active.image = img
            bpy.ops.image.resize(size=(resolution, resolution))
            img.file_format = "PNG"
            img.save_render(filepath=target_path)
            bpy.data.images.remove(img)
        except Exception as e:
            print(f"Error resizing image: {e}")
            return False
        return True
