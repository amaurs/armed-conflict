'''
Created on May 13, 2016

@author: agutierrez
'''
import sys

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import extract
from sshtunnel import SSHTunnelForwarder

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
            
    def get_countries(self):
        print 'nothing wrong here'
        klass = sessionmaker(bind=self.engine)
        session = klass()
        countries = {}
        for country in session.query(Country):
            countries[country.country_id] = [country.gwno,country.name]
        
        return countries
    def get_all_events(self):
        klass = sessionmaker(bind=self.engine)
        session = klass()
        events = []
        for event in session.query(Event).limit(400):
            feature = {}
            feature["type"] ="Feature"
            feature["geometry"] = {"type": "Point", "coordinates": [event.longitud,event.latitud]}
            feature["properties"] = {"marker-color": "#9c89cc"}
            events.append(feature)
        return events
    def get_events(self, country, year):
        klass = sessionmaker(bind=self.engine)
        session = klass()
        events = []
        for event in session.query(Event).filter(extract('year', Event.event_date) == year).filter(Event.country_id == country):
            feature = {}
            feature["type"] ="Feature"
            feature["geometry"] = {"type": "Point", "coordinates": [event.longitud,event.latitud]}
            feature["properties"] = {"marker-color": "#9c89cc"}
            events.append(feature)
        return events
if __name__ == '__main__':
    with SSHTunnelForwarder(
        (sys.argv[1], 22),
        ssh_username=sys.argv[2],
        ssh_password=sys.argv[3],
        remote_bind_address=('127.0.0.1', 5432)
        ) as server:
            engine_url = 'postgres://%s:%s@localhost:%s/armed-conflict' %(sys.argv[4], sys.argv[5], server.local_bind_port)
            engine = create_engine(engine_url)
            
            query = Query(engine)
            print query.get_events()
            