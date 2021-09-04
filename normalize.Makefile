SHELL		:= /bin/zsh

include config.Makefile
# requires variables
# PREFIX

IMAGES := ${wildcard ${PREFIX}/*.png}
NORM_IMAGES := ${IMAGES:${PREFIX}/%.png=n_%}

all : ${NORM_IMAGES}
.PHONY: all

n_% :
	convert ${PREFIX}/${*}.png	\
	  -colorspace gray		\
	  -normalize			\
	  -background white		\
	  +flatten			\
	  ${PREFIX}/${*}.png
