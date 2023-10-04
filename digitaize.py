import sys, os
import torch
from PIL import Image
import torchvision.transforms as transforms

# Check that we have enough arguments
if( len( sys.argv ) < 2 ):
	# Print command usage and terminate if there is not enough arguments
	print( "Usage: python digitaize.py [imageFileName]" )
	os._exit( 1 )

img = Image.open( sys.argv[ 1 ] )

# Create definition for transform
# Transform converts image file to tensor
imgToTensorTransform = transforms.Compose(
	[
	transforms.PILToTensor()
	]
)

# Apply the transformation on the image
img_tensor = imgToTensorTransform( img )

# Print the tensors for the demo
print( img_tensor )