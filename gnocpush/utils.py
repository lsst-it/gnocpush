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
        case 'major' | 'warning': s ='Major'
        case 'minor' | 'info': s = 'Minor'
        case 'unknown': s = 'Unknown'
        case 'ok': s ='Ok'

    log.debug(f'severity: {severity} -> {s}')

    return s