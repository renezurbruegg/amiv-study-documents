# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point for the server application."""
import json
import logging
import os
import re
import traceback
from datetime import date
from datetime import timedelta, datetime
from functools import update_wrapper

from bson.objectid import ObjectId
from flask import make_response
from flask import request, current_app, Flask
from flask_cors import CORS
from flask_jwt_simple import (
    JWTManager
)
from pylogging import HandlerType, setup_logger
from pymongo import MongoClient

from .config import CONFIG
from .http_codes import Status

logger = logging.getLogger(__name__)
setup_logger(log_directory='./logs', file_handler_type=HandlerType.ROTATING_FILE_HANDLER, allow_console_logging = True, console_log_level  = logging.DEBUG, max_file_size_bytes = 1000000)

app = Flask(__name__)
# Load Configuration for app. Secret key etc.
config_name = os.getenv('FLASK_CONFIGURATION', 'default')

app.config.from_object(CONFIG[config_name])

# Set Cors header. Used to accept connections from browser using XHTTP requests.
CORS(app, headers=['Content-Type'])
jwt = JWTManager(app)

mensaMapping = {}

mydb = MongoClient("localhost", 27017)["amivmat"]
db = mydb['links']

def main():
    """Main entry point of the app. """

    logger.info("starting server")
    try:
        app.run(debug = True, host = app.config["IP"], port = app.config["PORT"])
        logger.info("Server started. IP: " + str(app.config["IP"]) + " Port: " + str(app.config["PORT"]))
    except Exception as exc:
        logger.error(exc)
        logger.exception(traceback.format_exc())
    finally:
        pass

@jwt.jwt_data_loader
def add_claims_to_access_token(identity):
    """ Used to allow CORS Request from any source"""
    now = datetime.utcnow()
    return {
        'exp': now + current_app.config['JWT_EXPIRES'],
        'iat': now,
        'nbf': now,
        'sub': identity,
        'roles': 'Admin'
    }


def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    # use str instead of basestring if using Python 3.x
    if headers is not None and not isinstance(headers, list):
        headers = ', '.join(x.upper() for x in headers)
    # use str instead of basestring if using Python 3.x
    if not isinstance(origin, list):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Content-type'] = "application/json"
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/mat/<dep>/<sem>/<name>', methods=['GET', 'OPTIONS'])
@crossdomain(origin = '*')
def getForDepSemName(dep, sem, name):
    """
    ### API Path   `/api/getAllMensas`
    ### Request Type: `GET`
    Returns all mensafor the actual week

    for menu in collection.find(filterObj).sort("mensaName"):

        if(menu["mensaName"] in mensaMap):
            if(mensa is None or mensa.name != menu["mensaName"]):
                mensa = mensaMap[menu["mensaName"]]
            if(mensa != None):
                mensa.addMenuFromDb(menu, date, db)"""
    list = []
    for e in db.find({'fach' : name}):
        print(e)
        del e['_id']
        list.append(e)

    for e in db.find({'title' : {'$regex':name, '$options' : 'i'}, 'master':True}):
        if(e not in list):
            del e['_id']
            list.append(e)
    return json.dumps(list), Status.HTTP_OK_BASIC


def parseToApiResponse(data):
    print(data)
    year = data['year']
    numbers = re.findall('\d+',year)
    print(numbers)
    if(len(numbers) > 0 and len(numbers[0]) < 4):
        print("year missmatch for " + str(numbers[0]))
        if(numbers[0] > "19"):
            year = "19"+ numbers[0];
        else:
            year = "20"+numbers[0];
    files = []
    for (n,l) in data['files']:
        files.append({"file": l, "name": n})

    obj = {
        "author":data['author'],
        'course_year': year,
        'files': files,
        'lecture':data['fach'],
        'professor': '',
        'title': data['title'],
        'type': data['category']
    }

    return obj

@app.route('/mat/forName/<name>', methods=['GET', 'OPTIONS'])
@crossdomain(origin = '*')
def getForName(name):
    """
    ### API Path   `/api/getAllMensas`
    ### Request Type: `GET`
    Returns all mensafor the actual week

    for menu in collection.find(filterObj).sort("mensaName"):

        if(menu["mensaName"] in mensaMap):
            if(mensa is None or mensa.name != menu["mensaName"]):
                mensa = mensaMap[menu["mensaName"]]
            if(mensa != None):
                mensa.addMenuFromDb(menu, date, db)"""
    list = []
    for e in db.find({'fach' : name}):
        list.append(parseToApiResponse(e))

    for e in db.find({'title' : {'$regex':name.strip(), '$options' : 'i'}}):
        e2 = parseToApiResponse(e)
        if(e2 not in list):
            list.append(e2)


    return json.dumps(list), Status.HTTP_OK_BASIC
