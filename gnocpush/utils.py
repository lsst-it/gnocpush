"""Assorted utility functions."""

import logging

from dateutil import parser

log = logging.getLogger(__name__)


def sanitize_severity(severity):
    s = 'Unknown'

    # match statement doesn't seem to have an easy way to do case insensitive
    # matching, so we force everything to lower case.
    match severity.lower():
        case 'critical' | 'alert': s = 'Critical'
        case 'major' | 'warning': s = 'Major'
        case 'minor' | 'info': s = 'Minor'
        case 'unknown': s = 'Unknown'
        case 'ok': s = 'OK'

    log.debug(f'severity: {severity} -> {s}')

    return s


def alertmanager_to_gnoc(alert):
    sev = sanitize_severity(alert['labels'].get('severity', 'Unknown'))
    desc = alert['annotations'].get('description', 'Unknown')
    start_time = int(parser.isoparse(alert['startsAt']).timestamp())

    data = {
        'node_name': alert['labels'].get('node_name', 'Unknown'),
        'device': alert['labels'].get('device'),
        'service_name': alert['labels'].get('service_name', 'Unknown'),
        'severity': sev,
        'description': desc,
        'start_time': start_time,
    }

    return data
