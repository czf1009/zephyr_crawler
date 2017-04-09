#! /bin/sh

cd /home/zfchen/zephyr_crawler/sql

datename=$(date +%Y%m%d-%H%M%S) 
mysqldump -uuser_test -ptest app_test > $datename.sql

