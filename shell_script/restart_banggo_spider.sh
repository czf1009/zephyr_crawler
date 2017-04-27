scrapys=`ps -ef|grep scrapy|grep -v grep|awk '{print $2}'`
logname="banggo_"$(date +%Y%m%d_%H:%M:%S)".log"
echo "len_scrapys: "$len_scrapys
if [ $scrapys ];then
	kill ${scrapys[0]}
	for i in 1 2 3 4 5 6 7 8
	do
		echo `ps -ef|grep scrapy|grep -v grep|awk '{print $2}'`
		if [ `ps -ef|grep scrapy|grep -v grep|awk '{print $2}'` ];then
			sleep 1;
		elif [ $i -eq 8 ];then
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
