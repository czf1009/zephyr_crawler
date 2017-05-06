#!/bin/bash

log_file=`ls banggo_*|tail -n 1`
for i in 1 2 3 4 5
do
	echo '################'$i'times#############'>> test.log
	start_time=`date +%s`
	shell_script/push_redis-key.sh >> test.log
    # scrapy crawl banggo -L INFO -s LOG_FILE=banggo.log >> test.log
	sleep 120;
	while true
	do
		if [ `grep -P '/min' $log_file|tail -n 1|sed -e "s/.* \(.*\) pages.*/\1/g"` -eq 0 ];then
			break;
		else
			sleep 1;
		fi
	done
	echo `mysql -u root -p123456 app_test -e 'select count(*) as common_num from common;'` >> test.log
	echo "banggo:dupefilter: "`redis-cli SCARD banggo:dupefilter` >> test.log
	shell_script/delete_common.sh >> test.log
	redis-cli FLUSHALL >> test.log
	echo "耗时: "$(((`date +%s`-$start_time)/60))" 分" >> test.log
	sleep 3
done
