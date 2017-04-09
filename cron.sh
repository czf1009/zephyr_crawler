#! /bin/sh

cd /home/zfchen/zephyr_crawler 

scrapy crawl banggo -L WARNING -s LOG_FILE=banggo.log
scrapy crawl jd -L WARNING -s LOG_FILE=jd.log
python process_commen_item.py
sh sql_backup.sh
