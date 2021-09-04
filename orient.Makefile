DIST := dist

# AXES := X_Y X_-Y -X_Y -X_-Y
# AXES += X_Z X_-Z -X_Z -X_-Z
# AXES += Y_Z Y_-Z -Y_Z -Y_-Z
# AXES += Y_X Y_-X -Y_X -Y_-X
# AXES += Z_Y Z_-Y -Z_Y -Z_-Y
# AXES += Z_X Z_-X -Z_X -Z_-X

AXES := -Z_Y Z_Y X_Y -X_Y

# AXES := X_Y
KEYS_FOLDER := ${DIST}/keys
RENDERS_FOLDER := ${DIST}/renders
KEYS_LIST := ${wildcard ${KEYS_FOLDER}/*}

axes = $(shell echo '"$1"' | jq -M '. / "_"')


all :
	${MAKE} keys
	${MAKE} -f ${MAKEFILE_LIST} \
	  DIST="${DIST}" \
	  AXES="${AXES}" \
	  params
	${MAKE} -f ${MAKEFILE_LIST} \
	  DIST=${DIST} \
	  AXES="${AXES}"  \
	  render-axes

params : ${KEYS_LIST:${KEYS_FOLDER}/%=${RENDERS_FOLDER}/%/params}
	${MAKE} -f ${MAKEFILE_LIST} \
	  DIST=${DIST} \
	  AXES="${AXES}"  \
	  params-symbolic
${RENDERS_FOLDER}/%/params :
	${MAKE} -f render.Makefile \
	  PREFIX=${@D} \
	  params

params-symbolic : 
	$(foreach KEY,${KEYS_LIST:${KEYS_FOLDER}/%=%},\
	  $(foreach AXIS,${AXES},mkdir -p \
	  ${DIST}/${AXIS}/renders/${KEY} ; \
	  ln -sf ../../../renders/${KEY}/params \
	  ${DIST}/${AXIS}/renders/${KEY}/ ; ))

# 	${MAKE} -f ${MAKEFILE_LIST} \
# 	  DIST=${DIST} \
# 	  AXES="${AXES}" \
# 	  params-$*

# ${KEYS_LIST:${KEYS_FOLDER}/%=params-%} :
# 	echo $(foreach AXIS,${AXES},ln -sf ../../../../renders/$$*/params \
# 	  ${DIST}/${AXIS}/renders/$$*/params)

# keys : ${AXES:%=${DIST}/%/keys}
# configs : ${AXES:%=${DIST}/%/config.json}
render-axes : 	${AXES:%=${DIST}/%/config.json} \
		${AXES:%=${DIST}/%/keys} \
		${AXES:%=render-partial-%}

# for a given axis
# ${AXES:%=render-%} : ${DIST}/%/config.json
# render-% : config-% keys-% render-partial-%
render-% : ${DIST}/%/config.json

# config-% : ${DIST}/%/config.json
${DIST}/%/config.json : ${DIST}/%
	cat config.json \
	| jq -M '. | setpath(["geometry", "import_axes"]; $(call axes,$*))' \
	> $@

${AXES:%=${DIST}/%} :
	[ -d "$@" ] || mkdir -p $@

keys-% : ${DIST}/%/keys
${DIST}/%/keys : ${DIST}/%
	ln -sf ../keys $@

render-partial-% : ${DIST}/%/config.json ${DIST}/%/keys 
	export SHADEGAN_CONFIG=${DIST}/$*/config.json ; \
	${MAKE} -k \
	  PREFIX=${DIST}/$* \
	  render-partials

