from db import connect
import MySQLdb

def run_sql(sql):

    conn = connect.open()
    params = ()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, params)

file = open('/tmp/mysql-cache.log', 'w+')
file.write("Starting flask. The system is safe to use now but slow. Starting caching.\n")
file.flush()
for y in [2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008]:
   file.write("Caching " + str(y + 1) + " data...\n")
   file.flush()
   run_sql('SELECT g.game_id FROM gameday.game g INNER JOIN gameday.atbat b ON g.game_id=b.game_id WHERE g.date > "' + str(y) + '-12-30"')
   run_sql('SELECT g.game_id FROM gameday.game g INNER JOIN gameday.pitch p ON g.game_id=p.game_id WHERE g.date > "' + str(y) + '-12-30"');

file.write('\nSystem Ready!\n')
file.close()
