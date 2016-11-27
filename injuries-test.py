# External Packages
import sys
from datetime import date
from datetime import timedelta
import re

# Internal Packages
from injury import raw
from injury import parse
from config import load
#from db import connect
# from db import query
#from aws import connect as s3





# raw.load_raw("data/transactions/201504.json")
# for t in raw.raw_injuries:
#    inj = parse.parse_injury_transaction(t)
#    print(inj)


def next_month(d):
    y = d.year
    m = d.month
    new_m = d.month + 1
    new_y = y
    if new_m > 12:
        new_m = 1
        new_y += 1
    return date(new_y, new_m, 1)

start_date = date(2009, 4, 1)
final_date = date(2016, 10, 1)

# Loop over all dates from the beginning to the cutoff month
while start_date < final_date:
    filename = start_date.strftime("%Y%m.json")
    raw.load_raw(filename)
    for t in raw.raw_injuries:
        inj = parse.parse_injury_transaction(t)
        if "injury" in inj:
            print(inj['injury'])

    start_date = next_month(start_date)