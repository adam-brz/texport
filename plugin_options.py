import bpy


class PluginOptions(bpy.types.PropertyGroup):
    output_directory: bpy.props.StringProperty(
        name="Output directory",
        description="Path to output directory for exported textures",
        subtype="DIR_PATH",
    )
    global_extension: bpy.props.StringProperty(
        name="Default extension",
        description="Extension to apply for all images to export (see supported images: https://docs.blender.org/manual/en/latest/files/media/image_formats.html)",
        default="jpg",
    )
