from datetime import timedelta
from functools import update_wrapper
import json
import os
import sys

from flask import Flask, jsonify
from flask.globals import current_app, request
from flask.helpers import make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import create_engine

from database.create_database import Country
from database.query_database import Query


app = Flask(__name__)
query = None


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/')
@crossdomain(origin='*')
def hello():
            engine_url = 'postgres://%s:%s@localhost/armed-conflict' %(sys.argv[1], sys.argv[2])
            engine = create_engine(engine_url)
            
            query = Query(engine)
            countries = query.get_countries()
            print countries
            return jsonify({'countries': countries}, indent=4)

@app.route('/events')
@crossdomain(origin='*')
def all_events():
            engine_url = 'postgres://%s:%s@localhost/armed-conflict' %(sys.argv[1], sys.argv[2])
            engine = create_engine(engine_url)
            
            query = Query(engine)
            events = query.get_all_events()
            
            result = { "type": "FeatureCollection",
                "features": events
             }
            
            return jsonify(result)
        
@app.route('/events/<country>/<year>')
@crossdomain(origin='*')
def events(country,year):
            engine_url = 'postgres://%s:%s@localhost/armed-conflict' %(sys.argv[1], sys.argv[2])
            
            print engine_url
            try:
                engine = create_engine(engine_url)
                
                query = Query(engine)
                events = query.get_events(country,year)
                center = query.get_events_center(country, year)
                result = { "type": "FeatureCollection",
                    "features": events,
                    "center":center 
                 }
                
                return jsonify(result)
            except Exception as inst:
                print type(inst)     # the exception instance
                print inst.args      # arguments stored in .args
                print inst           # __str__ allows args to be printed directly
                return "<h1>error</h1>"
            
@app.route('/fatalities/<fatalities>')
@crossdomain(origin='*')
def fatalities(fatalities):
            engine_url = 'postgres://%s:%s@localhost/armed-conflict' %(sys.argv[1], sys.argv[2])
            
            print engine_url
            try:
                engine = create_engine(engine_url)
                
                query = Query(engine)
                events = query.get_fatalities(fatalities)
                center = query.get_fatalities_center(fatalities)
                result = { "type": "FeatureCollection",
                    "features": events,
                    "center":center 
                 }
                
                return jsonify(result)
            except Exception as inst:
                print type(inst)     # the exception instance
                print inst.args      # arguments stored in .args
                print inst           # __str__ allows args to be printed directly
                return "<h1>error</h1>"
@app.route('/bubble')
@crossdomain(origin='*')            
def get_countries_fatalities():
            engine_url = 'postgres://%s:%s@localhost/armed-conflict' %(sys.argv[1], sys.argv[2])
            
            print engine_url
            try:
                engine = create_engine(engine_url)
                
                query = Query(engine)
                events = query.get_countries_fatalities()
                return jsonify(results=events)
            except Exception as inst:
                print type(inst)     # the exception instance
                print inst.args      # arguments stored in .args
                print inst           # __str__ allows args to be printed directly
                return "<h1>error</h1>"
    

@app.route('/<name>')
def hello_name2(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run(host='0.0.0.0')