import bpy
pi = 22/7
posebones = bpy.context.object.pose.bones

#for bone in posebones:
#    bone.rotation_euler.(x y or z)= (rotation in radians)
    
for bone in posebones:
    posebones = bpy.context.object.pose.bones
    bone.rotation_mode = 'XYZ' #is QUATERNINON by default, we don't want that, this is reset EVERY time you open blender
    bone.rotation_euler.x -= pi/90
