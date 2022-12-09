#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Aug 23 20:23:03 2019

@author: smkj33
"""
import pymysql
from app import app
from content_recommendation.parameters.db_config import *

from flask import jsonify
from flask import flash, request

from content_recommender import *
import pandas as pd


@app.route('/content-reco-cosine')
def content_recommender_cosine():
    try:

        req_data = request.get_json()
        resp = reco_catcher_cosine(req_data)
        resp = resp.to_json(orient='records')
        return resp

    except Exception as e:
        print(e)


@app.route('/content-reco-ts')
def content_recommender_ts_ss():
    try:

        req_data = request.get_json()
        resp = reco_catcher_ts_ss(req_data)
        resp = resp.to_json(orient='records')
        return resp

    except Exception as e:
        print(e)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run()
