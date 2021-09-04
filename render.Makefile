SHELL		:= /bin/zsh

include config.Makefile

DATA_PREFIX	:= ${PREFIX}/params
LOG_PREFIX	:= ${PREFIX}/log
FRAMES_DATA	:= ${DATA_PREFIX}/frames.ndjson
SCENE_DATA	:= ${DATA_PREFIX}/meta.ndjson

SELF		:= $(realpath $(dir $(realpath $(firstword $(MAKEFILE_LIST)))))

all :
	rm -rf ${PREFIX}
	mkdir -p ${PREFIX}/log
	${MAKE} -f ${firstword ${MAKEFILE_LIST}} params
	${MAKE} -f $(firstword ${MAKEFILE_LIST}) all-renders


include blender.render.Makefile
# include any_other.render.Makefile

## Create Params
## ====================================================

params : ${DATA_PREFIX} ${LOG_PREFIX} ${FRAMES_DATA} ${SCENE_DATA}

${DATA_PREFIX} ${LOG_PREFIX} :
	pwd && \
	[ ! -d "$@" ] && mkdir -p $@ && \
	echo $@

${FRAMES_DATA} : ${LOG_PREFIX}
	cd ${SELF} ;				\
	python -m params -o $@			\
	  create-frames				\
	  ${NUM_FRAMES} ${NUM_KEYFRAMES}	\
	  2>&1					\
	  | tee -a ${LOG_PREFIX}/create-frames.log

${SCENE_DATA} : ${LOG_PREFIX}
	cd ${SELF} ;				\
	python -m params -v -o  $@		\
	  create-scene				\
	  2>&1					\
	  | tee -a ${PREFIX}/log/create-scene.log

## Create Renders
## ====================================================

all-renders : blender-renders
# all-renders : blender-renders any_other-renders
# # where any_other-renders is defined in any_other.render.Makefile

.PHONY : all params all-renders 
