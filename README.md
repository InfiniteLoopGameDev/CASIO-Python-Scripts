CASIO Python Scripts
====================

Python CCITT Decoder for Casio
------------------------------

This is the main attraction as it lets you store images in small file-sizes.

### Creating and processing the image

Create an image use the dimensions 128 x 64 (The program should be able to handle 
smaller dimensions). The export it to PNG or JPEG. Using 
[Image Magick](https://imagemagick.org) convert the image to a CCITT Group 4 
compressed image. Use the following command:  

    magick example.png -monochrome -compress Group4 example.tiff  
Then using the `ccittconvert.py` script in the ccitt folder you strip the file of 
all metadata and output it in a `.bin` file. Make use of the following command:  

    python ./ccitt/ccittconvert.py example.tiff example.bin  
Note: the script can also take a single argument, outputted file having the same 
name as the inputted file  
The resulting file can then be made into a hexadecimal string using the following
command:

    echo $(hexdump -ve '1/1 "%.2X"' example.bin)
Note: the previous command may output something different on macOS and does not
work on Windows' CMD or PowerShell

### Transferring to the calculator

Download the `ccittdriver.py` from 
[here](https://github.com/InfiniteLoopGameDev/CASIO-Python-Scripts/releases) 
or make it using the `ccitt-driver-release.sh` (for Linux / macOS with GNU sed only)  
Plug-in your fx-9860G in USB Flash Mode. Copy the `ccitt` folder to the calculator 
(`ccittconvert.py, ccitt-driver-release.sh, ccittdriverdev.py` can be omitted). 
Copy the `ccittdriver.py` file in the folder as well.  
Create an empty file called `images.py` in the same folder. Add the following 
into the file:  

    your_image_name = "hexadecimal_string_output_here"  
Edit the `ccittdriver.py` file, replacing the `your_image_name` with the name 
of the image input into the previous file. You should now have a file structure 
like this:  

    ROOT  
    └── ccitt  
        ├── bitbuffer.py  
        ├── ccittcodes.py  
        ├── ccittdecoder.py  
        ├── ccittdriver.py  
        ├── ccittmodes.py  
        ├── image.py  
        └── modecodes.py  
Now running the `ccittdriver.py` calculator should display your image (give a take 
a few tens of seconds). Note: the calculator might throw a `MemoryError` message
if the image is too large

<!-- 
    TODO: use a .zip
    TODO: describe new ccittrelease.py
    TODO: credit plaisted/CCITTFaxDecode <- GIGA CHAD
-->