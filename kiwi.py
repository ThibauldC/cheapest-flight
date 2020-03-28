from dataclasses import dataclass, field
from typing import List, Dict, Any
import streamlit as st
import json
import requests
import datetime
import time
import pandas as pd

from request import Request, Response
from routes import Route

with open('airline_id.json') as f:
    airline_data = json.load(f)


date_format = '%d/%m/%Y'
no_of_adults = st.sidebar.number_input('Number of persons', step=1.0)
date_from = st.sidebar.date_input('Min departure date').strftime(date_format)
date_to = st.sidebar.date_input('Max departure date').strftime(date_format)
fly_from = st.sidebar.text_input('Departure airport code (can be multiple)')
fly_to = st.sidebar.text_input('Arrival airport code (can be multiple)')
flight_type = st.sidebar.radio('One way/Round trip?', ('oneway', 'round'))
min_nights_in_destination, max_nights_in_destination = '', ''
if flight_type == 'round':
    min_nights_in_destination = str(int(st.sidebar.number_input('Min number of days in destination', step=1.0)))
    max_nights_in_destination = str(int(st.sidebar.number_input('Max number of days in destination', step=1.0)))

# TODO: transform request string into f-string

# max_fly_duration = '8'
# date_return_from = ''
# date_return_to = ''
# no_of_children = '0'
# no_of_infants = '0'
# max_stopovers = '1'
# stopover_from = '1:00'
# excluded_airlines = 'FR'
#
# #REQUEST_STRING = 'https://api.skypicker.com/flights?fly_from=' + fly_from + '&fly_to=' + fly_to + '&date_from=' + date_from + '&date_to=' + date_to + '&max_fly_duration=' + max_fly_duration + '&nights_in_dst_from=' + min_nights_in_destination + '&nights_in_dst_to=' + max_nights_in_destination + '&return_from=' + date_return_from + '&return_to=' + date_return_to + '&flight_type=' + flight_type + '&adults=' + no_of_adults + '&children=' + no_of_children + '&infants=' + no_of_infants + '&curr=EUR' + '&max_stopovers=' + max_stopovers + "&stopover_from=" + stopover_from + '&select_airlines=' + excluded_airlines + '&select_airlines_exclude=True' + '&partner=picky'
# REQUEST_STRING = 'https://api.skypicker.com/flights?fly_from=AMS&fly_to=LAX&date_from=03/09/2020&date_to=01/10/2020&max_fly_duration=20&nights_in_dst_from=14&nights_in_dst_to=24&return_from=&return_to=&flight_type=round&adults=2&children=0&infants=0&curr=EUR&max_stopovers=1&stopover_from=1:00&select_airlines=FR&select_airlines_exclude=True&partner=picky'
#
# class Layover:
#     def __init__(self, flight1, flight2):
#         self.layover_time: str = self.calculate_layover(flight1, flight2)
#
#     @staticmethod
#     def calculate_layover(flight1, flight2) -> str:
#         layover = datetime.datetime.strptime(flight2.departure, DATETIMEFORMAT) - datetime.datetime.strptime(
#             flight1.arrival, DATETIMEFORMAT)
#         if layover > datetime.timedelta(days=1):
#             layover = datetime.timedelta(seconds=0)
#
#         return str(layover)
#
#
# @dataclass
# class Flight:
#     start: str
#     destination: str
#     departure: str
#     arrival: str
#     operating_carrier: str
#     airline: str
#
#
# class Route:
#     def __init__(self, price: float, to_duration: datetime.time, return_duration: datetime.time, flights):
#         self.price: float = price
#         to_duration: datetime.time
#         flights: List[Flight]
#         coords: List[Dict[str, Any]]
#         return_duration: datetime.time
#         #self.flights = calculate_flights #TO BE IMPLEMENTED
#
#     def calculate_layovers(self) -> List[str]:
#         all_layovers = [Layover(self.flights[i], self.flights[i+1]) for i in range(len(self.flights) - 1)]
#         all_layovers = [layover.layover_time for layover in all_layovers]
#         all_layovers.append(str(datetime.timedelta(seconds=0)))
#         return all_layovers
#
#     def to_df(self) -> pd.DataFrame:
#         departures = [flight.start for flight in self.flights]
#         destinations = [flight.destination for flight in self.flights]
#         departure_times = [flight.departure for flight in self.flights]
#         arrival_times = [flight.arrival for flight in self.flights]
#         carriers = [flight.operating_carrier for flight in self.flights]
#         airlines = [flight.airline for flight in self.flights]
#         layovers = self.calculate_layovers()
#         return pd.DataFrame({"fly_from": departures, "fly_to": destinations, "departure": departure_times, "arrival": arrival_times,
#                            "airline": carriers, "operating_airline": airlines, "layover": layovers})
#
# def make_request():
#     print(REQUEST_STRING)
#     return requests.get(REQUEST_STRING)
#
#
# def get_airlines(airline_code):
#     airlines = ''
#     if airline_code:
#         airlines = airline_data[airline_code]
#     return airlines
#
#
# def get_flights(route) -> List[Flight]:
#     stops = [Flight(stop['flyFrom'], stop['flyTo'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stop['dTime'])),
#                     time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stop['aTime'])),
#                     get_airlines(stop['operating_carrier']), get_airlines(stop['airline'])) for stop in route]
#     return stops
#
#
# def get_coords(route):
#     coords = [{"lon_from": stop['lngFrom'], "lat_from": stop['latFrom'], "lon_to": stop['lngTo'], "lat_to": stop['latTo']} for stop in route]
#     return coords
#
#
# def calculate_route(route, flight_type) -> Route:
#     min_price = route['price']
#     to_duration = route['fly_duration']
#     flights = get_flights(route['route'])
#     coords = get_coords(route['route'])
#     return_duration = datetime.time(0, 0)
#     if flight_type == 'round':
#         return_duration = route['return_duration']
#     # TODO: calculation of flights and coords in Route class
#     return Route(min_price, to_duration, return_duration, flights)
#
# DATETIMEFORMAT = '%Y-%m-%d %H:%M:%S'
# min_price = 10000
# used_airlines_for_route = []
# response = make_request()
# if 'data' not in response.json().keys():
#     st.write("No data found for this request, please retry with other parameters!")
# else:
#     if all_suggestions := response.json()['data']:
#         for flights in all_suggestions:
#             if flights['price'] < min_price:
#                 route = calculate_route(flights, flight_type)
#
#         #TODO: add return and to duration to df
#
#         st.write(f"Min price: {route.price}")
#         routes_df = route.to_df()
#         coords = pd.DataFrame(route.coords)
#         st.dataframe(routes_df)
#         st.deck_gl_chart(
#             viewport={
#                 'latitude': 47.457809,
#                 'longitude': 4.394531,
#                 'zoom': 3
#             },
#             layers=[{
#                 'type': 'ArcLayer',
#                 'data': coords,
#                 'getLatitude': "lat_from",
#                 'getLongitude': 'lon_from',
#                 'getTargetLatitude': "lat_to",
#                 'getTargetLongitude': "lon_to"
#             }])

#TODO: Refactoring

#flight_request = Request(int(no_of_adults), date_from, date_to, fly_from, fly_to, flight_type, min_nights_in_destination, max_nights_in_destination)
flight_request = Request(2, datetime.datetime(2020,12,23, 0, 0, 0), datetime.datetime(2020,12,23, 0, 0, 0), 'TDT', 'TFD', 'round', 5, 6)
response = flight_request.make_request()
if response.all_routes:
    best_route: Route = response.get_cheapest_route()
    #print(best_route.price)
    st.write(f"Min price: {best_route.price}")
    routes_df = best_route.to_df()
    coords = pd.DataFrame(best_route.coords)
    st.dataframe(routes_df)
    #TODO: Deck GL still does not work
    st.deck_gl_chart(
        viewport={
            'latitude': 47.457809,
            'longitude': 4.394531,
            'zoom': 3
        },
        layers=[{
            'type': 'ArcLayer',
            'data': coords,
            'getLatitude': "lat_from",
            'getLongitude': 'lon_from',
            'getTargetLatitude': "lat_to",
            'getTargetLongitude': "lon_to"
        }])
else:
    st.write("No data found for this request, please retry with other parameters!")
