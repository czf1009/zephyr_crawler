import MySQLdb
def connect_mysql():
    try:
        conn = MySQLdb.connect(
            host='172.31.238.60', user='user_gust', passwd='gust', db='app_test', port=3306, charset='utf8')
        conn.ping(True)
        cur = conn.cursor()
        return (conn,cur)
    except MySQLdb.Error, e:
        raise SystemExit('Mysql Error %d: %s' % (e.args[0], e.args[1]))
