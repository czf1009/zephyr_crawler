echo `mysql -u root -p123456 app_test -e 'select count(*) as common_num from common;'`
echo "banggo:dupefilter: "`redis-cli scard banggo:dupefilter`
echo "banggo:requests: "`redis-cli zcard banggo:requests`
