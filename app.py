import csv
from datetime import datetime, timedelta
import os
import re

wgs = ["EG"]
for stock in range(1, 4):
    wgs.append("{}. OG links".format(stock))
    wgs.append("{}. OG rechts".format(stock))

tonnen = ["Gelb (Wertstoffe)", "Braun (Bioabfall)", "Schwarz (Restmüll)", "Grün (Altpapier)"]

groupId = os.environ['SIGNAL_GROUP_ID']
username = os.environ['SIGNAL_USERNAME']

assert re.search(r"^[A-Za-z0-9+=]+$", groupId).group() == groupId, "Invalid Group ID"
assert re.search(r"^\+[0-9]+$", username).group() == username, "Invalid Username"

tomorrow = datetime.now()
# tomorrow = datetime(2020, 11, 9)
tomorrow += timedelta(days=1)
tomorrow2 = tomorrow + timedelta(days=1)
checkdays = [tomorrow.date(), tomorrow2.date()]
with open('Trashplan.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=";")
    for row in csv_reader:
        if row['Tonne'] != "":
            rowDate = datetime.strptime(row['Datum'], "%m/%d/%y")
            if rowDate.date() in checkdays:
                assert row['WG'] in wgs
                assert row['Tonne'] in tonnen

                cmd = ("signal-cli -u \"{}\" send "
                       "-g \"{}\" "
                       "-m \"[MÜLLBOT]{}: {} ist dran mit {}\""
                       .format(username,
                               groupId,
                               rowDate.date().strftime("%d.%m. %A"), row['WG'], row['Tonne']))

                print(cmd)
                cmd_out = os.popen(cmd).read()
                print(cmd_out)
