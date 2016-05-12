'''
Created on May 11, 2016

@author: agutierrez
'''
import csv
import datetime
import sys

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from sshtunnel import SSHTunnelForwarder

from create_database import Actor, Country, BASE
from database.create_database import Region, Interaction, Event


COUNTRIES = {}
ACTORS = {}
REGIONS = {}
INTERACTIONS = {}
EVENTS = {}

def populate(path, session):
    populate_countries(path, session)
    populate_actors(path, session)
    populate_regions(path, session)
    populate_interactions(path, session)
    populate_events(path, session)
    
    session.close_all()
def populate_countries(path, session):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        headers = reader.next()
        print headers
        countries = {}
        for row in reader:
            country = Country(name=row[14], gwno=row[0])
            countries[row[14]] = country
        country_id = 1
        for key in countries:
            COUNTRIES[key] = country_id
            session.add(countries[key])
            country_id = country_id + 1
        session.commit()
        print 'added all countries'
def populate_actors(path, session):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        headers = reader.next()
        print headers
        actors = {}
        for row in reader:
            if row[7]:
                actor = Actor(actor_type=row[7])
                actors[row[7]] = actor
            if row[8]:
                actor = Actor(actor_type=row[8])
                actors[row[8]] = actor
            if row[10]:
                actor = Actor(actor_type=row[10])
                actors[row[10]] = actor
            if row[11]:
                actor = Actor(actor_type=row[11])
                actors[row[11]] = actor
        progress = 0
        total = len(actors)
        for key in actors:
            key
            session.add(actors[key])
            session.commit()
            progress = progress + 1
            ACTORS[key] = progress
            print "Ingested %s out of %s actors." % (progress, total)
        print 'added all actors'

def populate_interactions(path, session):
    session.add(Interaction(interaction_type="Government or mutinous force"))
    session.add(Interaction(interaction_type="Rebel force"))
    session.add(Interaction(interaction_type="Political militia"))
    session.add(Interaction(interaction_type="Ethnic militia"))
    session.add(Interaction(interaction_type="Rioters"))
    session.add(Interaction(interaction_type="Protesters"))
    session.add(Interaction(interaction_type="Civilians"))
    session.add(Interaction(interaction_type="Outside/external force (e.g. UN)"))
    session.commit()

def populate_regions(path, session):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        headers = reader.next()
        print headers
        regions = {}
        for row in reader:
            if row[15]:
                region = Region(name=row[15],country_id=COUNTRIES[row[14]])
                regions[row[15]] = region
            if row[16]:
                region = Region(name=row[16],country_id=COUNTRIES[row[14]])
                regions[row[16]] = region
            if row[17]:
                region = Region(name=row[17],country_id=COUNTRIES[row[14]])
                regions[row[17]] = region
            if row[18]:    
                region = Region(name=row[18],country_id=COUNTRIES[row[14]])
                regions[row[18]] = region
        progress = 0
        total = len(regions)
        region_id = 1
        for key in regions:
            REGIONS[key] = region_id
            #session.add(regions[key])
            #session.commit()
            progress = progress + 1
            region_id = region_id + 1
            print "Ingested %s out of %s regions." % (progress, total)
        print 'added all regions'
        
def populate_events(path, session):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        headers = reader.next()
        print headers
        events = {}
    
        for row in reader:
            if row[1]:
                event_id_cnty = row[1]
            else:
                event_id_cnty = ''
            if row[2]:
                event_id_no_cnty = row[2]
            else:
                event_id_no_cnty = ''
            if row[3]:
                event_date = datetime.datetime.strptime(row[3], "%d/%m/%Y").date()
            else:
                event_date = ''
            if row[5]:    
                time_precision = row[5]
            else:
                time_precision = ''
            if row[6]:    
                event_type = row[6]
            else:
                event_type = ''
            if row[7]:    
                actor_1_id = ACTORS[row[7]]
            else:
                actor_1_id = ''
            if row[8]:    
                actor_ally_1_id = ACTORS[row[8]]
            else:
                actor_ally_1_id = ''
            if row[9]:    
                inter_1_id = ACTORS[row[9]]
                inter_1_id = ''
            if row[10]:    
                actor_2_id = ACTORS[row[10]]
            else:
                actor_2_id = ''
            if row[11]:    
                actor_ally_2_id = ACTORS[row[11]]
            if row[12]:    
                inter_2_id = ACTORS[row[12]]
            else:
                inter_2_id = ''
            if row[13]:    
                interaction = row[13]
            else:
                interaction = ''
            if row[14]:    
                country_id = COUNTRIES[row[14]]
            else:
                country_id = ''
            if row[15]:    
                admin_1_id = REGIONS[row[15]]
            else:
                admin_1_id = ''
            if row[16]:    
                admin_2_id = REGIONS[row[16]]
            else:
                admin_2_id = ''
            if row[17]:    
                admin_3_id = REGIONS[row[17]]
            else:
                admin_3_id = ''
            if row[18]:    
                location_id = REGIONS[row[18]]
            else:
                location_id = ''
            if row[19]:    
                latitud = row[19]
            else:
                latitud = ''
            if row[20]:    
                longitud = row[20]
            else:
                longitud = ''
            if row[21]:    
                geo_precis = row[21]
            else:
                geo_precis = ''
            if row[22]:    
                source = row[22]
            else:
                source = ''
            if row[23]:    
                notes = row[23]
            else:
                notes = ''
            if row[24]:    
                fatalities = row[24]
            else:
                fatalities = ''
            events[event_id_cnty] = Event(
                                event_id_cnty = event_id_cnty,
                                event_id_no_cnty = event_id_no_cnty,
                                event_date = event_date,
                                time_precision = time_precision,
                                event_type = event_type,
                                actor_1_id=actor_1_id,
                                actor_ally_1_id=actor_ally_1_id,
                                inter_1_id=inter_1_id,
                                actor_2_id=actor_2_id,
                                actor_ally_2_id=actor_ally_2_id,
                                inter_2_id=inter_2_id,
                                interaction=interaction,
                                country_id = country_id,
                                admin_1_id = admin_1_id,
                                admin_2_id = admin_2_id,
                                admin_3_id = admin_3_id,
                                location_id = location_id,
                                latitud = latitud,
                                longitud = longitud,
                                geo_precis = geo_precis,
                                source = source,
                                notes = notes,
                                fatalities = fatalities)  
            
                
        progress = 0
        total = len(events)
        region_id = 1
        for key in events:
            EVENTS[key] = event_id_cnty
            session.add(events[key])
            session.commit()
            progress = progress + 1
            region_id = region_id + 1
            print "Ingested %s out of %s events." % (progress, total)
        print 'added all events'
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
        klass = sessionmaker(bind=ENGINE)
        
        session = klass()
        
        populate(sys.argv[6], session)