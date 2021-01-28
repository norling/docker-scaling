#!/usr/bin/env python3
"""
Simple web server that allows sending jobs and listing status of the worker
containers.
"""

from flask import Flask, render_template, request

import requests

APP = Flask(__name__)
APP.template_folder = 'templates'


@APP.route('/submit', methods=['POST'])
def submit():
    """
    Takes a job submission and relays it to a worker node, returning the reply
    once the work is done.
    """
    job_data = request.json
    #pylint: disable=no-member
    APP.logger.info("submitting job: %s", job_data)
    response = requests.post('http://worker:5000', data=job_data)

    return response.json()

@APP.route('/')
def main():
    """
    Serves the index template
    """
    return render_template('/index.html')
