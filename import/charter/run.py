import csv
import json
from subprocess import check_output
import sqlite3

csv_str = check_output(["./import/charter/scrape/phantomjs",
  "./import/charter/scrape/scrape.js", "./import/charter/scrape/config.yaml"])

csv_list = csv_str.strip().split("\n")
csv_list.reverse()  # was descending, make it ascending

sessions = []
start = None
for row in csv.reader(csv_list):
  if not start:
    start = (int(row[0]), row[2])
  else:
    time = int(row[0])
    # If > 4 hours between start and end, assume different sessions
    if time - start[0] > 1000*60*60*4 or start[1] != row[2]:
      sessions.append((start[0], start[0] + 1000*60*40, start[1]))
      start = (int(row[0]), row[2])
    else:
      sessions.append((start[0], int(row[0]), row[2]))
      start = None

# Account for a final session with no end
if start:
  sessions.append((start[0], start[0] + 1000*60*40, start[1]))  # 40 minute

conn = sqlite3.connect('qcm.db')
# Delete any existing entries
start_times = set([session[0] for session in sessions])
toDelete = []
for row in conn.execute("SELECT key, value FROM activities;"):
  value = json.loads(row[1])
  if value['start'] in start_times:
    toDelete.append(str(row[0]))
if len(toDelete) > 0:
  conn.execute("DELETE FROM activities WHERE key IN (%s);" %
      ",".join(toDelete))

for session in sessions:
  toWrite = {"activity": ["gym"], "start": session[0], "stop": session[1],
      "extra": {"location": session[2]}}
  conn.execute("INSERT INTO activities (value) VALUES (?);", 
      (json.dumps(toWrite),))

conn.commit()
conn.close()
