from dataclasses import dataclass, field
from datetime import datetime

import json
import requests

from routes import Route

DATE_FORMAT = '%d/%m/%Y'
max_fly_duration = '8'
date_return_from = ''
date_return_to = ''
no_of_children = '0'
no_of_infants = '0'
max_stopovers = '1'
stopover_from = '1:00'
excluded_airlines = 'FR'


class Request:
    def __init__(self, no_of_adults: int, date_from: datetime, date_to: datetime, fly_from: str, fly_to:str, flight_type: str, min_nights: str, max_nights: str):
        self.no_of_adults: str = str(no_of_adults)
        self.date_from: str = date_from.strftime(DATE_FORMAT)
        self.date_to: str = date_to.strftime(DATE_FORMAT)
        self.fly_from: str = fly_from
        self.fly_to: str = fly_to
        self.flight_type: str = flight_type
        self.min_nights_in_destination, self.max_nights_in_destination = min_nights, max_nights

    def make_request(self):
        #request_string = f'https://api.skypicker.com/flights?fly_from={self.fly_from}&fly_to={self.fly_to}&date_from={self.date_from}&date_to={self.date_to}&max_fly_duration={max_fly_duration}&nights_in_dst_from={self.min_nights_in_destination}&nights_in_dst_to={self.max_nights_in_destination}&return_from={date_return_from}&return_to={date_return_to}&flight_type={self.flight_type}&adults={self.no_of_adults}&children={no_of_children}&infants={no_of_infants}&curr=EUR&max_stopovers={max_stopovers}&stopover_from={stopover_from}&select_airlines={excluded_airlines}&select_airlines_exclude=True&partner=picky '
        request_string = 'https://api.skypicker.com/flights?fly_from=AMS&fly_to=LAX&date_from=03/09/2020&date_to=01/10/2020&max_fly_duration=20&nights_in_dst_from=14&nights_in_dst_to=24&return_from=&return_to=&flight_type=round&adults=2&children=0&infants=0&curr=EUR&max_stopovers=1&stopover_from=1:00&select_airlines=FR&select_airlines_exclude=True&partner=picky'
        print(request_string)
        response = requests.get(request_string)
        if 'data' in response.json().keys():
            return Response(response.json()['data'])
        else:
            return Response([])


@dataclass
class Response:
    all_routes: field(default_factory=list)

    def get_cheapest_route(self) -> Route:
        return Route(min(self.all_routes, key=lambda route: route['price']))
