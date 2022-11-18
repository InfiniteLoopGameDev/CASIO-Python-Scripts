CASIO Python Scripts
====================

Python CCITT Decoder for Casio
------------------------------

This is the main attraction as it lets you store images in small file-sizes.

### Creating and processing the image

Create an image use the dimensions 128 x 64 (The program should be able to handle 
smaller dimensions). The export it to PNG or JPEG. Using [Image Magick](https://imagemagick.org) convert the image to a CCITT Group 4 compressed image. Use the following command:  

    magick example.png -monochrome -compress Group4 example.tiff  

Then using the `ccittconvert.py` script in the ccitt folder you strip the file of all metadata and output its hexadecimal interpretation. Make use of the following command:  

    python ./ccitt/ccittconvert.py example.tiff -H   

Note: the script can also output to a binary file. See `python ./ccitt/ccittconvert.py -h` for more info

### Transferring to the calculator

Download the `ccitt.zip` from [here](https://github.com/InfiniteLoopGameDev/CASIO-Python-Scripts/releases). Then extract the archive.  
Plug-in your fx-9860G in USB Flash Mode. Copy the `ccitt` folder to the calculator.   
Note this can also be made from source using the `ccittrelease.py` script
Change the following in the `image.py` file:  

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

Credits
-------

plaisted for creating [a GO version of CCITTFaxDecode](github.com/plaisted/CCITTFaxDecode) which this is based on  
uniwix for creating [a version of casioplot that is on PyPI](github.com/uniwix/casioplot) which makes development much easier