import os
from pathlib import Path

import bpy
from bpy.types import Operator, Context, Image


class TextureExporterOperator(Operator):
    bl_idname = "asset_packer.pbr_textures_export"
    bl_label = "Export Textures"

    def export_texture(self, texture: Image, context: Context):
        if texture == None:
            return
        settings = context.scene.pbr_textures_settings
        for res in settings.export_resolutions:
            self.resize_and_save_image(
                texture, settings.folder_export_path, int(res), context
            )

    def execute(self, context: Context):
        # TODO check if textures are set
        settings = context.scene.pbr_textures_settings
        target_path = settings.folder_export_path

        self.export_lods(context, target_path)

        self.export_texture(settings.albedo, context)
        self.export_texture(settings.ao, context)
        self.export_texture(settings.displacement, context)
        self.export_texture(settings.metallic, context)
        self.export_texture(settings.normal, context)
        self.export_texture(settings.roughness, context)
        self.export_texture(settings.emission, context)

        return {"FINISHED"}

    def export_lods(self, context: Context, target_path: str):
        lods = [
            context.scene.decimate_settings.lod_mesh_0,
            context.scene.decimate_settings.lod_mesh_1,
            context.scene.decimate_settings.lod_mesh_2,
            context.scene.decimate_settings.lod_mesh_3,
        ]
        path = (
            context.scene.pbr_textures_settings.folder_export_base_path
            + "/"
            + target_path
        )
        if not os.path.exists(path):
            os.mkdir(path)
        for i, lod in enumerate(lods):
            filename = path + "lod_" + str(i + 1) + ".fbx"
            lod.select_set(True)
            bpy.ops.export_scene.fbx(filepath=filename)
            bpy.ops.object.select_all(action="DESELECT")

    def resize_and_save_image(
        self, image: Image, target_path: str, resolution: int, context: Context
    ):
        try:
            # TODO export path checking
            # TODO different solutions
            bpy.context.area.type = "IMAGE_EDITOR"
            bpy.context.area.spaces.active.image = image
            bpy.ops.image.resize(size=(resolution, resolution))
            image.file_format = "PNG"
            filename = (
                Path(image.filepath).stem
                + "_"
                + str(resolution)
                + "_"
                + Path(image.filepath).suffix
            )
            path = (
                context.scene.pbr_textures_settings.folder_export_base_path
                + "/"
                + target_path
                + "textures/"
                + filename
            )
            image.save_render(filepath=path)
            # bpy.data.images.remove(image)
        except Exception as e:
            print(f"Error resizing image: {e}")
            return False
        bpy.context.area.type = "VIEW_3D"
        return True
