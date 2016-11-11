from config import load
import pymysql

conf = load.conf

# conf_stream = open("config/environment.yaml", "r")
# config = yaml.load(conf_stream)['injuryfx']
#
# conn = pymysql.connect(
#     host=config['dbhost'],
#     user=config['dbuser'],
#     password=config['dbpass'],
#     db=config['dbname']
# )
#
# try:
#     with conn.cursor() as cur:
#         sql = "SELECT * FROM test"
#         cur.execute(sql)
#         for t in cur:
#             print(t[1])
# finally:
#     conn.close()

conn = pymysql.connect(
    host=conf['db']['dbhost'],
    user=conf['db']['dbuser'],
    password=conf['db']['dbpass'],
    db=conf['db']['dbname']
)