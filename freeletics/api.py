#!/usr/bin/python
"""Generate statistics from your Freeletics feed"""

import collections
import json
import requests

import configargparse

URL_LOGIN = 'https://api.freeletics.com/user/v1/auth/password/login'
URL_FEED = 'https://api.freeletics.com/v3/users/{}/feed_entries?page={}'
URL_PROFILE = 'https://api.freeletics.com/v3/users/{}'
CONFIG_FILENAME = 'freeletics.conf'

def get_feedpage(token, i):
    """Get feed entries for a given page"""
    feed_response = requests.get(URL_FEED.format(token.user_id, i), headers=token.header)
    feed_json = json.loads(feed_response.text)
    return feed_json['feed_entries']

def get_feedentries(token):
    """ Get all feed entries"""
    i = 0
    feed_entries = []
    page_feed_entries = get_feedpage(token, i)
    while page_feed_entries:
        feed_entries += page_feed_entries
        i += 1
        page_feed_entries = get_feedpage(token, i)
    return feed_entries

def get_profile(token, user_id):
    """ Get profile"""
    response = requests.get(URL_PROFILE.format(user_id), headers=token.header)
    profile = json.loads(response.text)
    return profile['user']

def do_login(user, password):
    """Log-in and return auth token"""

    login_payload = {
        "login": {
            "email": user,
            "password": password
        }
    }

    login_response = requests.post(URL_LOGIN, json=login_payload)
    login_ans = json.loads(login_response.text)
    id_token = login_ans['auth']['id_token']
    token = collections.namedtuple('AuthToken', ['user_id', 'header'])
    token.user_id = login_ans['user']['id']
    token.header = {'Authorization': 'Bearer ' + id_token}
    return token


def main():
    """Main func"""
    parser = configargparse.ArgParser(default_config_files=[CONFIG_FILENAME])
    parser.add('-c', '--config', is_config_file=True, help='Configuration file')
    parser.add('-u', '--user', required=True, help='Username/Email')
    parser.add('-p', '--password', required=True, help='Password')
    parser.add('-o', '--output-file', help='If specified, save results to this file')

    config = parser.parse_args()

    token = do_login(config.user, config.password)
    entries_string = json.dumps(get_feedentries(token))
    if config.output_file:
        with open(config.output_file, 'w') as file:
            file.write(entries_string)
    else:
        print(entries_string)


if __name__ == "__main__":
    main()
