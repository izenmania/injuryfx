#/bin/bash

cd /home/ubuntu/injuryfx
/usr/bin/python scripts/transaction-daily-load.py
/usr/bin/python py-gameday/gameday.py --delta >> /var/log/injuryfx-import/import.log 2>&1

