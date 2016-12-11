"""Functions for downloading, processing and saving the raw JSON files from the MLB transaction API"""
import json
import requests
import sys
from datetime import date, datetime
from aws import connect
import botocore

# Utility list for determining which transactions are injury-related
__injury_terms = ["activated", "placed", "transferred", "from the 15", "from the 60", "from the 7"]

# All the lists that will be populated by other functions
raw_transactions = []
raw_injuries = []
new_transactions = []
new_injuries = []

# Open a connection to Amazon S3, where we will be storing the downloaded JSON.
s3 = connect.open()


def load_raw(filename):
    """Load a transaction JSON file from the S3 bucket. Typically files contain a single full month of transactions.
    Standard filenames are YYYYMM.json (ex: 201609.json)"""
    global raw_transactions, raw_injuries, s3

    try:
        # Attempt to load the transactions
        obj = s3.get_object(Bucket="injuryfx", Key="transactions/"+filename)
        # If the file loaded, place all data into the raw_transactions list.
        raw_transactions = json.loads(obj['Body'].read().decode())
        # Filter only the injury-related transactions into the raw_injuries list
        raw_injuries = filter_raw_injuries(raw_transactions)
    except botocore.exceptions.ClientError:
        # If the file does not exist, set the raw lists to empty.
        print("No such key %s. Loading empty list for raw.", (filename,))
        raw_transactions = []
        raw_injuries = []


def save_raw(filename):
    """Save a list of transaction dicts to a file on S3. As above, standard filenames of YYYYMM.json"""
    global raw_transactions, s3

    # Convert list to JSON and encode as the byte type for transmission.
    content = json.dumps(raw_transactions).encode()
    # Place the object in S3.
    s3.put_object(Bucket="injuryfx", Key="transactions/"+filename, Body=content)


def get_raw(start_date, end_date):
    """Retrieve the raw data from the original mlb.com json endpoint."""
    global raw_transactions, raw_injuries

    # Make sure start_date and end_date are actually dates
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


def append_raw(start_date, end_date):
    """Given an existing raw_transactions list, append a new set of transaction data from the MLB transaction API.
    Also place newly downloaded data into new_injuries for processing."""
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

    # If this import overlaps dates with the last row imported, trim duplicates, which have already been saved
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


def print_raw_transactions():
    """Output the raw transaction data to the terminal, for testing purposes"""
    global raw_transactions

    print(json.dumps(raw_transactions, sort_keys=True, indent=4, separators=(',', ': ')))


def print_raw_injuries():
    """Output the raw injury data to the terminal, for testing purposes"""
    global raw_injuries

    print(json.dumps(raw_injuries, sort_keys=True, indent=4, separators=(',', ': ')))



def filter_raw_injuries(trans):
    """Given a list of raw transaction JSON, filter down to a list of only injury-related transactions"""
    global __injury_terms

    i = []
    for t in trans:
        # If one of the __injury_terms appears in note, it is almost always an injury transaction
        if any(term in t["note"] for term in __injury_terms) and not (
                            # Handle a few edge cases where __injury_terms appear without injury
                            "paternity list" in t["note"] or "restricted list" in t["note"] or "bereavement list" in t["note"] or "waivers" in t["note"]
        ):
            i.append(t)

    return i


