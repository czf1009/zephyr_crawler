#!/bin/bash

for i in 1 2 3 4 5
do
	echo '################'$i'times#############'>> test.log
	echo "start time: "`date` >> test.log
	sh push_redis-key.sh
    # scrapy crawl banggo -L INFO -s LOG_FILE=banggo.log >> test.log
	sleep 60;
	while true
	do
		if [ `redis-cli EXISTS banggo:requests` -eq 0 ];then
			break;
		else
			sleep 1;
		fi
	done
	echo "banggo:dupefilter: "`redis-cli SCARD banggo:dupefilter` >> test.log
	redis-cli FLUSHALL
	echo "end time: "`date` >> test.log
done
