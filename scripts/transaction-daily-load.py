import sys, os
from datetime import timedelta, datetime, date

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from injury import raw, injury, parse
from db import query

# Retrieve the last transaction saved, and the target conclusion date (typically last night)
final_date = datetime.now().date() - timedelta(days=1)

last_sql = '''
    SELECT *
    FROM injury_load_log
    ORDER BY id DESC
    LIMIT 1
'''

last_saved = query.select_first_row(last_sql)
start_date = last_saved['transaction_date']


# Loop over all dates from the beginning to the cutoff month
while start_date < final_date:
    next_date = injury.next_month(start_date)

    # If we've caught up to the current month, end at yesterday's date
    if start_date.month == final_date.month:
        end_date = final_date
    # Otherwise, go to the end of the month
    else:
        end_date = next_date - timedelta(days=1)

    # Load
    filename = start_date.strftime("%Y%m.json")
    raw.load_raw(filename)

    # Append transactions between start_date and end_date to the list
    raw.append_raw(start_date, end_date)

    # Save latest version of raw injuries file
    raw.save_raw(filename)

    # Save all new injuries to the database
    for i in raw.new_injuries:
        injury.save_injury(parse.parse_injury_transaction(i))
        injury.log_save(i["transaction_id"], datetime.strptime(i["trans_date"], "%Y-%m-%dT00:00:00"))

    # Advance one month
    start_date = next_date