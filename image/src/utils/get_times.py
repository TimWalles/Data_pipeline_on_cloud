import datetime


def get_end_times() -> list[datetime.time]:
    hours = [11, 23]
    minutes = [59, 59]
    return [datetime.time(hour=hour, minute=minute) for hour, minute in zip(hours, minutes)]


def get_start_times() -> list[datetime.time]:
    hours = [0, 12]
    minutes = [0, 0]
    return [datetime.time(hour=hour, minute=minute) for hour, minute in zip(hours, minutes)]


def get_date_tomorrow() -> datetime.date:
    return datetime.datetime.now() + datetime.timedelta(days=1)


def get_datetimes(date, time):
    return datetime.datetime.combine(date=date, time=time).isoformat()


def get_times():
    date = get_date_tomorrow()
    start_times = [get_datetimes(date, time) for time in get_start_times()]
    end_times = [get_datetimes(date, time) for time in get_end_times()]
    return start_times, end_times
