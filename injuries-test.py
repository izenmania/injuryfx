# External Packages
import sys
from datetime import date
import re

# Internal Packages
from injury import raw
from injury import parse
from config import load
from db import connect
# from db import query
from aws import connect as s3


#startDate = date(2015, 12, 1)
#endDate = date(2015, 12, 31)
#trans = Transactions()
#trans.loadRaw("data/transactions/test.json")
#trans.getRaw(startDate, endDate)
#trans.saveRaw("data/transactions/201512.json")

# raw.load_raw("201501.json")
# raw.print_raw_transactions()

start_date = date(2015, 12, 1)
end_date = date(2015, 12, 31)

raw.get_raw(start_date, end_date)
raw.save_raw("201512.json")

#s3conn = s3.open()
#output = "asdf"
#s3conn.put_object(Bucket="injuryfx", Key="transactions/test.txt", Body=output)

# objs = client.list_objects(Bucket="injuryfx", Prefix="transactions/")
#
# keys = []
#
# for obj in objs['Contents']:
#     if obj['Size'] > 0:
#         keys.append(obj['Key'])
#
#
# f = client.get_object(Bucket="injuryfx", Key=keys[0])
# o = f['Body']
#
# print(o.read())

#
# # Looping over all the months to get distinct injuries
#
# raw.load_raw("data/transactions/201504.json")
# for t in raw.raw_injuries:
#    inj = parse.parse_injury_transaction(t)
#    print(inj)
#
# # conn = connect.conn
# # try:
# #     with conn.cursor() as cur:
# #         sql = "SELECT * FROM injuries"
# #         cur.execute(sql)
# #         for t in cur:
# #             print(t)
# # finally:
# #     conn.close()
#
# #print(query.select_list("SELECT exact FROM body_part_map"))
