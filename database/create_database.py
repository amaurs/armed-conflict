'''
Created on May 10, 2016

@author: agutierrez
'''

import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


#from sshtunnel import SSHTunnelForwarder
BASE = declarative_base()

class Country(BASE):
    __tablename__ = 'country'
    country_id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)
    gwno = Column(Integer())
class Actor(BASE):
    __tablename__ = 'actor'
    actor_id = Column(Integer, primary_key=True)
    actor_type = Column(String(500))
class Region(BASE):
    __tablename__ = 'region'
    region_id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)
    country_id = Column(Integer, ForeignKey('country.country_id'))
    country = relationship('Country') 
class Interaction(BASE):
    __tablename__ = 'interaction'
    interaction_id = Column(Integer, primary_key=True)
    interaction_type = Column(String(100))
class Event(BASE):
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True)
    event_id_cnty = Column(String())
    event_id_no_cnty = Column(Integer())
    event_date = Column(Date())
    time_precision = Column(Integer())
    event_type = Column(String(100))
    actor_1_id = Column(Integer, ForeignKey('actor.actor_id'))
    actor_ally_1_id = Column(Integer, ForeignKey('actor.actor_id'))
    actor_2_id = Column(Integer, ForeignKey('actor.actor_id'))
    actor_ally_2_id = Column(Integer, ForeignKey('actor.actor_id'))
    
    actor_1 = relationship('Actor', foreign_keys=actor_1_id)
    actor_ally_1 = relationship('Actor', foreign_keys=actor_ally_1_id)
    actor_2 = relationship('Actor', foreign_keys=actor_2_id)
    actor_ally_2 = relationship('Actor', foreign_keys=actor_ally_2_id)
    
    
    inter_1_id = Column(Integer, ForeignKey('interaction.interaction_id'))
    inter_2_id = Column(Integer, ForeignKey('interaction.interaction_id'))
    inter_1 = relationship('Interaction', foreign_keys=inter_1_id)
    inter_2 = relationship('Interaction', foreign_keys=inter_2_id)
    
    interaction = Column(Integer)
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