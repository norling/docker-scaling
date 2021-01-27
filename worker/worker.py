#!/usr/bin/env python3
"""
Simple web server that accepts POST requests with work to perform.
"""

import time
import random
from flask import Flask, jsonify

APP = Flask(__name__)
APP.status = 'idle'

@APP.route('/status')
def status():
    """
    Returns the current status of the worker
    """
    return jsonify(status=APP.status)


@APP.route('/', methods=['POST'])
def main():
    """
    Accepts POST requests to perform "work". In this case, the work is just
    waiting and then returning a random number between 0 and 100.
    """
    if APP.status != 'idle':
        return jsonify(status='fail', result='already running')
    APP.status='working'

    time.sleep(5)
    result = random.randint(0,100)

    APP.status='idle'
    return jsonify(status='success', result=result)
