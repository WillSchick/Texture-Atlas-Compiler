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


# Raises an error if no jpg or png files were found 
def fileCountError(fileCount):
	if (fileCount == 0):
		raise FileNotFoundError("No files with '.png' or '.jpg' files found! \n Check the readme for more info")


# Returns number of valid image files in Input
def getNumImages(inputPath):
	fileCount = 0
	for filename in os.listdir(inputPath):
		# Only include PNGs and JPGs
		if (filename.lower().endswith('.png') or filename.lower().endswith('.jpg')):
			fileCount += 1
	fileCountError(fileCount)
	return fileCount


def fetchAspectRatioMode():
	with open('config.txt', 'r') as config:
		line = config.readline()
		while ("atlas_aspect_ratio:" not in line):
			line = config.readline()
		line = line.lstrip("atlas_aspect_ratio:")
		return line.strip().upper()

# returns resolution of atlas as a square, in which the dimensions are a power of two
def powerOfTwoAspectRatio(TEXTURE_WIDTH, TEXTURE_HEIGHT, imageCount):
	outputColumns = math.ceil(math.sqrt(imageCount))
	outputRows = math.ceil(math.sqrt(imageCount))
	return (outputColumns * TEXTURE_WIDTH, outputRows * TEXTURE_HEIGHT)

# returns resolution of atlas with a single row
def nByOneAspectRatio(TEXTURE_WIDTH, TEXTURE_HEIGHT, imageCount):
	outputColumns = imageCount
	outputRows = 1
	return (outputColumns * TEXTURE_WIDTH, outputRows * TEXTURE_HEIGHT) 
	
# Returns resolution of atlas with the smallest perimeter 
# Quasi-recursive if the number is prime
def optimalAspectRatio(TEXTURE_WIDTH, TEXTURE_HEIGHT, imageCount, generous):
	outputColumns = imageCount
	outputRows = 1
	
	for possibleRows in range(1, imageCount):
		for possibleColumns in range(1, imageCount):
			if ((possibleColumns * possibleRows) == imageCount and 
				abs(outputColumns - outputRows) > abs(possibleColumns - possibleRows)):
				outputColumns = possibleColumns
				outputRows = possibleRows
	
	# Recursive case: imageCount is prime and therefore could possibly be incredibly long
	if (generous and outputRows <= 1):
		return optimalAspectRatio(TEXTURE_WIDTH, TEXTURE_HEIGHT, imageCount + 1, generous)
	
	return (outputColumns * TEXTURE_WIDTH, outputRows * TEXTURE_HEIGHT)
	

# returns width and height of texture atlas bassed on 
def getAtlasResolution(TEXTURE_WIDTH, TEXTURE_HEIGHT, inputPath):
	imageCount = getNumImages(inputPath)
	mode = fetchAspectRatioMode()
	
	if (mode == "SQUARE"):
		return powerOfTwoAspectRatio(TEXTURE_WIDTH, TEXTURE_HEIGHT, imageCount)
	elif (mode == "LINE"):
		return nByOneAspectRatio(TEXTURE_WIDTH, TEXTURE_HEIGHT, imageCount)
	elif (mode == "OPTIMAL"):
		return optimalAspectRatio(TEXTURE_WIDTH, TEXTURE_HEIGHT, imageCount, False)
	elif (mode == "GENEROUS_OPTIMAL"):
		return optimalAspectRatio(TEXTURE_WIDTH, TEXTURE_HEIGHT, imageCount, True)
	else:
		print("Atlas aspect ratio could not be parsed: " + mode)


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
def makeTextures(TEXTURE_SIZE, inputPath):
	outputTextures = []
	for filename in os.listdir(inputPath):
		if (filename.lower().endswith('.png') or filename.lower().endswith('.jpg')):
			image = Image.open(os.path.join(inputPath, filename))
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


# If directory of string exists in current working directory, return path of that directory
# otherwise return working directory
def getPathIfDirectory(directoryName):
	cwdPath = os.getcwd()
	dirPath = os.path.join(cwdPath, directoryName)
	
	if (os.path.isdir(dirPath)):
		return dirPath
	else:
		return cwdPath

def main():
	# CONSTANTS
	TEXTURE_SIZE = getTextureSize()
	TEXTURE_WIDTH = TEXTURE_SIZE[0]
	TEXTURE_HEIGHT = TEXTURE_SIZE[1]
	
	# Paths
	inputPath = getPathIfDirectory("Input")
	outputPath = getPathIfDirectory("Output")

	# Width of Atlas (power of 2)
	ATLAS_SIZE = getAtlasResolution(TEXTURE_WIDTH, TEXTURE_HEIGHT, inputPath)
	ATLAS_WIDTH = ATLAS_SIZE[0]
	ATLAS_HEIGHT = ATLAS_SIZE[1]
	
	# Create textures array
	textures = []
	textures = makeTextures(TEXTURE_SIZE, inputPath)
	
	# Create atlas
	atlas = generateAtlas(textures, ATLAS_SIZE, TEXTURE_SIZE)
	
	# Save the newly created Atlas
	atlas.save(os.path.join(outputPath, 'Atlas.png'))

main()
