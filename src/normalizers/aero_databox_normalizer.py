from src.normalizers.normalizer import get_datetime


# region airport info
def get_longitude(location: dict) -> float:
    return location['lon']


def get_latitude(location: dict) -> float:
    return location['lat']


def normalize_airport_info(airport: dict, city_id: str) -> dict:
    return {
        'city_id': city_id,
        'airport_id': airport['icao'],
        'airport_name': airport['name'],
        'country_code': airport['countryCode'],
        'latitude': get_latitude(airport['location']),
        'longitude': get_longitude(airport['location']),
    }


def normalize_airports_info(response: dict, city_id: str) -> list[dict]:
    return [{} if not 'items' in response else normalize_airport_info(airport, city_id) for airport in response['items']]


# endregion


# region normalize flight data


def get_local_arrival_time(arrival_time) -> str:
    return get_datetime(arrival_time['local'])


def get_arrival_info(arrival: dict, flight_no: str, airport_id: str, departure_city: str) -> dict:
    return {
        'airport_id': airport_id,
        'flight_number': flight_no,
        'arrival_time': get_local_arrival_time(arrival['scheduledTime']),
        'terminal': int(arrival.get('terminal', 0)),
        'departure_city': departure_city,
    }


def get_city_name(airport: dict) -> str:
    return airport['name']


def get_departure_city(departure: dict) -> str:
    return get_city_name(departure['airport'])


def normalize_flight_info(flight_info: dict, airport_id: str) -> dict:
    return get_arrival_info(flight_info['arrival'], flight_info['number'], airport_id, get_departure_city(flight_info['departure']))


def normalize_flight_infos(flight_infos: list[dict], airport_id: str) -> list[dict]:
    return [normalize_flight_info(flight_info, airport_id) for flight_info in flight_infos]


def normalize_flights_infos(response: dict, airport_id: str) -> list:
    return [] if not 'arrivals' in response else normalize_flight_infos(response['arrivals'], airport_id)


# endregion
