from credentials import load
import MySQLdb

conf = load.conf


def open():
    return MySQLdb.connect(
        host=conf['db']['dbhost'],
        user=conf['db']['dbuser'],
        passwd=conf['db']['dbpass'],
        db=conf['db']['dbname']
    )
