#!/bin/bash

ffmpeg -framerate 40 -pattern_type glob -i 'snaps/*.png' -c:v libx264 -pix_fmt yuv420p res.mp4
