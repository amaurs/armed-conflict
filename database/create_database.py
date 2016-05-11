'''
Created on May 10, 2016

@author: agutierrez
'''

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
import csv
 
BASE = declarative_base()

class Event(BASE):
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True)
    event_id_cnty = Column(String(4))
    event_id_no_cnty = Column(Integer())
    event_date = Column(Date())
    time_precision = Column(Integer())
    event_type = Column(String(100))
    #country
    #admin_1
    #admin_2
    #admin_3 
    #location 
    latitud = Column(Float())
    longitud = Column(Float())
    geo_precis =Column(Integer())
    source = Column(String(100))
    notes = Column(String(500))
    fatalities = Column(Integer())
class Actor(BASE):
    __tablename__ = 'actor'
    actor_id = Column(Integer, primary_key=True)
    actor_type = Column(String(100))

class Country(BASE):
    __tablename__ = 'country'
    country_id = Column(Integer, primary_key=True)
    gwno = Column(Integer())
    
class Region(BASE):
    __tablename__ = 'region'
    region_id = Column(Integer, primary_key=True)
    

class Interaction(BASE):
    __tablename__ = 'interaction'
    interaction_id = Column(Integer, primary_key=True)
    #actor1
    #actor2
    

if __name__ == '__main__':
    with SSHTunnelForwarder(
        (sys.argv[1], 22),
        ssh_username=sys.argv[2],
        ssh_password=sys.argv[3],
        remote_bind_address=('127.0.0.1', 5432)
    ) as server:
        engine_url = 'postgres://%s:%s@localhost:%s/armed-conflict' %(sys.argv[4], sys.argv[5], server.local_bind_port)
        print engine_url
        ENGINE = create_engine(engine_url)
        BASE.metadata.drop_all(ENGINE)
        BASE.metadata.create_all(ENGINE)