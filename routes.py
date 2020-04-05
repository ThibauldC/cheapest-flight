from dataclasses import dataclass
from typing import Dict, Any, List
import json
import time
import datetime

import pandas as pd

DATETIMEFORMAT = '%Y-%m-%d %H:%M:%S'

with open('airline_id.json') as f:
    airline_data = json.load(f)


def get_airlines(airline_code):
    airlines = ''
    if airline_code:
        airlines = airline_data[airline_code]
    return airlines


class Route:
    def __init__(self, best_route: Dict[str, Any]):
        self.price: float = best_route['price']
        self.duration: str = best_route['fly_duration']
        self.flights: List[Flight] = [
            Flight(stop['flyFrom'], stop['flyTo'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stop['dTime'])),
                   time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stop['aTime'])),
                   get_airlines(stop['operating_carrier']), get_airlines(stop['airline'])) for stop in
            best_route['route']]
        self.coords: List[FlightCoordinates] = [
            FlightCoordinates(stop['lngFrom'], stop['latFrom'], stop['lngTo'], stop['latTo']) for stop in
            best_route['route']]
        self.return_duration: str = "0h"
        if 'return_duration' in best_route.keys():
            self.return_duration = best_route['return_duration']

    def _calculate_layovers(self) -> List[str]:
        all_layovers = [Layover(self.flights[i], self.flights[i + 1]) for i in range(len(self.flights) - 1)]
        all_layovers = [layover.layover_time for layover in all_layovers]
        all_layovers.append(str(datetime.timedelta(seconds=0)))
        return all_layovers

    def to_df(self) -> pd.DataFrame:
        departures = [flight.start for flight in self.flights]
        destinations = [flight.destination for flight in self.flights]
        departure_times = [flight.departure for flight in self.flights]
        arrival_times = [flight.arrival for flight in self.flights]
        carriers = [flight.operating_carrier for flight in self.flights]
        airlines = [flight.airline for flight in self.flights]
        layovers = self._calculate_layovers()
        return pd.DataFrame(
            {"fly_from": departures, "fly_to": destinations, "departure": departure_times, "arrival": arrival_times,
             "airline": carriers, "operating_airline": airlines, "layover": layovers})

    def get_coords(self) -> Dict[str, List[float]]:
        all_lon_from, all_lat_from = [coord.lon_from for coord in self.coords], [coord.lat_from for coord in self.coords]
        all_lon_to, all_lat_to = [coord.lon_to for coord in self.coords], [coord.lat_to for coord in self.coords]
        return {"lon_from": all_lon_from, "lat_from": all_lat_from, "lon_to": all_lon_to, "lat_to": all_lat_to}


@dataclass
class Flight:
    start: str
    destination: str
    departure: str
    arrival: str
    operating_carrier: str
    airline: str


@dataclass
class FlightCoordinates:
    lon_from: float
    lat_from: float
    lon_to: float
    lat_to: float


class Layover:
    def __init__(self, flight1, flight2):
        self.layover_time: str = self.calculate_layover(flight1, flight2)

    @staticmethod
    def calculate_layover(flight1, flight2) -> str:
        layover = datetime.datetime.strptime(flight2.departure, DATETIMEFORMAT) - datetime.datetime.strptime(
            flight1.arrival, DATETIMEFORMAT)
        if layover > datetime.timedelta(days=1):
            layover = datetime.timedelta(seconds=0)

        return str(layover)
