from flask import jsonify
import uuid

from hello_function.entry_point import handle_request
import datetime as dt
from datetime import datetime
from datetime import timedelta


def response_code_to_return_dictionary(response_code,backend_message):
    if (200 == response_code):
        return {"response_msg": "Success", "response_code": 101}
    elif (400 == response_code):
        return {"response_msg": "No records found for the given ID or combination of inputs", "response_code": 103}
    elif (424 == response_code):
        return {"response_msg": "Source Unavailable", "response_code": 110, "transaction_status": 0}
    elif (401 == response_code):
        return {"response_msg": backend_message.get('error','unkown format passed'), "response_code": 112, "transaction_status": 0}


def handle_response_and_return_code(request_handler, request, time_delta_value=2):
    request_uuid = str(uuid.uuid1())
    request_time = datetime.now(dt.timezone.utc)
    response = request_handler(request)
    code = response.pop("code")
    response_time = datetime.now(dt.timezone.utc)
    response_time = response_time + timedelta(seconds=time_delta_value)
    mdictionary = {"request_time": request_time.isoformat(), "response_time": response_time.isoformat(),
                   "id": request_uuid}
    if (code == 200):
        mdictionary.update({"data": response})
    mdictionary.update(response_code_to_return_dictionary(code,response))
    print("request with args {} of {} to {}".format(request.args, request_uuid, request_handler.__name__))
    return mdictionary


def handle_response_and_prepare_for_request_response(request_handler, request):
    response = handle_response_and_return_code(request_handler, request)
    return jsonify(response), 200


def handle_hello_function(request):
    return handle_response_and_prepare_for_request_response(handle_request, request)

