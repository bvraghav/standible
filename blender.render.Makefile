
BLENDER_RENDER_SCRIPT	:= ${SELF}/blender_run_render.py

blender-renders : ${STYLES:%=${PREFIX}/r_%} \

${PREFIX}/r_% :
	[ ! -d "$@" ] && mkdir -p $@
	-cd ${SELF} ;				\
	blender -b ${SELF}/null.blend		\
	  -P ${BLENDER_RENDER_SCRIPT}  --	\
	  --verbose				\
	  --scene ${SCENE_DATA}			\
	  --frames ${FRAMES_DATA}		\
	  --style $*				\
	  --output $@				\
	  2>&1					\
	  | tee -a ${PREFIX}/log/r_${*}.log
	${MAKE} -f normalize.Makefile \
	  PREFIX=$@
