#!/bin/bash
# use feh to update wallpaper
# exemple: wallpaper.sh ~/Pictures/Wallpapers 10m
while true
do
	feh -z --bg-fill $1
	sleep $2
done
