import os
from pathlib import Path

import bpy
from bpy.types import Operator, Context, Object
from bpy.props import StringProperty, BoolProperty, FloatProperty
from bpy_extras.io_utils import ImportHelper

# TODO: make this suffixes settable


class ImportFbxOperator(Operator, ImportHelper):
    bl_idname = "asset_packer.import_fbx"
    bl_label = "Import FBX"
    filename_ext = ".fbx"

    suffixes: dict = {}
    # TODO: move this to the settings group
    filepath: StringProperty(
        name="File Path",
        description="File path used for importing FBX",
        subtype="FILE_PATH",
    )

    def execute(self, context: Context):
        self.suffixes = {
            "albedo": context.scene.suffix_settings.albedo,
            "ao": context.scene.suffix_settings.ao,
            "displacement": context.scene.suffix_settings.displacement,
            "metallic": context.scene.suffix_settings.metallic,
            "normal": context.scene.suffix_settings.normal,
            "roughness": context.scene.suffix_settings.roughness,
            "emission": context.scene.suffix_settings.emission,
        }

        # Check if a file path is provided
        if self.filepath:
            # Import the FBX file
            bpy.ops.import_scene.fbx(filepath=self.filepath)
            self.report({"INFO"}, f"FBX file '{self.filepath}' imported successfully")

            # set export base path for export textures operator
            context.scene.pbr_textures_settings.folder_export_base_path = (
                Path(self.filepath).parent.absolute().as_posix()
            )

            obj: Object = bpy.context.selected_objects[0]
            if obj:
                self.create_pbr_material(obj, context)
                # TODO: refactor thats ugly and make it settable?
                lod_1 = self.copy_object(obj)
                lod_1.location.y += 2.0
                lod_2 = self.copy_object(lod_1)
                lod_2.location.y += 2.0
                lod_3 = self.copy_object(lod_2)
                lod_3.location.y += 2.0
                self.decimate(
                    lod_1, context.scene.decimate_settings.lod_ratio_1, context
                )
                self.decimate(
                    lod_2, context.scene.decimate_settings.lod_ratio_2, context
                )
                self.decimate(
                    lod_3, context.scene.decimate_settings.lod_ratio_3, context
                )

                # assign objects for export
                context.scene.decimate_settings.lod_mesh_0 = obj
                context.scene.decimate_settings.lod_mesh_1 = lod_1
                context.scene.decimate_settings.lod_mesh_2 = lod_2
                context.scene.decimate_settings.lod_mesh_3 = lod_3

        else:
            self.report({"ERROR"}, "No file selected")

        return {"FINISHED"}

    def decimate(self, obj, ratio, context: Context):
        self.select_object(obj)
        if obj.type == "MESH":
            modifier = obj.modifiers.new(name="Decimate", type="DECIMATE")
            modifier.ratio = ratio
            # TODO make this settable with a checkbox
            if context.scene.general_settings.decimate_on_import:
                bpy.ops.object.modifier_apply(modifier="Decimate")
                self.report({"INFO"}, "Decimate Modifier applied to the imported mesh.")
        else:
            self.report({"ERROR"}, "The selected object is not a mesh.")

    def select_object(self, obj):
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

    def copy_object(self, obj):
        duplicate = obj.copy()
        duplicate.data = obj.data.copy()
        bpy.context.collection.objects.link(duplicate)
        return duplicate

    def create_pbr_material(self, obj, context: Context):
        self.select_object(obj)
        if obj.material_slots and obj.material_slots[0].material:
            material = obj.material_slots[0].material
        else:
            material = bpy.data.materials.new(name="PBR_Material")
            obj.data.materials.append(material)

        # Ensure the material has a node tree and switch to node editor
        if material.use_nodes:
            tree = material.node_tree
        else:
            material.use_nodes = True
            tree = material.node_tree

        # Clear existing nodes
        for node in tree.nodes:
            tree.nodes.remove(node)

        # Create Texture Coordinate node
        tex_coord_node = tree.nodes.new(type="ShaderNodeTexCoord")
        tex_coord_node.location = (-1400, 0)

        # Create Mapping node
        mapping_node = tree.nodes.new(type="ShaderNodeMapping")
        mapping_node.location = (-1200, 0)
        tree.links.new(tex_coord_node.outputs["UV"], mapping_node.inputs["Vector"])

        # create  pbr shader
        principled_node = tree.nodes.new(type="ShaderNodeBsdfPrincipled")
        principled_node.location = (0, 0)

        # Create Displacement node
        displacement_node = tree.nodes.new(type="ShaderNodeDisplacement")
        displacement_node.location = (200, -400)

        # Create Material Output node
        output_node = tree.nodes.new(type="ShaderNodeOutputMaterial")
        output_node.location = (400, 0)
        tree.links.new(
            displacement_node.outputs["Displacement"],
            output_node.inputs["Displacement"],
        )
        tree.links.new(
            principled_node.outputs["BSDF"],
            output_node.inputs["Surface"],
        )

        # create multiply for ao and basecolor
        multiply_node = tree.nodes.new(type="ShaderNodeMixRGB")
        multiply_node.blend_type = "MULTIPLY"
        multiply_node.location = (-400, 200)
        tree.links.new(
            multiply_node.outputs["Color"], principled_node.inputs["Base Color"]
        )

        # Create nodes for each texture type
        texture_nodes = {}
        # TODO: make the path relative to the mesh maybe and setable in settings?
        # or maybe selectable too?
        base_path = Path(self.filepath).parent.joinpath(
            context.scene.general_settings.import_folder
        )
        # TODO make error message
        if not os.path.exists(base_path):
            return
        for filename in self.files_in_folder(base_path):
            self.report({"INFO"}, f"filename: {filename}")
            for tex_type, suffix in self.suffixes.items():
                if suffix in filename:
                    texture_node = tree.nodes.new(type="ShaderNodeTexImage")
                    texture_node.image = bpy.data.images.load(
                        os.path.join(base_path, filename)
                    )
                    texture_node.location = (
                        -800,
                        200 - list(self.suffixes.keys()).index(tex_type) * 300,
                    )  # Adjust node positions
                    texture_nodes[tex_type] = texture_node

        # assign current loaded textures to export settings
        if "albedo" in texture_nodes.keys():
            context.scene.pbr_textures_settings.albedo = texture_nodes["albedo"].image
        if "ao" in texture_nodes.keys():
            context.scene.pbr_textures_settings.ao = texture_nodes["ao"].image
        if "displacement" in texture_nodes.keys():
            context.scene.pbr_textures_settings.displacement = texture_nodes[
                "displacement"
            ].image
        if "metallic" in texture_nodes.keys():
            context.scene.pbr_textures_settings.metallic = texture_nodes[
                "metallic"
            ].image
        if "normal" in texture_nodes.keys():
            context.scene.pbr_textures_settings.normal = texture_nodes["normal"].image
        if "roughness" in texture_nodes.keys():
            context.scene.pbr_textures_settings.roughness = texture_nodes[
                "roughness"
            ].image
        if "emission" in texture_nodes.keys():
            context.scene.pbr_textures_settings.emission = texture_nodes[
                "emission"
            ].image

        # link all maps
        for tex_type, node in texture_nodes.items():
            # link mapping with texture nodes
            tree.links.new(mapping_node.outputs["Vector"], node.inputs["Vector"])

            if tex_type == "albedo":
                tree.links.new(node.outputs["Color"], multiply_node.inputs["Color1"])
            elif tex_type == "ao":
                tree.links.new(node.outputs["Color"], multiply_node.inputs["Color2"])
            elif tex_type == "displacement":
                tree.links.new(
                    node.outputs["Color"], displacement_node.inputs["Height"]
                )
                tree.links.new(
                    displacement_node.outputs["Displacement"],
                    output_node.inputs["Displacement"],
                )
            elif tex_type == "normal":
                normal_map_node = tree.nodes.new(type="ShaderNodeNormalMap")
                normal_map_node.location = (-400, 0)
                tree.links.new(node.outputs["Color"], normal_map_node.inputs["Color"])
                tree.links.new(
                    normal_map_node.outputs["Normal"], principled_node.inputs["Normal"]
                )
            elif tex_type == "roughness":
                tree.links.new(
                    node.outputs["Color"], principled_node.inputs["Roughness"]
                )
            elif tex_type == "emission":
                tree.links.new(
                    node.outputs["Color"], principled_node.inputs["Emission Color"]
                )

    def files_in_folder(self, path):
        if os.path.exists(path):
            # Get all files in the folder
            return [
                f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
            ]
        return None
