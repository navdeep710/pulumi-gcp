#2011-03-01T00:00:00+05:30' does not match format 'yyyy-MM-ddTHH:mm:ssTZD'
import datetime

from util_functions import get_date_from_schedule_string, get_string_from_datetime, safe_run


def assert_time_convertion():
    print(get_string_from_datetime(get_date_from_schedule_string("2010-04-09T00:00:00+05:30")))


@safe_run
def i_am_bound_to_fail():
    raise Exception()

# if __name__ == '__main__':
#     assert_time_convertion()
#     i_am_bound_to_fail()