#!/usr/bin/env python3
"""
Simple web server that accepts POST requests with work to perform.
"""

import os
import time
import random
from flask import Flask, jsonify

import requests

# Start the server

APP = Flask(__name__)
APP.hostname = os.getenv('HOSTNAME')
APP.status = 'idle'
APP.server = "server"

def register(server):
    """
    Sends a registration message to the server, to let it know that there's a
    new worker available.
    """
    msg = {'worker': APP.hostname}
    response = None
    while not response or response.status != 200:
        response = requests.post(f'http://{server}:5000/register', json=msg)
        time.sleep(1)

register(APP.server)

@APP.route('/status')
def status():
    """
    Returns the current status of the worker
    """
    return APP.status


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
