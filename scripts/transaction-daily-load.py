import sys, os
import datetime
from datetime import timedelta

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from injury import raw

# This process is intended to run every morning
yesterday = datetime.datetime.now().date() - timedelta(days=1)

filename = yesterday.strftime("%Y%m.json")
raw.load_raw(filename)
raw.append_raw(yesterday, yesterday)
raw.save_raw(filename)