import os

import bpy


class OBJECT_OT_Refresh(bpy.types.Operator):
    """Refreshes textures list"""

    bl_idname = "object.texport_refresh_images"
    bl_label = "Refresh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.scene.textures_list.clear()

        for image in bpy.data.images:
            if image.resolution.x > 0 and image.resolution.y > 0:
                new_item = context.scene.textures_list.add()
                new_item.texture_name = image.name

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
        output_dir = self._normalize_output_dir(options.output_directory)
        exported_images = 0

        try:
            for entry in context.scene.textures_list:
                if entry.export and entry.texture_name in bpy.data.images:
                    image = bpy.data.images[entry.texture_name]
                    filename = f"{os.path.splitext(entry.texture_name)[0]}.{entry.output_format}"
                    self._export(image, output_dir, filename)
                    exported_images += 1
        except Exception as e:
            self.report({"ERROR"}, f"{e}")

        self.report({"INFO"}, f"Exported {exported_images} images to '{output_dir}'.")
        return {"FINISHED"}

    def _export(self, image, output_dir, output_file):
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(
            output_dir,
            output_file,
        )
        image.save(filepath=output_filename, quality=100)

    def _normalize_output_dir(self, output_dir):
        return bpy.path.abspath(output_dir or "//") or os.path.abspath(".")
