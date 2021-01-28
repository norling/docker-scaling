#!/usr/bin/env python3
"""
Simple web server that allows sending jobs and listing status of the worker
containers.
"""

from flask import Flask, jsonify, render_template, request

import requests

APP = Flask(__name__)
APP.template_folder = 'templates'
APP.workers = []

@APP.route('/register', methods=['POST'])
def register():
    """
    Allows worker nodes to register as available to the server.
    This is done by posting a form with json data as:
      {worker: <id>}
    """
    worker = request.json
    if worker['worker'] not in APP.workers:
        #pylint: disable=no-member
        APP.logger.info("worker %s registered", worker['worker'])
        APP.workers += [worker['worker']]

    return jsonify(msg="Thanks!")

@APP.route('/submit', methods=['POST'])
def submit():
    """
    Takes a job submission and relays it to a worker node, returning the reply
    once the work is done.
    """
    job_data = request.json
    # find an idle worker
    if len(APP.workers) == 0:
        return jsonify(status='fail', result='no workers')
    for worker in APP.workers:
        status = requests.get(f'http://{worker}:5000/status')
        if status.text != 'idle':
            continue
        response = requests.post(f'http://{worker}:5000', json=job_data)
        return response.json()

    return jsonify(status='fail', result='no idle workers')

@APP.route('/')
def main():
    """
    Serves the index template
    """
    return render_template('/index.html')
