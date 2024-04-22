#!/bin/env python3

import os
import requests
import sys
import yaml
import logging

from dateutil import parser
from globalnoc_alertmon_agent import AlertMonAgent, Alert

def sanitize_severity(severity):
    s = 'Unknown'

    # match statement doesn't seem to have an easy way to do case insensitive
    # matching, so we force everything to lower case.
    match severity.lower():
        case 'critical' | 'alert': s = 'Critical'
        case 'major' | 'warning': s ='Major'
        case 'minor' | 'info': s = 'Minor'
        case 'unknown': s = 'Unknown'
        case 'ok': s ='Ok'

    log.debug(f'severity: {severity} -> {s}')
    return s

def push_to_gnoc(alerts, agent):
    # initialize the alertmon agent
    for alert in alerts:
        data = {
            'node_name': alert['labels'].get('pod', 'Unknown'),
            'service_name': alert['labels'].get('alertname', 'Unknown'),
            'severity': sanitize_severity(alert['labels'].get('severity', 'Unknown')),
            'description': alert['annotations'].get('description', 'Unknown'),
            'start_time': parser.isoparse(alert['startsAt']).timestamp()
        }

        agent.add_alert(Alert(
            start_time   = data.get('start_time', None),
            node_name    = data.get('node_name'),
            service_name = data.get('service_name'),
            description  = data.get('description'),
            severity     = data.get('severity')
        ))

    agent.send_alerts()


def get_alertmanager_alerts(url):
    r = requests.get(url)
    return r.json()#['data']['alerts']

def main():
    config = {}

    logging.basicConfig(level=logging.DEBUG)
    global log
    log = logging.getLogger()

    try:
        config['username'] = os.environ['GNOC_USERNAME']
        config['password'] = os.environ['GNOC_PASSWORD']
        config['server'] = os.environ['GNOC_SERVER']
        config['realm'] = os.environ['GNOC_REALM']
        config['alertmanager_url'] = os.environ['ALERTMANAGER_URL']
    except KeyError as e:
        print(f"The {e} environment variable is not set.")
        sys.exit(1)

    alerts = get_alertmanager_alerts(config['alertmanager_url'])

    agent = AlertMonAgent(
        username    = config['username'],
        password    = config['password'],
        server      = config['server'],
        realm       = config['realm']
    )

    push_to_gnoc(alerts, agent)

if __name__ == '__main__':
    main()
