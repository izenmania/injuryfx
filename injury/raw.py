import json
import requests
import sys
from datetime import date, datetime
from aws import connect
import botocore

__injury_terms = ["activated", "placed", "transferred", "from the 15", "from the 60", "from the 7"]

raw_transactions = []
raw_injuries = []
new_transactions = []
new_injuries = []

s3 = connect.open()


def load_raw(filename):
    global raw_transactions, raw_injuries, s3

    # Attempt to load the transactions
    try:
        obj = s3.get_object(Bucket="injuryfx", Key="transactions/"+filename)
        raw_transactions = json.loads(obj['Body'].read().decode())
        print(raw_transactions)
        raw_injuries = filter_raw_injuries(raw_transactions)
    except botocore.exceptions.ClientError:
        print("No such key %s. Loading empty list for raw.", (filename,))
        raw_transactions = []
        raw_injuries = []


def save_raw(filename):
    global raw_transactions, s3

    content = json.dumps(raw_transactions).encode()
    s3.put_object(Bucket="injuryfx", Key="transactions/"+filename, Body=content)


# Retrieve the raw data from the mlb.com json endpoint
def get_raw(start_date, end_date):
    global raw_transactions, raw_injuries

    # Make sure startDate and endDate are actually dates
    if type(start_date) is not date or type(end_date) is not date:
        raise TypeError("Both arguments of get_raw must be dates")

    # Construct the URL for the mlb.com json endpoint
    url = "http://mlb.mlb.com/lookup/json/named.transaction_all.bam?start_date=%(sd)s&end_date=%(ed)s&sport_code=%(sc)s"
    payload = {
        'sd': start_date.strftime("%Y%m%d"),
        'ed': end_date.strftime("%Y%m%d"),
        'sc': '%27mlb%27',
    }

    # Retrieve the json data, strip off some wrappers, and load into self.raw
    r = requests.get(url % payload)
    raw_transactions = r.json()["transaction_all"]["queryResults"]["row"]

    # Populate self.injuries with only the injury transactions
    raw_injuries = filter_raw_injuries(raw_transactions)


# def append_raw(start_date, end_date):
#     global raw_transactions, raw_injuries
#
#     # Make sure startDate and endDate are actually dates
#     if type(start_date) is not date or type(end_date) is not date:
#         raise TypeError("Both arguments of append_raw must be dates")
#
#     # Construct the URL for the mlb.com json endpoint
#     url = "http://mlb.mlb.com/lookup/json/named.transaction_all.bam?start_date=%(sd)s&end_date=%(ed)s&sport_code=%(sc)s"
#     payload = {
#         'sd': start_date.strftime("%Y%m%d"),
#         'ed': end_date.strftime("%Y%m%d"),
#         'sc': '%27mlb%27',
#     }
#
#     # Retrieve the json data, strip off some wrappers, and load into self.raw
#     r = requests.get(url % payload)
#     raw_transactions.append(r.json()["transaction_all"]["queryResults"]["row"])
#
#     # Populate self.injuries with only the injury transactions
#     raw_injuries.append(filter_raw_injuries())

def append_raw(start_date, end_date):
    global raw_transactions, raw_injuries, new_transactions, new_injuries

    # Make sure start_date and end_date are actually dates
    if type(start_date) is not date or type(end_date) is not date:
        raise TypeError("Both arguments of append_raw must be dates")

    # If there are contents in raw_transactions, get the last id and date
    if raw_transactions:
        last_transaction_id = int(raw_transactions[-1]["transaction_id"])
        last_transaction_date = datetime.strptime(raw_transactions[-1]["trans_date"], "%Y-%m-%dT00:00:00").date()
    else:
        last_transaction_id = 0
        last_transaction_date = date(1000,1,1)

    # Construct the URL for the mlb.com json endpoint
    url = "http://mlb.mlb.com/lookup/json/named.transaction_all.bam?start_date=%(sd)s&end_date=%(ed)s&sport_code=%(sc)s"
    payload = {
        'sd': start_date.strftime("%Y%m%d"),
        'ed': end_date.strftime("%Y%m%d"),
        'sc': '%27mlb%27',
    }

    # Retrieve the json data, strip off some wrappers, and load into new_transactions
    r = requests.get(url % payload)
    new_transactions = r.json()["transaction_all"]["queryResults"]["row"]

    # If this import overlaps dates with the last row imported, trim duplicates
    if last_transaction_date >= start_date:
        i = 0
        for t in new_transactions:
            i += 1
            if int(t["transaction_id"]) == last_transaction_id:
                break

        new_transactions = new_transactions[i:]

    # Append the new transactions to the full raw for the month
    new_injuries = filter_raw_injuries(new_transactions)
    raw_transactions += new_transactions
    raw_injuries += new_injuries


# output the raw data to the terminal
def print_raw_transactions():
    global raw_transactions

    print(json.dumps(raw_transactions, sort_keys=True, indent=4, separators=(',', ': ')))


# output the injury data to the terminal
def print_raw_injuries():
    global raw_injuries

    print(json.dumps(raw_injuries, sort_keys=True, indent=4, separators=(',', ': ')))


# Filter the raw data to just the injuries
# def filter_raw_injuries():
#     global raw_transactions, __injury_terms
#
#     i = []
#     for t in raw_transactions:
#         if any(term in t["note"] for term in __injury_terms) and not (
#                             "paternity list" in t["note"] or "restricted list" in t["note"] or "bereavement list" in t["note"] or "waivers" in t["note"]
#         ):
#             i.append(t)
#
#     return i


def filter_raw_injuries(trans):
    global __injury_terms

    i = []
    for t in trans:
        if any(term in t["note"] for term in __injury_terms) and not (
                            "paternity list" in t["note"] or "restricted list" in t["note"] or "bereavement list" in t["note"] or "waivers" in t["note"]
        ):
            i.append(t)

    return i


