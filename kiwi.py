import streamlit as st
import json
import pandas as pd
import pydeck as pdk

from request import Request
from routes import Route

with open('airline_id.json') as f:
    airline_data = json.load(f)


date_format = '%d/%m/%Y'
no_of_adults = st.sidebar.number_input('Number of persons', step=1.0)
date_from = st.sidebar.date_input('Min departure date')
date_to = st.sidebar.date_input('Max departure date')
fly_from = st.sidebar.text_input('Departure airport code (can be multiple)')
fly_to = st.sidebar.text_input('Arrival airport code (can be multiple)')
flight_type = st.sidebar.radio('One way/Round trip?', ('oneway', 'round'))
min_nights_in_destination, max_nights_in_destination = '', ''
if flight_type == 'round':
    min_nights_in_destination = str(int(st.sidebar.number_input('Min number of days in destination', step=1.0)))
    max_nights_in_destination = str(int(st.sidebar.number_input('Max number of days in destination', step=1.0)))

flight_request = Request(int(no_of_adults), date_from, date_to, fly_from, fly_to, flight_type, min_nights_in_destination, max_nights_in_destination)
response = flight_request.make_request()
if response.all_routes:
    best_route: Route = response.get_cheapest_route()
    st.write(f"Min price: {best_route.price}")
    routes_df = best_route.to_df()
    coords = pd.DataFrame(best_route.get_coords())
    st.dataframe(routes_df)
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=47.457809,
            longitude=4.394531,
            zoom=2),
        layers=[
            pdk.Layer(
                'ArcLayer',
                data=coords,
                get_source_position=['lon_from', 'lat_from'],
                get_target_position=['lon_to', 'lat_to'],
                get_color=[255, 0, 0]
            ),
        ],
    ))
else:
    st.write("No data found for this request, please retry with other parameters!")
