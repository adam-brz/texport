import os

import bpy


class OBJECT_OT_Refresh(bpy.types.Operator):
    """Refreshes textures list"""

    bl_idname = "object.texport_refresh_images"
    bl_label = "Refresh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        current_texture_names = [
            item.texture_name for item in context.scene.textures_list
        ]
        new_texture_names = [image.name for image in bpy.data.images]

        for image in bpy.data.images:
            if image.name not in current_texture_names:
                new_item = context.scene.textures_list.add()
                new_item.texture_name = image.name

        for image_name in current_texture_names:
            if image_name not in new_texture_names:
                context.scene.textures_list.remove(image_name)

        return {"FINISHED"}


class OBJECT_OT_SelectAll(bpy.types.Operator):
    """Selects all images to export from texture list"""

    bl_idname = "object.texport_select_all"
    bl_label = "Select all"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        select = True

        if all(entry.export for entry in context.scene.textures_list):
            select = False

        for entry in context.scene.textures_list:
            entry.export = select

        return {"FINISHED"}


class OBJECT_OT_ChangeExtensionForAll(bpy.types.Operator):
    """Changes output file extension for each texture in the list"""

    bl_idname = "object.texport_change_output_extension"
    bl_label = "Change extension for all"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for entry in context.scene.textures_list:
            entry.output_format = context.scene.texport_plugin_options.global_extension
        return {"FINISHED"}


class OBJECT_OT_Export(bpy.types.Operator):
    """Exports selected textures to files in chosen format"""

    bl_idname = "object.texport_export"
    bl_label = "Export selected textures"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        options = context.scene.texport_plugin_options
        exported_images = 0

        for entry in context.scene.textures_list:
            if entry.export:
                image = bpy.data.images[entry.texture_name]
                filename = (
                    f"{os.path.splitext(entry.texture_name)[0]}.{entry.output_format}"
                )
                self._export(image, options.output_directory, filename)
                exported_images += 1

        self.report({"INFO"}, f"Exported {exported_images} images.")
        return {"FINISHED"}

    def _export(self, image, output_dir, output_file):
        output_dir = bpy.path.abspath(output_dir or "//")
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(
            output_dir,
            output_file,
        )
        image.save(filepath=output_filename, quality=100)
