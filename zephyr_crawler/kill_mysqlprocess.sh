#杀掉锁定的MySQL连接
for id in `mysqladmin processlist -u user_test -ptest|grep -i locked|awk '{print $1}'`
do
	mysqladmin kill ${id}
done
