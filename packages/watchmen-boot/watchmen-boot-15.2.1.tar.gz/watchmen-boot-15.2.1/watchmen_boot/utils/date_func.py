import arrow
from math import ceil

DATETIME = "datetime"  # YYYY-MM-DD HH:mm:ss
FULL_DATETIME = "full-datetime"  # YYYY-MM-DD HH:mm:ss.SSS
DATE = "date"  # YYYY - MM - DD
TIME = "time"  # HH: mm:ss
YEAR = "year"  # 4
HALF_YEAR = "half-year"  # 1: first half, 2: second half

QUARTER = "quarter"  # 1 - 4
SEASON = "season"  # 1: spring, 2: summer, 3: autumn, 4: winter
MONTH = "month"  # 1 - 12
HALF_MONTH = "half-month"  # 1: first half, 2: second half

TEN_DAYS = "ten-days"  # 1, 2, 3
WEEK_OF_YEAR = "week-of-year"  # 0 - 53
WEEK_OF_MONTH = "week-of-month"  # 0 - 5
HALF_WEEK = "half-week"  # 1: first half, 2: second half

DAY_OF_MONTH = "day-of-month"  # 1 - 31, according to month/year

DAY_OF_WEEK = "day-of-week"  # 1(Sunday) - 7(Saturday)
DAY_KIND = "day-kind"  # 1: workday, 2: weekend, 3: holiday
HOUR = "hour"  # 0 - 23
HOUR_KIND = "hour-kind"  # 1: work time, 2: off hours, 3: sleeping time

MINUTE = "minute"  # 0 - 59
SECOND = "second"  # 0 - 59
MILLISECOND = "millisecond"  # 0-999
AM_PM = "am-pm"  # 1, 2


def parsing_and_formatting(value, format_type_):
    if value is not None:
        arr_value = arrow.get(value).datetime.replace(tzinfo=None)
        if format_type_ == YEAR:
            return arr_value.year
        elif format_type_ == HALF_YEAR:
            month = arr_value.month
            if month <= 6:
                return 1
            else:
                return 2
        elif format_type_ == QUARTER:
            return quarter_of(arr_value)
        elif format_type_ == MONTH:
            return arr_value.month
        elif format_type_ == WEEK_OF_YEAR:
            return int(arr_value.strftime("%U"))
        elif format_type_ == WEEK_OF_MONTH:
            return week_of_month(arr_value.date())
        elif format_type_ == DAY_OF_MONTH:
            return arr_value.day
        elif format_type_ == DAY_OF_WEEK:
            return int(arr_value.strftime("%w")) + 1
    else:
        return value


def quarter_of(dt):
    month_ = dt.strftime("%m")
    if month_ in ['01', '02', '03']:
        return 1
    elif month_ in ['04', '05', '06']:
        return 2
    elif month_ in ['07', '08', '09']:
        return 3
    elif month_ in ['10', '11', '12']:
        return 4


def week_of_month(dt):
    """ Returns the week of the month for the specified date.
    """
    first_day = dt.replace(day=1)
    first_day_weekday = int(first_day.strftime(
        "%w"))  # The position of the first day in a week, is also the number of days to be supplemented in that week
    days = dt.day  # the number of days about dt
    adjusted_ = first_day_weekday + days
    print(adjusted_)
    return int(ceil(adjusted_ / 7.0)) - 1
