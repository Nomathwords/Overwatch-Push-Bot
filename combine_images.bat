@echo off
cd shop_images
magick montage *.jpg -background black -tile 8x br_shop.png
magick convert br_shop.png -resize 2000% br_shop.png