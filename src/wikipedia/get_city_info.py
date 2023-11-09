import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.normalizers.normalizer import cast_to_int, coords2float, country2code, get_year


def get_website_content(city_name: str) -> bytes:
    url = f'https://en.wikipedia.org/wiki/{city_name}'
    response = requests.get(url)
    if not response.status_code == 200:
        print(f'Response code: {response.status_code} was returned for city: {city_name}')
        return b''
    return response.content


def get_country(city_name: str, soup: BeautifulSoup) -> str:
    country_info = soup.select_one(".infobox-label:-soup-contains('Country')")
    if not country_info:
        print(f'Failed to find country information for city: {city_name}')
        return ''
    return country_info.find_next(class_='infobox-data').get_text()


def get_county_code(country_name: str) -> str:
    return country2code(country_name)


def get_population(city_name: str, soup: BeautifulSoup) -> int:
    country_info = soup.select_one(".infobox-header:-soup-contains('Population')")
    population = country_info.find_next(class_='infobox-data').get_text()
    try:
        return cast_to_int(population)
    except:
        print(f'Failed to normalize population information {population} for city: {city_name}')
        return 0


def get_measurement_year(city_name: str, soup: BeautifulSoup) -> int:
    country_info = soup.select_one(".infobox-header:-soup-contains('Population')")
    measurement_year = country_info.find_next(class_='ib-settlement-fn').get_text()
    try:
        return get_year(measurement_year)
    except:
        print(f'Failed to normalize measurement year information {measurement_year} for city: {city_name}')
        return 0


def get_latitude(city_name: str, soup: BeautifulSoup) -> float | None:
    coord = soup.select_one('.latitude').get_text()
    try:
        return coords2float(coord)
    except:
        print(f"couldn't normalize latitude coordinate {coord} to decimal for city: {city_name}")
        return None


def get_longitude(city_name: str, soup: BeautifulSoup) -> float | None:
    coord = soup.select_one('.longitude').get_text()
    try:
        return coords2float(coord)
    except:
        print(f"couldn't normalize longitude coordinate {coord} to decimal for city: {city_name}")
        return None


def get_city_info(city_name: str) -> dict:
    content = get_website_content(city_name)
    if content == b'':
        return {}

    soup = BeautifulSoup(content, 'html.parser')
    latitude = get_latitude(city_name, soup)
    longitude = get_longitude(city_name, soup)

    # without latitude or longitude we can't get the data from the other databases
    if not any([latitude, longitude]):
        print(f'Critical value longitude or latitude is missing for city: {city_name}')
        return {}
    country_name = get_country(city_name, soup)
    return {
        'city_name': city_name,
        'country': country_name,
        'country_code': get_county_code(country_name),
        'population': get_population(city_name, soup),
        'measurement_year': get_measurement_year(city_name, soup),
        'latitude': latitude,
        'longitude': longitude,
    }
