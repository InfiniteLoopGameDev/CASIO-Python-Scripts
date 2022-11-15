#!/bin/bash

sed 's/casioplot.casioplot_settings.get("width")/128/g' ccitt/ccittdriverdev.py > tmpfile
sed -i '/import ccittdecoder/c\import ccittdecoder\nfrom image import your_image_name as img_data' tmpfile
sed -i '/file_data = open(*/c\file_data = bytes([int(img_data[i:i + 2],16) for i in range(0, len(img_data), 2)])' tmpfile
sed -i '/casioplot_settings/d' tmpfile
sed -i "/from PIL/d" tmpfile
sed -i "/Image/d" tmpfile
sed -i "/__name__/d" tmpfile
sed -i "s/    //" tmpfile
sed -i "s=../==" tmpfile
sed $'s/$/\r/' tmpfile > releases/ccittdriver.py
rm tmpfile