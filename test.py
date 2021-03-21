#!/usr/bin/python


USERS = [("Ueli", 110612994), ("Tobi", 4155941)]

import freeletics.api as api
from configargparse import DefaultConfigFileParser

config = None
with open('freeletics.conf') as file:
    config = DefaultConfigFileParser().parse(file)

token = api.do_login(config['user'], config['password'])
for user_name,user_id in USERS:
    profile = api.get_profile(token, user_id)
    print("{},{}".format(user_name, profile['points']))

