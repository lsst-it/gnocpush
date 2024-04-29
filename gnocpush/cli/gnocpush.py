#!/bin/env python3

import argparse
import json
import logging

from flask import Flask, request, jsonify
from gnocpush.envdefault import EnvDefault
from gnocpush import Pusher
from prometheus_flask_exporter import PrometheusMetrics
from waitress import serve

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4 MB
metrics = PrometheusMetrics(app)


@app.route('/alerts', methods=['POST'])
def push_endpoint():
    # Get the data from the request
    data = request.get_json()

    log.debug(f"Received data: {json.dumps(data)}")

    try:
        yeeter.push(data['alerts'])
    except Exception as e:
        log.error(f"Failed to push alerts to GNOC: {str(e)}")
        return jsonify(error=str(e)), 502

    # Return a response
    return {'status': 'success'}


@app.route('/healthz', methods=['GET'])
@metrics.do_not_track()
def healthz():
    return {'status': 'ok'}


def parse_args():
    """Parse command-line arguments"""

    parser = argparse.ArgumentParser(
        prog='gnocpush',
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
        '-r', '--realm', action=EnvDefault, envvar='GNOC_REALM',
        help='Specify the GNOC realm'
    )
    parser.add_argument(
        '-l', '--listen',
        default='localhost:8080',
        help='Specify the address:port to listen on'
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
    logging.getLogger('waitress').setLevel(log_level)

    global log
    log = logging.getLogger(__name__)

    global yeeter
    yeeter = Pusher({
        'username': args.user,
        'password': args.password,
        'server': args.server,
        'realm': args.realm
    })

    serve(app, listen=args.listen)


if __name__ == '__main__':
    main()
