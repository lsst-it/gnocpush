#!/bin/env python3

import json
import logging
import os
import sys

from flask import Flask, request, jsonify
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


def main():
    config = {}

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('waitress').setLevel(logging.DEBUG)
    global log
    log = logging.getLogger()

    try:
        config['username'] = os.environ['GNOC_USERNAME']
        config['password'] = os.environ['GNOC_PASSWORD']
        config['server'] = os.environ['GNOC_SERVER']
        config['realm'] = os.environ['GNOC_REALM']
    except KeyError as e:
        print(f"The {e} environment variable is not set.")
        sys.exit(1)

    global yeeter
    yeeter = Pusher(config)

    serve(app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
