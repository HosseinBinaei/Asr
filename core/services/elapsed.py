def elapsed(passed, total):
    return (passed * 100 / total)


def elapsed_year(now):
    '''Percentage of year elapsed:
    (days passed in year - 1) * 100 / 365'''
    return elapsed(now.yday() - 1, 365)


def elapsed_month(now):
    '''Percentage of month elapsed:
    (days passed in month - 1) * 100 / 30'''

    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if now.month==12:
        end = now.replace(year=now.year+1, month=1, day=1)
    else:
        end = now.replace(month= now.month+1, day=1)

    elapsed_days = (now-start).days
    total_days = (end-start).days

    return elapsed(elapsed_days, total_days)


def elapsed_week(now):
    '''Percentage of week elapsed:
    (hours passed since start of week) * 100 / (7 * 24)
    Note:
    Week starts at 00:00 on the first weekday.
    weekday() is used to convert days to hours.'''
    return elapsed(now.hour + now.weekday() * 24, 7 * 24)


def elapsed_day(now):
    '''Percentage of day elapsed:
    (minutes passed since midnight) * 100 / (24 * 60)'''
    return elapsed(now.minute + now.hour * 60, 24 * 60)

def get_elapsed(now, pk=None):
    mapping = {
        'y': elapsed_year,
        'm': elapsed_month,
        'w': elapsed_week,
        'd': elapsed_day,
    }

    if pk is not None:
        output = mapping.get(pk)
        if output is None:
            return None
        return output(now)
            
    return {k: v(now) for k, v in mapping.items()}


def waiit(now, pk=None):
    '''Where am I in time?'''
    mapping = {
        'y': lambda x: x.yday(),
        'm': lambda x: x.day,
        'w': lambda x: x.weekday() + 1,
        'd': lambda x: x.hour,
    }
    if pk is not None:
        output = mapping.get(pk)
        if output is None:
            return None
        return output(now)
            
    return {k: v(now) for k, v in mapping.items()}