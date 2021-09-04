PREFIX			:= dist

KEYS_FOLDER		:= ${PREFIX}/keys
RENDERS_FOLDER		:= ${PREFIX}/renders
SUMMARY_FOLDER		:= ${PREFIX}/summary

NUM_KEYS		:= 8

NUM_FRAMES		:= 5
NUM_KEYFRAMES		:= 3

STYLES			:= contour gnomon 
STYLES			+= highlights midtones shades shadow
STYLES			+= sketch sketch_no_free diffuse
STYLES			+= sketch_geom sketch_geom_no_free

## Summary
## -----------------------------------------------------

CRONTAB			:= fcrontab
COUNT_FILE		:= ${PREFIX}/count

FIND_NUM_PRIMITIVES	:= 3
SUMMARY_NUM_SAMPLES	:= 32
SMY_L0_MONTAGE_OPTIONS	:= -background snow -tile 1x -geometry +1+1
SMY_L1_MONTAGE_OPTIONS	:= -background snow3 -tile x1 -geometry +1+1



## Where am i
SELF			:= $(realpath $(dir $(realpath $(firstword $(MAKEFILE_LIST)))))

