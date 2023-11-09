def get_wind_gust(forecast: dict) -> float:
    return forecast['gust']


def get_wind_direction(forecast: dict) -> int:
    return forecast['deg']


def get_wind_speed(forecast: dict) -> float:
    return forecast['speed']


def get_snow(forecast: dict | None) -> int:
    return forecast['3h'] if forecast else 0


def get_rain(forecast: dict | None) -> int:
    return forecast['3h'] if forecast else 0


def get_cloudiness(forecast: dict) -> int:
    return forecast['all']


def get_humidity(forecast: dict) -> int:
    return forecast['humidity']


def get_feel_temp(forecast: dict) -> float:
    return forecast['feels_like']


def get_temp(forecast: dict) -> float:
    return forecast['temp']


def get_weather(forecast: list[dict]) -> str:
    return forecast[0]['description']


def get_weather_forcast(weather_forecast: dict, city_id: int) -> dict:
    return {
        'city_id': city_id,
        'forecast_time': weather_forecast['dt_txt'],
        'forecast': get_weather(weather_forecast['weather']),
        'temperature': get_temp(weather_forecast['main']),
        'temperature_feels_like': get_feel_temp(weather_forecast['main']),
        'humidity': get_humidity(weather_forecast['main']),
        'cloudiness': get_cloudiness(weather_forecast['clouds']),
        'rain': get_rain(weather_forecast.get('rain')),
        'snow': get_snow(weather_forecast.get('snow')),
        'probability': weather_forecast['pop'],
        'wind_speed': get_wind_speed(weather_forecast['wind']),
        'wind_direction': get_wind_direction(weather_forecast['wind']),
        'wind_gust': get_wind_gust(weather_forecast['wind']),
    }


def normalize_list_response(list_response: dict, city_id: int) -> list[dict]:
    return [get_weather_forcast(weather_forecast, city_id) for weather_forecast in list_response]


def normalize_open_weather_response(response: dict, city_id: int) -> list[dict]:
    return normalize_list_response(response['list'], city_id)
