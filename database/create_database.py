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

class Country(BASE):
    __tablename__ = 'country'
    country_id = Column(Integer, primary_key=True)
    name = Column(String())
    gwno = Column(Integer())
class Actor(BASE):
    __tablename__ = 'actor'
    actor_id = Column(Integer, primary_key=True)
    actor_type = Column(String(100))
class Region(BASE):
    __tablename__ = 'region'
    region_id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('country.country_id'))
    country = relationship('Country') 
class Interaction(BASE):
    __tablename__ = 'interaction'
    interaction_id = Column(Integer, primary_key=True)
    interaction_type = Column(String(100))
class Event(BASE):
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True)
    event_id_cnty = Column(String(4))
    event_id_no_cnty = Column(Integer())
    event_date = Column(Date())
    time_precision = Column(Integer())
    event_type = Column(String(100))
    country_id = Column(Integer, ForeignKey('country.country_id'))
    country = relationship('Country')
    admin_1_id = Column(Integer, ForeignKey('region.region_id'))
    admin_2_id = Column(Integer, ForeignKey('region.region_id'))
    admin_3_id = Column(Integer, ForeignKey('region.region_id'))
    location_id = Column(Integer, ForeignKey('region.region_id'))
    admin_1 = relationship('Region', foreign_keys=admin_1_id)
    admin_2 = relationship('Region', foreign_keys=admin_2_id)
    admin_3 = relationship('Region', foreign_keys=admin_3_id)
    location = relationship('Region', foreign_keys=location_id)
    latitud = Column(Float())
    longitud = Column(Float())
    geo_precis =Column(Integer())
    source = Column(String(100))
    notes = Column(String(500))
    fatalities = Column(Integer())

class Conflict(BASE):
    __tablename__ = 'conflict'
    interaction_id = Column(Integer, primary_key=True)

    actor_1_id = Column(Integer, ForeignKey('actor.actor_id'))
    actor_ally_1_id = Column(Integer, ForeignKey('actor.actor_id'))
    actor_2_id = Column(Integer, ForeignKey('actor.actor_id'))
    actor_ally_2_id = Column(Integer, ForeignKey('actor.actor_id'))
    
    actor_1 = relationship('Actor', foreign_keys='actor_1_id')
    actor_ally_1 = relationship('Actor', foreign_keys='actor_ally_1_id')
    actor_2 = relationship('Actor', foreign_keys='actor_2_id')
    actor_ally_2 = relationship('Actor', foreign_keys='actor_ally_2_id')
    
    
    inter_1_id = Column(Integer, ForeignKey('interaction.interaction_id'))
    inter_2_id = Column(Integer, ForeignKey('interaction.interaction_id'))
    inter_1 = relationship('Interaction', foreign_keys='inter_1_id')
    inter_2 = relationship('Interaction', foreign_keys='inter_2_id')
    
    interaction = Column(Integer)
    event = Column(Integer, ForeignKey('event.event_id'))
    actor = relationship('Event')
    

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