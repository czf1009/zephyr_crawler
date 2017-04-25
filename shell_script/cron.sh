#! /bin/sh

cd /home/zfchen/zephyr_crawler 

scrapy crawl banggo -L INFO -s LOG_FILE=banggo.log
scrapy crawl jd -L INFO -s LOG_FILE=jd.log
python python_script/process_common_item.py
sh shell_script/sql_backup.sh
#bash shell_script/test_threads.sh
