import logging

import pandas as pd
from utils.get_times import get_times

from normalizers.aero_databox_normalizer import normalize_flights_infos
from normalizers.open_weather_normalizer import normalize_open_weather_response
from service.aero_databox_api import AeroDataBox
from service.mysql_db import MySQL
from service.open_weather_api import OpenWeather

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_weather(cities_df: pd.DataFrame, api=OpenWeather()) -> list[dict]:
    cities_weather = []
    for row in cities_df.itertuples():
        response = api.get_response(params=api.get_params(lat=row.latitude, lon=row.longitude, cnt=9), logger=logger)
        if not response:
            continue
        cities_weather += normalize_open_weather_response(response, row.city_id)
    return cities_weather


def get_flight_info(airports_df: pd.DataFrame, api=AeroDataBox()) -> list[dict]:
    # fight data for a airport api http url
    query_params = {"withLeg": True, "direction": "Arrival"}

    # get date of tomorrow
    start_times, end_times = get_times()

    flights_info = []
    for row in airports_df.itertuples():
        for start_time, end_time in zip(start_times, end_times):
            url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{row.airport_id}/{start_time}/{end_time}"
            response = api.get_response(url=url, params=query_params, logger=logger)
            if not response:
                continue
            flights_info += normalize_flights_infos(response, row.airport_id)
    return flights_info


def handler(event, context):
    sql_con = MySQL()

    if 'event' in event:
        match event['event']:
            case 'weather':
                # read cities_df from the sql server
                cities_df = pd.read_sql_table('cities', con=sql_con.con())

                # read cities_df from the sql server
                cities_df = cities_df.merge(pd.read_sql_table('cities_location', con=sql_con.con()), how='left')

                # update weather data on database:
                weather_df = get_weather(cities_df)
                if weather_df:
                    # truncate database
                    sql_con.truncate_df('weathers')
                    pd.DataFrame(weather_df).to_sql('weathers', if_exists='append', con=sql_con.con(), index=False)
            case 'flights':
                # read cities_df from the sql server
                airports_df = pd.read_sql_table('airports', con=sql_con.con())

                # update flights data on database:
                flights_df = get_flight_info(airports_df)
                if flights_df:
                    sql_con.truncate_df('flights')
                    pd.DataFrame(flights_df).to_sql('flights', if_exists='append', con=sql_con.con(), index=False)
            case _:
                logger.info({'statusCode': 404, 'body': 'event trigger not found'})
                return {'statusCode': 404, 'body': 'event trigger not found'}
    else:
        logger.info({'statusCode': 404, 'body': 'event not found'})
        return {'statusCode': 404, 'body': 'event not found'}

    logger.info({'statusCode': 200, 'body': 'updated weather and flight data successfully'})
    return {'statusCode': 200, 'body': 'updated weather and flight data successfully'}
