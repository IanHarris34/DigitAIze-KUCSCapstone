import bpy  # Import the Blender Python module
from bpy_extras.io_utils import ImportHelper  # Import a helper class for file import

# Define a panel class for the file selection demo
class FileSelectDemoPanel(bpy.types.Panel):
    bl_idname = "PT_FileSelectDemoPanel"  # Unique identifier for the panel
    bl_label = "File Select Demo"  # Label displayed in the UI
    bl_space_type = 'VIEW_3D'  # Panel space type
    bl_region_type = 'UI'  # Panel region type
    bl_category = 'Custom'  # Panel category

    # Method to draw the panel UI
    def draw(self, context):
        layout = self.layout  # Get the panel layout

        # Display a row with the "File Path:" label, file path, and a button for the file icon
        row = layout.row(align=True)
        row.label(text="File Path:")
        row.prop(context.scene, "file_path", text="")
        row.operator("file.select_demo", text="", icon='FILE_FOLDER')

# Define an operator class for the file selection demo
class FileSelectDemo(bpy.types.Operator, ImportHelper):
    bl_idname = "file.select_demo"  # Unique identifier for the operator
    bl_label = "Select File"  # Label displayed in the UI
    filename_ext = ""  # File extension filter

    # Method to execute the operator
    def execute(self, context):
        context.scene.file_path = self.filepath  # Set the selected file path in the scene
        return {'FINISHED'}  # Return a flag indicating the operation is finished

    # Method to invoke the operator
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)  # Add the file selection dialog
        return {'RUNNING_MODAL'}  # Return a flag indicating the operator is running

# Register the classes and properties
def register():
    bpy.types.Scene.file_path = bpy.props.StringProperty(name="File Path", description="Selected File Path", default="")
    bpy.utils.register_class(FileSelectDemo)
    bpy.utils.register_class(FileSelectDemoPanel)

# Unregister the classes and properties
def unregister():
    bpy.utils.unregister_class(FileSelectDemo)
    bpy.utils.unregister_class(FileSelectDemoPanel)
    del bpy.types.Scene.file_path

# Entry point to register the classes and properties
if __name__ == "__main__":
    register()
