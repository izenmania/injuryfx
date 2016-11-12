import json
import requests
from datetime import date

__injury_terms = ["activated", "placed", "transferred"]

raw_transactions = []
raw_injuries = []


# Load raw data from a json file
def load_raw(filepath):
    global raw_transactions, raw_injuries

    # Open the specified file and load json into self.raw
    with open(filepath) as infile:
        raw_transactions = json.load(infile)

    # Populate self.injuries with only the injury transactions
    raw_injuries = filter_raw_injuries()


# Save raw data to a json file
def save_raw(filepath):
    global raw_transactions

    # Export self.raw as json to the specified file
    with open(filepath, 'w') as outfile:
        json.dump(raw_transactions, outfile)


# Retrieve the raw data from the mlb.com json endpoint
def get_raw(start_date: date, end_date: date):
    global raw_transactions, raw_injuries

    # Make sure startDate and endDate are actually dates
    if type(start_date) is not date or type(end_date) is not date:
        raise TypeError("Both arguments of getRaw must be dates")

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
    raw_injuries = filter_raw_injuries()


# output the raw data to the terminal
def print_raw_transactions():
    global raw_transactions

    print(json.dumps(raw_transactions, sort_keys=True, indent=4, separators=(',', ': ')))


# output the injury data to the terminal
def print_raw_injuries():
    global raw_injuries

    print(json.dumps(raw_injuries, sort_keys=True, indent=4, separators=(',', ': ')))


# Filter the raw data to just the injuries
def filter_raw_injuries():
    global raw_transactions, __injury_terms

    i = []
    for t in raw_transactions:
        if any(term in t["note"] for term in __injury_terms):
            i.append(t)

    return i





