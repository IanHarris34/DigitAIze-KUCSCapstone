# Import necessary Blender modules
import bpy
import json
import mathutils

# Define pi as an approximation
pi = 22/7

# Access the pose bones of the current object in Blender
posebones = bpy.context.object.pose.bones

# Function to generate a normalized vector based on given bone names
def genVector(dict, namebot, nametop):
    # Extract coordinates for the bottom and top positions of the bone from the json
    xbot = int(dict[namebot + '_x'])
    ybot = int(dict[namebot + '_y'])
    zbot = int(dict[namebot + '_z'])
    
    xtop = int(dict[nametop + '_x'])
    ytop = int(dict[nametop + '_y'])
    ztop = int(dict[nametop + '_z'])
    
    # Calculate and return the normalized vector between bottom and top positions
    return mathutils.Vector((xtop - xbot, ytop - ybot, ztop - zbot)).normalized()
  
    

#def open_data():
#    with open('C:/Users/annab/Downloads/frame_test.json', 'r') as f:
#        j=json.load(f)
#    return(j)

# Open and load JSON data from the specified file path
with open('C:/Users/annab/Downloads/frame_test.json', 'r') as f:
    j=json.load(f)


#for bone in posebones:
#    bone.rotation_euler.(x y or z)= (rotation in radians)
    
# Loop through each bone in the pose bones of the hand
for bone in posebones:
    # Reset the rotation mode to QUATERNION for each bone
    bone.rotation_mode = 'QUATERNION'
#    bone.rotation_euler.x -= pi/90

    # Obtain the current bone's vector
    curVector = bone.vector
    
    # Initialize a new vector with zero values
    newVector = mathutils.Vector((0, 0, 0))
    
    # Extract the name of the current bone
    boneNameBot = bone.name
    
    # Skip processing for specific bones ('Wrist' and 'palm')
    if boneNameBot == 'Wrist' or boneNameBot == 'palm':
        continue
    else:
        # Extract the numerical part of the bone name and increment it
        val = int(boneNameBot[-1]) + 1
        boneNameTop = boneNameBot[:-1] + str(val)
        
        # Generate a new vector based on the bottom and top bone names
        newVector = genVector(j, boneNameBot, boneNameTop)
    
    # Calculate the rotation difference between the new and current vectors
    rotDiff = newVector.rotation_difference(curVector)
    
    # Apply the rotation difference to the bone's quaternion rotation
    bone.rotation_quaternion.rotate(rotDiff)