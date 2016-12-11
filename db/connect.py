"""Functions to open various database api connections, using stored credentials"""
from credentials import load
import MySQLdb
import sqlalchemy

# Load the MySQL connection credentials
conf = load.conf

# Set up a SQLAlchemy engine for later use
eng = sqlalchemy.create_engine('mysql://'+
                               conf['db']['dbuser'] + ':' +
                               conf['db']['dbpass']+ '@' +
                               conf['db']['dbhost']+ '/' +
                               conf['db']['dbname'])


def open():
    """Create a MySQLdb connect object for direct SQL queries"""
    return MySQLdb.connect(
        host=conf['db']['dbhost'],
        user=conf['db']['dbuser'],
        passwd=conf['db']['dbpass'],
        db=conf['db']['dbname']
    )


def sqlalchemy_open():
    """Create a SQLAlchemy connect object for programmatic query building, and selecting into Pandas dataframes"""
    global eng
    return eng.connect()

