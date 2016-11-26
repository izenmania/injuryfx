from injury import raw
from injury import parse
from injury import injury
import sys
from datetime import date
from datetime import timedelta

# raw.load_raw("201504.json")

#injuries = []

# for i in raw.raw_injuries:
#     inj = parse.parse_injury_transaction(i)
#     print(inj)
#
# injuries = [injury.save_injury(parse.parse_injury_transaction(i)) for i in raw.raw_injuries]
# print(injuries)

# parse.parse_note("asdf", "Dave Butts", "Tampa Bay Rays")


# This is the first date of the json-based transaction tracker
start_date = date(2009, 4, 1)
final_date = date(2016, 10, 1)

# Take any date object and return a date object of the first day of the next month
def next_month(d):
    y = d.year
    m = d.month
    new_m = d.month + 1
    new_y = y
    if new_m > 12:
        new_m = 1
        new_y += 1
    return date(new_y, new_m, 1)


# Loop over all dates from the beginning to the cutoff month
while start_date < final_date:
    next_date = next_month(start_date)
    end_date = next_date - timedelta(days=1)
    filename = start_date.strftime("%Y%m.json")

    raw.load_raw(filename)

    injuries = [injury.save_injury(parse.parse_injury_transaction(i)) for i in raw.raw_injuries]
    print(injuries)

    start_date = next_date