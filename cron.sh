#! /bin/sh

cd /home/zfchen/scrapy/zephyr_crawler 

scrapy crawl banggo -L WARNING -s LOG_FILE=banggo.log
python process_commen_item.py
sh sql_backup.sh
