#!/bin/bash

cd S12-L
./run.sh S12-L
cd ..
~/workspace/photo_density/build/Release/./photo_dens S12-L/inps/settings.inp S12-L/dumps/len/ density/
./plot-c.py
./make_movie.sh


