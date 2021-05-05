# Created: 5/4/2021
# Made by: Will Schick
# Check Readme for more info on configurations

# Imports:
import os
import math
from PIL import Image

# Reads desired texture resolution from config file
def getTextureSize():
	with open('config.txt', 'r') as config:
		line = config.readline()
		while ("texture_resolution:" not in line):
			line = config.readline()
		line = line.strip("texture_resolution:")
		splitLine = line.split("x")
		return (int(splitLine[0].strip(" ")), int(splitLine[1].strip(" ")))

# Returns number of valid image files in Input
def getNumImages():
	fileCount = 0
	for filename in os.listdir('./Input'):
		# Only include PNGs and JPGs
		if (filename.lower().endswith('.png') or filename.lower().endswith('.jpg')):
			fileCount += 1
	return fileCount
	
# returns width and height of texture atlas bassed on 
def getAtlasResolution(TEXTURE_WIDTH, TEXTURE_HEIGHT):
	imageCount = getNumImages()
	outputColumns = math.ceil(math.sqrt(imageCount))
	outputRows = math.ceil(math.sqrt(imageCount))
	
	return (outputColumns * TEXTURE_WIDTH, outputRows * TEXTURE_HEIGHT)

def resampleParse(mode):
	if (mode == "NEAREST"):
		return Image.NEAREST
	elif (mode == "BICUBIC"):
		return Image.BICUBIC
	elif (mode == "LANCZOS"):
		return Image.LANCZOS
	elif (mode == "HAMMING"):
		return Image.HAMMING
	else:
		print("Resampling mode not found!")
		print("Using BICUBIC as default")
		return Image.BICUBIC


def getResampleMode() :
	with open('config.txt', 'r') as config:
		line = config.readline()
		while ("resample_mode:" not in line):
			line = config.readline()
		line = line.strip("resample_mode:")
		line = line.strip()
		line = line.upper()
		
	return resampleParse(line)
		


# Return an array of resized textures
def makeTextures(TEXTURE_SIZE):
	outputTextures = []
	for filename in os.listdir('./Input'):
		if (filename.lower().endswith('.png') or filename.lower().endswith('.jpg')):
			image = Image.open(os.path.join('Input', filename))
			image = image.resize(TEXTURE_SIZE, resample=getResampleMode())
			outputTextures.append(image)
	return outputTextures

# Takes in textures and returns an atlas
def generateAtlas(textures, ATLAS_SIZE, TEXTURE_SIZE):
	atlas = Image.new("RGB", ATLAS_SIZE) 

	# Paste textures onto the atlas
	widthOffset = 0
	heightOffset = 0
	for textureImage in textures:
		atlas.paste(textureImage, (widthOffset, heightOffset))
		widthOffset += TEXTURE_SIZE[0]
		if (widthOffset >= ATLAS_SIZE[0]):
			widthOffset = 0
			heightOffset += TEXTURE_SIZE[1]
			
	return atlas

def main():
	# CONSTANTS
	TEXTURE_SIZE = getTextureSize()
	TEXTURE_WIDTH = TEXTURE_SIZE[0]
	TEXTURE_HEIGHT = TEXTURE_SIZE[1]

	# Width of Atlas (power of 2)
	ATLAS_SIZE = getAtlasResolution(TEXTURE_WIDTH, TEXTURE_HEIGHT)
	ATLAS_WIDTH = ATLAS_SIZE[0]
	ATLAS_HEIGHT = ATLAS_SIZE[1]
	
	# Create textures array
	textures = []
	textures = makeTextures(TEXTURE_SIZE)
	
	# Create atlas
	atlas = generateAtlas(textures, ATLAS_SIZE, TEXTURE_SIZE)
	
	# Save the newly created Atlas
	atlas.save(os.path.join('Output', 'Atlas.png'))
	
main()
