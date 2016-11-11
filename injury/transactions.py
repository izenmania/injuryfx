import json
import requests
import re
from datetime import date
#from injuries.injury import *

__injuryTerms = ["activated", "placed", "transferred"]
__positions = ["C", "1B", "2B", "3B", "SS", "RF", "CF", "LF", "OF", "DH", "RHP", "LHP"]
__directions = ["from", "on", "to"]
__dl_types = ["15-day", "60-day"]

rawTransactions = []
rawInjuries = []


# Load raw data from a json file
def loadRaw(filepath):
    global rawTransactions, rawInjuries

    # Open the specified file and load json into self.raw
    with open(filepath) as infile:
        rawTransactions = json.load(infile)

    # Populate self.injuries with only the injury transactions
    rawInjuries = filterRawInjuries()


# Save raw data to a json file
def saveRaw(filepath):
    global rawTransactions

    # Export self.raw as json to the specified file
    with open(filepath, 'w') as outfile:
        json.dump(rawTransactions, outfile)


# Retrieve the raw data from the mlb.com json endpoint
def getRaw(startDate: date, endDate: date):
    global rawTransactions, rawInjuries

    # Make sure startDate and endDate are actually dates
    if type(startDate) is not date or type(endDate) is not date:
        raise TypeError("Both arguments of getRaw must be dates")

    # Construct the URL for the mlb.com json endpoint
    url = "http://mlb.mlb.com/lookup/json/named.transaction_all.bam?start_date=%(sd)s&end_date=%(ed)s&sport_code=%(sc)s"
    payload = {
        'sd': startDate.strftime("%Y%m%d"),
        'ed': endDate.strftime("%Y%m%d"),
        'sc': '%27mlb%27',
    }

    # Retrieve the json data, strip off some wrappers, and load into self.raw
    r = requests.get(url % payload)
    rawTransactions = r.json()["transaction_all"]["queryResults"]["row"]

    # Populate self.injuries with only the injury transactions
    rawInjuries = filterRawInjuries()


# output the raw data to the terminal
def printRawTransactions():
    global rawTransactions

    print(json.dumps(rawTransactions, sort_keys=True, indent=4, separators=(',', ': ')))


# output the injury data to the terminal
def printRawInjuries():
    global rawInjuries

    print(json.dumps(rawInjuries, sort_keys=True, indent=4, separators=(',', ': ')))


# Filter the raw data to just the injuries
def filterRawInjuries():
    global rawTransactions, __injuryTerms

    i = []
    for t in rawTransactions:
        if any(term in t["note"] for term in __injuryTerms):
            i.append(t)

    return i



def parseInjury(rawInjury):
    global __directions, __dl_types, __injuryTerms, __positions

    searchString = rawInjury["team"] + " (" + '|'.join(__injuryTerms) + ") (" + '|'.join(__positions) + ") " + rawInjury["player"] + " (" + '|'.join(__directions) + ") the( 15-day disabled list to the)? (" + '|'.join(__dl_types) + ") disabled list( .*)?\. ?(.*)?"
    results = re.search(searchString, rawInjury["note"])
    if results == None:
        inj = {}
    else:
        inj = {
            "transaction_id": rawInjury["player"],
            "transaction_date": rawInjury["effective_date"],
            "player_name": rawInjury["player"],
            "player_id_mlbam": rawInjury["player_id"],
            "team_name": rawInjury["team"],
            "team_id_mlbam": rawInjury["team_id"],
            "action": results.group(1),
            "dl_type": results.group(5),
            "injury": results.group(7).replace(".", ""),
            "note": rawInjury["note"]
        }

    return(inj)

