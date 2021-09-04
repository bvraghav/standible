include config.Makefile

OUT_FOLDERS	:=
OUT_FOLDERS	+= ${KEYS_FOLDER}
OUT_FOLDERS	+= ${RENDERS_FOLDER}




RENDER_DEPS	:= 

KEYS_LIST	:= ${wildcard ${KEYS_FOLDER}/*}
RENDER_DEPS	+= ${KEYS_LIST:${KEYS_FOLDER}/%=${RENDERS_FOLDER}/%/complete}

RENDER_PARTIALS := ${KEYS_LIST:${KEYS_FOLDER}/%=${RENDERS_FOLDER}/%/partial}

SELF		:= $(realpath $(dir $(realpath $(firstword $(MAKEFILE_LIST)))))


all :
	$(MAKE) keys

	${MAKE} -f ${SELF}/count.Makefile write-count
	${MAKE} -f ${SELF}/count.Makefile setup-cron

	-${MAKE} renders

	${MAKE} -f ${SELF}/count.Makefile unset-cron
	${MAKE} -f ${SELF}/count.Makefile write-count

keys : ${KEYS_FOLDER}
	seq 1 ${NUM_KEYS} \
	| parallel uuidgen \
	| cut -d- -f1 \
	| parallel touch ${KEYS_FOLDER}/{}

${OUT_FOLDERS} :
	[ ! -d "$@" ] && \
	  mkdir -p $@

renders : ${RENDERS_FOLDER}/continue

${RENDERS_FOLDER}/continue : ${RENDERS_FOLDER} ${RENDER_DEPS}

${RENDERS_FOLDER}/%/complete :
	${MAKE} -f render.Makefile \
	  PREFIX=${@D} \
	  NUM_FRAMES=${NUM_FRAMES} \
	  NUM_KEYFRAMES=${NUM_KEYFRAMES} \
	&& touch $@

render-partials : ${RENDER_PARTIALS}
${RENDERS_FOLDER}/%/partial :
	${MAKE} -f render.Makefile \
	  PREFIX=${@D} \
	  NUM_FRAMES=${NUM_FRAMES} \
	  NUM_KEYFRAMES=${NUM_KEYFRAMES} \
	  all-renders
	touch $@


.PHONY: all keys renders render-partials
