# Texture-Atlas-Compiler
A script used to compile multiple texture image files into an Atlas primarily for use during low-poly 3d modeling

# Set-up
Texture-Atlas-Compiler uses PIL, which can be downloaded with pip by using:
  ```
  pip install Pillow
  ```

# Usage
Run the script using Python's interpreter:
  ```
  py Texture-Atlas-Compiler
  ```
This will take .png and .jpg files stored in the "Input" directory, and generate a formatted texture atlas which is then placed in the "Output" directory. If no "Input" or "Output" directory is found, the script will instead take from the current working directory, and create an atlas image in the current working directory as well.

# Configuration file
The "config.txt" file contains the following settings for the Texture-Atlas-Compiler:
  - texture_resolution: `int` x `int`
    - The resolution of each texture. Textures above or below this resolution will be scaled up or down.  
  - resample_mode: `mode`
    - The mode for resampling when resizing each texture.
    - Modes: NEAREST , BICUBIC , LANCZOS , HAMMING 
  - atlas_aspect_ratio: `mode`
	- The aspect ratio of the atlas to be generated
	- Modes:
		- SQUARE : (The atlas's dimensions will always be a power of two)
		- LINE : (The atlas will have a height of one texture, and will expand only by width)
		- OPTIMAL : (The atlas will generate only enough space as needed to fit all textures)
		