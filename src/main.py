from FlightRadar24.api import FlightRadar24API
from FlightRadar24.flight import Flight

from plane_pic import get_last_photo_url

import pdb
import json

# json file for icao -> model name
PLANE_NAMES = 'planes.json'
OPERATORS = 'airline-codes/airlines.json'
AIRPORTS = 'Airports/airports.json'

# airport code
sea = 'SEA'
# northwest zone
nw = 'na_nw'
nw_bounds = {'br_x': -96.75,'br_y': 38.32,'tl_x': -134.13,'tl_y': 54.12}

# only look for planes in this vertical space
vert_bounds = [1500, 3500]

print('starting up...')

with open(PLANE_NAMES, 'r') as f:
    planes = json.load(f)

with open(AIRPORTS, 'r') as f:
    raw_airports = json.load(f)
    airports = {raw_airports[a]['iata']: raw_airports[a]['name'] for a in raw_airports.keys()}

with open(OPERATORS, 'r') as f:
    raw_oper = json.load(f)
    airlines = {o['iata']: o['name'] for o in raw_oper}

def get_model(icao):
    try:
        return planes[icao]
    except:
        return None

def get_sea_flights(fr_api):
    nw_flights = fr_api.get_flights(bounds=fr_api.get_bounds(nw_bounds))
    print(f'there are {len(nw_flights)} total flights in nw north american airspace rn')

    sea_flights = []
    for flight in nw_flights:
        if flight.destination_airport_iata == sea:
            sea_flights.append(flight)
    
    return sea_flights

def print_flight(flight):
    plane = get_model(flight.aircraft_code)
    print(f'your plane is probably:')
    print(f'\tflight: #{flight.number}, from {airports.get(flight.origin_airport_iata, flight.origin_airport_iata)}')
    print(f'\tplane: {plane}')
    print(f'\taltitude: {flight.get_altitude()}')
    print(f'\theading: {flight.get_heading()}')
    print(f'\tlocation: [{flight.latitude}, {flight.longitude}]')
    print(f'\toperator: {airlines.get(flight.airline_iata, flight.airline_iata)}')

if __name__ == '__main__':
    fr_api = FlightRadar24API()
    sea_flights = sorted(get_sea_flights(fr_api), key=lambda x: x.altitude)
    for flight in sea_flights:
        if vert_bounds[0] < int(flight.get_altitude().split()[0]) < vert_bounds[1]:
            print_flight(flight)

