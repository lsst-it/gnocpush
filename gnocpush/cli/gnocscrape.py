#!/bin/env python3

import argparse
import logging
import requests

from gnocpush.envdefault import EnvDefault
from gnocpush import Pusher


def get_alertmanager_alerts(url):
    r = requests.get(url)
    return r.json()


def parse_args():
    """Parse command-line arguments"""

    parser = argparse.ArgumentParser(
        prog='gnocscrape',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '-u', '--user', action=EnvDefault, envvar='GNOC_USER',
        help='Specify the GNOC username'
    )
    parser.add_argument(
        '-p', '--pass', action=EnvDefault, envvar='GNOC_PASS',
        dest='password',
        help='Specify the GNOC password'
    )
    parser.add_argument(
        '-s', '--server', action=EnvDefault, envvar='GNOC_SERVER',
        help='Specify the GNOC server'
    )
    parser.add_argument(
        '-a', '--url', action=EnvDefault, envvar='ALERTMANAGER_URL',
        help='Specify the Alertmanager URL to scrape alerts from'
    )
    parser.add_argument(
        '-v', '--verbose',
        dest='debug',
        action=argparse.BooleanOptionalAction,
        help='Enable verbose logging'
    )

    return parser.parse_args()


def main():
    args = parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level)
    global log
    log = logging.getLogger(__name__)

    yeeter = Pusher({
        'username': args.user,
        'password': args.password,
        'server': args.server,
        'realm': args.realm
    })
    alerts = get_alertmanager_alerts(args.url)
    yeeter.push(alerts)


if __name__ == '__main__':
    main()
