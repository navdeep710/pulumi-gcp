import datetime
import functools
import operator
import random
import time
from functools import reduce

INCOMING_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
DEFAULT_OUTGOING_FORMAT = "%d-%m-%Y"



def delayed(seconds):
    def decorator(f):
        def wrapper(*args, **kargs):
            time.sleep(seconds)
            return f(*args,**kargs)
        return wrapper
    return decorator

def safe_run(func):
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except:
            client.report_exception()
    return wrapper

"""
we are only expecting single values
"""
def getFromDict(dataDict, mapList):
    try:
        return reduce(operator.getitem, mapList, dataDict)
    except:
        return ""

def get_dictionary_from_map_function(data_dictionary,validity_function_mapping,sanitize_function=lambda x:x):
    return {key:sanitize_function(getFromDict(data_dictionary,value)) for key,value in validity_function_mapping.items()}

def get_string_from_datetime(job_date_time, date_format=DEFAULT_OUTGOING_FORMAT):
    try:
        return job_date_time.strftime(date_format)
    except:
        return ""

def get_date_from_schedule_string(job_string, date_format=INCOMING_DATE_FORMAT):
    try:
        return datetime.datetime.strptime(job_string.replace('+05:30',''), date_format)
    except:
        return job_string

def setInDict(dataDict, mapList, value):
    for k in mapList[:-1]: dataDict = dataDict[k]
    dataDict[mapList[-1]] = value



from google.cloud import error_reporting
client = error_reporting.Client()


def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def sanitize_string_keys_dictionary(value,sanitize_function):
    if isinstance(value,str):
        return sanitize_function(value)
    else:
        return value


def string_sanitize_functions():
    return compose(lambda x:x.replace("$", " "), lambda x: x.strip())


def sanitise_dictionary_with_string_keys(mdict,string_sanitize_function=string_sanitize_functions()):
    return {key:sanitize_string_keys_dictionary(value,string_sanitize_function) for key,value in mdict.items()}


def response_content_to_json(response):
    try:
        json_response = response.json()
        return json_response
    except:
        return {}
