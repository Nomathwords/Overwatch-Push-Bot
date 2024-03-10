@echo off
cd shop_images
magick montage *.jpg -background black -tile 8x result.png
magick convert result.png -resize 2000% result.png