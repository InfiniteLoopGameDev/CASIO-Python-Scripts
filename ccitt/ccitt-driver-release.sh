sed 's/casioplot.casioplot_settings.get("width")/128/g' ccitt/ccittdriverdev.py > tmpfile
sed -i '/casioplot_settings/d' tmpfile
sed -i "/from PIL/d" tmpfile
sed -i "/Image/d" tmpfile
sed -i "/__name__/d" tmpfile
sed -i "s/    //" tmpfile
sed -i "s=../==" tmpfile
sed $'s/$/\r/' tmpfile > releases/ccittdriver.py
rm tmpfile