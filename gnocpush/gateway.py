#!/bin/env python3

import logging
import os
import sys

from flask import Flask, request
from gnocpush import Pusher

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4 MB


@app.route('/alerts', methods=['POST'])
def push_endpoint():
    # Get the data from the request
    data = request.get_json()

    print(data)

    yeeter.push(data)
    # Return a response
    return {'status': 'success'}


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
    except KeyError as e:
        print(f"The {e} environment variable is not set.")
        sys.exit(1)

    global yeeter
    yeeter = Pusher(config)

    app.run(port=8080)


if __name__ == '__main__':
    main()
