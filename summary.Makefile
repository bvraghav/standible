include config.Makefile

$(guile (load "summary.scm"))

all : summary-as-image-montages

${SUMMARY_FOLDER}, ${SUMMARY_FOLDER}/montages :
	mkdir -p $@

## summary-as-image-montages
## ====================================================
# requires variables
# -----------------------------------
# PREFIX		: data path
# RENDERS_FOLDER	: renders path
# SUMMARY_FOLDER	: output path
# STYLES		: list of styles to summarize
# SUMMARY_NUM_SAMPLES	: num samples to summarize

NS		:= $(guile (or ${SUMMARY_NUM_SAMPLES} 8))
SMY_KEYS	:= $(guile					\
	(random-key-frame-pairs  ${NS} "${RENDERS_FOLDER}")	\
)
SMY_MONTAGES	:= ${SMY_KEYS:%=${SUMMARY_FOLDER}/montages/%}

summary-as-image-montages : ${SUMMARY_FOLDER}/montage_summary.png
# summary-as-image-montages : 
# 	echo ${SMY_KEYS}

${SUMMARY_FOLDER}/montage_summary.png : ${SMY_MONTAGES}
	montage $^ ${SMY_L0_MONTAGE_OPTIONS} $@

${SUMMARY_FOLDER}/montages/% : ${SUMMARY_FOLDER}/montages
	montage $(guile (all-images "${RENDERS_FOLDER}" "$*" "${STYLES}")) \
	  ${SMY_L1_MONTAGE_OPTIONS} \
	  $@

## find-keys-with-num-primitives
## ====================================================
# requires variables
# -----------------------------------
# PREFIX		: data path
# SUMMARY_FOLDER	: output path
# FIND_NUM_PRIMITIVES	: num primitives to find

N		:= ${FIND_NUM_PRIMITIVES}
M		:= $(guile (1- ${N}))
N_DB		:= ${SUMMARY_FOLDER}/$N-primitives.db
N_KEYS_FOLDER	:= ${SUMMARY_FOLDER}/$N-renders
RENDER_KEYS	:= $(shell ls ${KEYS_FOLDER})
KEY_X_HAS_N	:= ${RENDER_KEYS:%=key_%_has_n}
is_num_prim	 = $(shell grep $(solid $1) ${N_DB})
solid		 = $(shell )

find-keys-with-num-primitives : ${N_DB} ${KEY_X_HAS_N}

${N_DB} : ${SUMMARY_FOLDER}
	cd ${PREFIX} ; \
	sift '"tree":\s+"[^"]*$M[^"]*"' csg-graph/json | \
	  cut -d: -f1 | \
	  cut -d/ -f3 | \
	  cut -d. -f1 \
	  > $@

key_%_has_n : ${NDB} ${N_KEYS_FOLDER}
	${MAKE} -f $(firstword ${MAKEFILE_LIST}) KEY=$* key-has-n

key-has-n :
	cd ${PREFIX} ; \
	SOLID=`cat renders/${KEY}/params/meta.ndjson | \
		grep -o '"name": "[0-9a-f]\+.stl' | \
		cut -d\" -f4 | cut -d. -f1` ;\
	echo $$SOLID ;\
	IS_NUM_PRIM=`grep $$SOLID ${N_DB}` ;\
	echo $$IS_NUM_PRIM ;\
	[ ! -z "$$IS_NUM_PRIM" ] && \
	  touch ${N_KEYS_FOLDER}/${KEY} || \
	  echo "${KEY} not has $N"

${N_KEYS_FOLDER} :
	mkdir -p $@
