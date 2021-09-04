SHELL		:= /bin/zsh

include config.Makefile
# requires variables
# PREFIX

SELF := $(realpath $(firstword $(MAKEFILE_LIST)))

CMD  := { cd $(dir ${SELF}) ; make -f $(notdir ${SELF}) write-count ; }

write-count: 
	printf "%s\t%s\n" \
	  `cd ${PREFIX} ; find . -iname "*.png" | wc -l` \
	  "`date '+%m/%d %H:%M'`" \
	  >> ${COUNT_FILE}

setup-cron : unset-cron
	{ \
	  echo "* * * * * ${CMD}" ;\
	} | ${CRONTAB} -n -

# unset-cron :
# 	${CRONTAB} -l | \
# 	  sed '/$(subst /,\/,$(dir ${SELF}))/d' | \
# 	  ${CRONTAB} -n -
unset-cron :
	${CRONTAB} -l | \
	  grep -v "$(dir ${SELF})" | \
	  ${CRONTAB} -n -

watch :
	watch -n .5 -- 'tail -n 30 ${COUNT_FILE} | tac'
