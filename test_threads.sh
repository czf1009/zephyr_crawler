#!/bin/bash

for j in 256 192 128 64 32 16 8 4 1
do
	concurent_request=`grep -E "CONCURRENT_REQUESTS =" zephyr_crawler/settings.py`
	sed -i "s/${concurent_request}/CONCURRENT_REQUESTS = "${j}"/" zephyr_crawler/settings.py
	echo '#####################  Thread number'$j>> test.log
	echo '########'$j>> banggo.log
	echo '########'$j>> banggo.log
	echo '########'$j>> banggo.log
	for i in 1 2 3 4 5
    do
		echo '################'$i'times###############'>> banggo.log
		echo '################'$i'times'>> test.log
    	scrapy crawl banggo -L INFO -s LOG_FILE=banggo.log >> test.log
		grep -E 'request_count|#####' banggo.log|tail -n 1 >> test.log
    done
done
