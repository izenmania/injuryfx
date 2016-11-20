import json
import requests
import re
from ..injuries import Transactions

trans = Transactions()


# http://mlb.mlb.com/lookup/json/named.transaction_all.bam?start_date=20151001&end_date=20151031&sport_code=%27mlb%27

injuryTerms = ["activated", "placed", "transferred"]
positions = ["C", "1B", "2B", "3B", "SS", "RF", "CF", "LF", "OF", "DH", "RHP", "LHP"]
directions = ["from", "on", "to"]

# url = "http://mlb.mlb.com/lookup/json/named.transaction_all.bam?start_date=%(sd)s&end_date=%(ed)s&sport_code=%(sc)s"
# payload = {
#     'sd': '20160901',
#     'ed': '20160930',
#     'sc': '%27mlb%27',
# }
#
# r = requests.get(url % payload)
# response = r.json()
#
# transactions = response["transaction_all"]["queryResults"]["row"]
#
# injuries = []
#
# for t in transactions:
#     if any(term in t["note"] for term in injuryTerms):
#         injuries.append(t)
#
#
# print(json.dumps(injuries, sort_keys=True, indent=4, separators=(',', ': ')))

# trans = {
#         "conditional_sw": "",
#         "effective_date": "2016-09-30T00:00:00",
#         "final_asset": "",
#         "final_asset_type": "",
#         "from_team": "",
#         "from_team_id": "",
#         "name_display_first_last": "Shin-Soo Choo",
#         "name_display_last_first": "Choo, Shin-Soo",
#         "name_sort": "CHOO, SHIN-SOO",
#         "note": "Texas Rangers activated RF Shin-Soo Choo from the 15-day disabled list.",
#         "orig_asset": "Player",
#         "orig_asset_type": "PL",
#         "player": "Shin-Soo Choo",
#         "player_id": "425783",
#         "resolution_cd": "FIN",
#         "resolution_date": "2016-09-30T00:00:00",
#         "team": "Texas Rangers",
#         "team_id": "140",
#         "trans_date": "2016-09-30T00:00:00",
#         "trans_date_cd": "D",
#         "transaction_id": "288181",
#         "type": "Status Change",
#         "type_cd": "SC"
#     }
#
# note = trans["note"]
# team = trans["team"]
# player = trans["player"]
#
# searchString = team+" ("+'|'.join(injuryTerms)+") ("+'|'.join(positions)+") "+player+" ("+'|'.join(directions)+") the (.*) list\."
# results = re.search(searchString, note)
# print(results.group(2))
# print(results.group(3))
# print(results.group(4))