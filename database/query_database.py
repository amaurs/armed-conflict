'''
Created on May 13, 2016

@author: agutierrez
'''
import sys

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import extract
from sqlalchemy.sql import func
#from sshtunnel import SSHTunnelForwarder

from database.create_database import Country, Event


class Query(object):
    '''
    classdocs
    '''


    def __init__(self, engine):
        '''
        Constructor
        '''
        self.engine = engine
        klass = sessionmaker(bind=self.engine)
        self.session = klass()
            
    def get_countries(self):
        print 'nothing wrong here'
        countries = {}
        for country in self.session.query(Country):
            countries[country.country_id] = [country.gwno,country.name]
        
        return countries
    def get_all_events(self):
        events = []
        for event in self.session.query(Event).limit(400):
            feature = {}
            feature["type"] ="Feature"
            feature["geometry"] = {"type": "Point", "coordinates": [event.longitud,event.latitud]}
            feature["properties"] = {"marker-color": "#9c89cc"}
            events.append(feature)
        return events
    def get_events_center(self, country, year):
        centers = []
        for center in self.session.query(func.avg(Event.longitud).label('longitud'),func.avg(Event.latitud).label('latitud')).filter(extract('year', Event.event_date) == year).filter(Event.country_id == country):
            centers.append(center.longitud)
            centers.append(center.latitud)
        if len(centers) == 0:
            return [23.992075732837595,4.755856763705008]
        return centers
    def get_events(self, country, year):
        events = []
        for event in self.session.query(Event.longitud,Event.latitud, Event.event_id_cnty,Event.fatalities,Event.notes).filter(extract('year', Event.event_date) == year).filter(Event.country_id == country):
            feature = {}
            feature["type"] ="Feature"
            feature["geometry"] = {"type": "Point", "coordinates": [event.longitud,event.latitud]}
            feature["properties"] = {"title": event.event_id_cnty,
                                     "description": "%s. Fatalities: %s" % (event.notes, event.fatalities),
                                     "marker-symbol": "hospital",
                                     "marker-color": "#ff4136"}
            events.append(feature)
        return events
    def get_fatalities_center(self, fatalities):
        centers = []
        for center in self.session.query(func.avg(Event.longitud).label('longitud'),func.avg(Event.latitud).label('latitud')).filter(Event.fatalities > fatalities):
            centers.append(center.longitud)
            centers.append(center.latitud)
        if len(centers) == 0:
            return [23.992075732837595,4.755856763705008]
        return centers
    def get_fatalities(self, fatalities):
        events = []
        for event in self.session.query(Event.longitud,Event.latitud, Event.fatalities).filter(Event.fatalities > fatalities):
            feature = {}
            feature["type"] ="Feature"
            feature["geometry"] = {"type": "Point", "coordinates": [event.longitud,event.latitud]}
            feature["properties"] = {"title": event.fatalities,
                                     "marker-color": "#ff4136"}
            events.append(feature)
        return events
    def get_countries_fatalities(self):
        
        with self.engine.connect() as connection:
    
            result = []
            result.append(['id','events','fatalities', 'fatalities','events'])
            for data in connection.execute('select c.name as name,f.events as events,f.fatalities as fatalities from fatalities as f,country as c where f.country_id=c.country_id;'):
        
                result.append([data.name,data.events,data.fatalities,data.fatalities,data.events])
                
            
        return result
            