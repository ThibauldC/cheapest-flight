import streamlit as st
import json
import requests
import datetime
import time
import pandas as pd

with open('airline_id.json') as f:
    airline_data = json.load(f)

date_format = '%d/%m/%Y'
no_of_adults = str(int(st.sidebar.number_input('Number of persons', step=1.0)))
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

max_fly_duration = '8'
date_return_from = ''
date_return_to = ''
no_of_children = '0'
no_of_infants = '0'
max_stopovers = '1'
stopover_from = '1:00'
excluded_airlines = 'FR'

request_string = 'https://api.skypicker.com/flights?fly_from=' + fly_from + '&fly_to=' + fly_to + '&date_from=' + date_from + '&date_to=' + date_to + '&max_fly_duration=' + max_fly_duration + '&nights_in_dst_from=' + min_nights_in_destination + '&nights_in_dst_to=' + max_nights_in_destination + '&return_from=' + date_return_from + '&return_to=' + date_return_to + '&flight_type=' + flight_type + '&adults=' + no_of_adults + '&children=' + no_of_children + '&infants=' + no_of_infants + '&curr=EUR' + '&max_stopovers=' + max_stopovers + "&stopover_from=" + stopover_from + '&select_airlines=' + excluded_airlines + '&select_airlines_exclude=True' + '&partner=picky'
print(request_string)


def make_request():
    return requests.get(request_string)


def get_airlines(airline_code):
    airlines = ''
    if airline_code:
        airlines = airline_data[airline_code]
    return airlines


def get_route(route):
    stops = []
    for stop in route:
        fly_from_stop = stop['flyFrom']
        fly_to_stop = stop['flyTo']
        departure = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stop['dTime']))
        arrival = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stop['aTime']))
        operating_carrier = get_airlines(stop['operating_carrier'])
        airline = get_airlines(stop['airline'])
        stops.append({"fly_from": fly_from_stop, "fly_to": fly_to_stop, "departure": departure, "arrival": arrival,
                      "airline": airline, "operating_airline": operating_carrier})
    return stops


def get_coords(route):
    coords = [{"lon_from": stop['lngFrom'], "lat_from": stop['latFrom'], "lon_to": stop['lngTo'], "lat_to": stop['latTo']} for stop in route]
    return coords

def calculate_route(flights):
    pass

DATETIMEFORMAT = '%Y-%m-%d %H:%M:%S'
min_price = 10000
used_airlines_for_route = []
#routes = pd.DataFrame()
#coords = pd.DataFrame()
#to_duration = 0
#return_duration = 0
response = make_request()
if 'data' not in response.json().keys():
    st.write("No data found for this request, please retry with other parameters!")
else:
    if all_suggestions := response.json()['data']:
        print(all_suggestions)
        # TODO put all here under in separate function calculate_route
        for flights in all_suggestions:
            if flights['price'] < min_price:
                min_price = flights['price']
                to_duration = flights['fly_duration']
                return_duration = flights['return_duration']
                routes = get_route(flights['route'])
                coords = get_coords(flights['route'])

        if routes: #can be removed due to if statement above
            for i in range(len(routes) - 1):
                layover = datetime.datetime.strptime(routes[i + 1]['departure'], DATETIMEFORMAT) - datetime.datetime.strptime(
                    routes[i]['arrival'], DATETIMEFORMAT)
                if layover > datetime.timedelta(days=1):
                    layover = None
                else:
                    layover = str(layover)
                routes[i]["layover"] = layover
            routes[len(routes) - 1]["layover"] = None

            for i in range(len(routes)):
                routes[i]["duration_to"] = to_duration
                routes[i]["duration_return"] = return_duration

        st.write(f"Min price: {min_price}")
        routes_df = pd.DataFrame(routes)
        coords = pd.DataFrame(coords)
        st.dataframe(routes_df)
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
