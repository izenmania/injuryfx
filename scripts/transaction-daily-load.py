import sys, os
import datetime
from datetime import timedelta

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from injury import raw
from db import query

# This process is intended to run every morning
# yesterday = datetime.datetime.now().date() - timedelta(days=1)

# filename = yesterday.strftime("%Y%m.json")
# raw.load_raw(filename)
# raw.append_raw(yesterday, yesterday)
# raw.save_raw(filename)

# Retrieve the last transaction saved, and the target conclusion date (typically last night)
yesterday = datetime.datetime.now().date() - timedelta(days=1)

last_sql = '''
    SELECT *
    FROM injury_load_log
    ORDER BY id DESC
    LIMIT 1
'''

last_saved = query.select_first_row(last_sql)

print(last_saved)