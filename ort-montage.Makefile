DIST := dist

AXES := X_Y X_-Y -X_Y -X_-Y
AXES += X_Z X_-Z -X_Z -X_-Z
AXES += Y_Z Y_-Z -Y_Z -Y_-Z
AXES += Y_X Y_-X -Y_X -Y_-X
AXES += Z_Y Z_-Y -Z_Y -Z_-Y
AXES += Z_X Z_-X -Z_X -Z_-X

IMAGES := $(shell \
	cd ${DIST}/$(firstword ${AXES})/renders ; \
	find . -iname '*.png' \
	| cut -d/ -f2,4 \
	| cut -d. -f1 \
	| tr '/' '-')

img-src = $(shell echo $2 \
	| sed -E 's,(.*)-(.*),${DIST}/$1/renders/\1/r_contour/\2.png,')

all : ${DIST}/ort-montages ${IMAGES:%=${DIST}/ort-montages/%.png}

${DIST}/ort-montages/%.png :
	montage \
	  $(foreach AXIS,${AXES},$(call img-src,${AXIS},$*) ) \
	  -tile 4x -geometry +2+2 -background SlateGray \
	  $@

${DIST}/ort-montages :
	[ -d $@ ] || mkdir -p $@
