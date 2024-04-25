#!/bin/env python3

import os
import requests
import sys
import logging

from gnocpush import Pusher

def get_alertmanager_alerts(url):
    r = requests.get(url)
    return r.json()

def main():
    config = {}

    logging.basicConfig(level=logging.DEBUG)
    global log
    log = logging.getLogger(__name__)

    try:
        config['username'] = os.environ['GNOC_USERNAME']
        config['password'] = os.environ['GNOC_PASSWORD']
        config['server'] = os.environ['GNOC_SERVER']
        config['realm'] = os.environ['GNOC_REALM']
        config['alertmanager_url'] = os.environ['ALERTMANAGER_URL']
    except KeyError as e:
        print(f"The {e} environment variable is not set.")
        sys.exit(1)

    yeeter = Pusher(config)
    alerts = get_alertmanager_alerts(config['alertmanager_url'])
    yeeter.push(alerts)

if __name__ == '__main__':
    main()
