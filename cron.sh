#! /bin/sh

cd /home/zfchen/zephyr_crawler 

scrapy crawl banggo -L INFO -s LOG_FILE=banggo.log
scrapy crawl jd -L INFO -s LOG_FILE=jd.log
python process_common_item.py
sh sql_backup.sh
bash test_threads.sh