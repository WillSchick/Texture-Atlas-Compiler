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
This will take .png and .jpg files stored in the "Input" directory, and generate a formatted texture atlas which is then placed in the "Output" directory.  

# Configuration file
The "config.txt" file contains the foolowing settings for the Texture-Atlas-Compiler:
  - texture_resolution: `int` x `int`
    - The resolution of each texture. Textures above or below this resolution will be scaled up or down.  
  - resample_mode: `mode`
    - The mode for resampling when resizing each texture.
    - Modes: NEAREST , BICUBIC , LANCZOS , HAMMING 
