sed 's/casioplot.casioplot_settings.get("width")/128/g' imagedriverdev.py > tmpfile
sed -i '/casioplot_settings/d' tmpfile
sed -i "/from PIL/d" tmpfile
sed -i "/Image/d" tmpfile
sed $'s/$/\r/' tmpfile > releases/imagedriver.py
rm tmpfile