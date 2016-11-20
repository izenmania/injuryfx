from config import load
import pymysql

conf = load.conf


def open():
    return pymysql.connect(
        host=conf['db']['dbhost'],
        user=conf['db']['dbuser'],
        password=conf['db']['dbpass'],
        db=conf['db']['dbname']
    )