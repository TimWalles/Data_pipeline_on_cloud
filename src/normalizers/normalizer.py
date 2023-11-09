import datetime
import re

import pycountry
from dms2dec.dms_convert import dms2dec


def coords2float(coord) -> float:
    return dms2dec(coord)


def cast_to_int(population: str) -> int:
    return int(''.join(re.compile('\d+').findall(population)))


def country2code(country: str) -> str:
    return str(pycountry.countries.get(name=country).alpha_2)


def get_datetime(time: str) -> str:
    return datetime.datetime.fromisoformat(time).strftime("%Y-%m-%d %H:%M:%S")


def get_year(time: str) -> int:
    time = re.compile('(\d{4})').search(time)
    if time:
        return cast_to_int(time.group(1))
    return 0
