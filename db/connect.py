from credentials import load
import MySQLdb
import sqlalchemy

conf = load.conf

eng = sqlalchemy.create_engine('mysql://'+
                               conf['db']['dbuser'] + ':' +
                               conf['db']['dbpass']+ '@' +
                               conf['db']['dbhost']+ '/' +
                               conf['db']['dbname'])


def open():
    return MySQLdb.connect(
        host=conf['db']['dbhost'],
        user=conf['db']['dbuser'],
        passwd=conf['db']['dbpass'],
        db=conf['db']['dbname']
    )


def sqlalchemy_open():
    global eng
    return eng.connect()

