import sys, logging
sys.path.insert(0, '/var/www/injuryfx')

from app import app as application

logging.basicConfig(filename='/var/log/flask/error.log',level=logging.DEBUG)