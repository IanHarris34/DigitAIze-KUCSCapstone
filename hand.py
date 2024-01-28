import bpy
import json
import mathutils

pi = 22/7
posebones = bpy.context.object.pose.bones

def genVector(dict, namebot, nametop):
    xbot = int(dict[namebot + '_x'])
    ybot = int(dict[namebot + '_y'])
    zbot = int(dict[namebot + '_z'])
    
    xtop = int(dict[nametop + '_x'])
    ytop = int(dict[nametop + '_y'])
    ztop = int(dict[nametop + '_z'])
    
    return(mathutils.Vector((xtop-xbot, ytop-ybot, ztop-zbot)).normalized())
    
    

#def open_data():
#    with open('C:/Users/annab/Downloads/frame_test.json', 'r') as f:
#        j=json.load(f)
#    return(j)

with open('C:/Users/annab/Downloads/frame_test.json', 'r') as f:
    j=json.load(f)


#for bone in posebones:
#    bone.rotation_euler.(x y or z)= (rotation in radians)
    
for bone in posebones:
    posebones = bpy.context.object.pose.bones
    bone.rotation_mode = 'QUATERNION' #is QUATERNINON by default, we don't want that, this is reset EVERY time you open blender
#    bone.rotation_euler.x -= pi/90

    curVector = bone.vector
    newVector = mathutils.Vector((0,0,0))

    boneNameBot = bone.name
    
    if(boneNameBot == 'Wrist'): continue
    elif(boneNameBot == 'palm'): continue
    else: 
        val = int(boneNameBot[-1]) + 1
        boneNameTop = boneNameBot[:-1] + str(val)
        
        newVector = genVector(j, boneNameBot, boneNameTop)
    
    rotDiff = newVector.rotation_difference(curVector)
    
    bone.rotation_quaternion.rotate(rotDiff)