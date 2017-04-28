scrapys=`ps -ef|grep scrapy|grep -v grep|awk '{print $2}'`
logname="banggo_"$(date +%Y%m%d_%H%M%S)".log"
if [ $scrapys ];then
	kill ${scrapys[0]}
	for i in {1..15}
	do
		if [ `ps -ef|grep scrapy|grep -v grep|awk '{print $2}'` ];then
			sleep 1;
		elif [ $i -eq 15 ];then
			echo 'kill scrapy failed! please check is scrapy runing.'
			exit
		else
			echo 'kill scrapy process success.'
			break
		fi
	done
	scrapy crawl banggo -s LOG_FILE=$logname >> test.log&
	echo 'start scrapy success.'
else
	echo "No scrapy runing."
	scrapy crawl banggo -s LOG_FILE=$logname >> test.log&
	echo 'start scrapy success.'
fi
