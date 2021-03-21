#!/usr/bin/python

import freeletics.api as api
import csv
from os.path import exists
from datetime import date
from configargparse import DefaultConfigFileParser

USERS = [("Ueli", 110612994), ("Tobi", 4155941)]
CSV_FILE = 'data.csv'

config = None
with open('freeletics.conf') as file:
    config = DefaultConfigFileParser().parse(file)

token = api.do_login(config['user'], config['password'])
points = []
for user_name,user_id in USERS:
    profile = api.get_profile(token, user_id)
    points.append(profile['points'])

header = None
if not exists(CSV_FILE):
    header = ["Date"] + [name for name,_ in USERS]

with open(CSV_FILE, 'a', newline='') as file:
    datawriter = csv.writer(file)
    if header:
        datawriter.writerow(header)
    datawriter.writerow([date.today()] + points)

with open(CSV_FILE, 'r', newline='') as file:
    datareader = csv.DictReader(file)
    for row in datareader:
        print(row)


