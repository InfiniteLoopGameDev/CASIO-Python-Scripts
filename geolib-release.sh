sed 's/casioplot.casioplot_settings.get("width")/128/g' geolibdev.py > tmpfile
sed -i '/casioplot_settings/d' tmpfile
sed -i "/from PIL/d" tmpfile
sed -i "/Image/d" tmpfile
sed -i "/__name__/Q" tmpfile
sed $'s/$/\r/' tmpfile > releases/geolib.py
rm tmpfile