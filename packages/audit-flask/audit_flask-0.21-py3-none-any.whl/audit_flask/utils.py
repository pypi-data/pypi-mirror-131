import json
from flask import request

def is_serializable(object):
    try:
        json.dump(object)
        return True
    except:
        return False

def serializar_dict(dictionary:  dict) -> dict:
    if type(dictionary) == dict:
        dictionary_new = dictionary.copy()
        for key, value in dictionary_new.items():
            if not is_serializable(value):
                dictionary_new[key] = json.dumps(value, default=str)
        return dictionary_new
    return dictionary

def remote_addr_validate():
    try:
        return {k: v for k, v in request.headers.items()}
    except RuntimeError as ex:
        pass

def user_validate():
    try:
        return f"{request.headers.get('X-Consumer-Custom-ID')} - {request.headers.get('X-Consumer-Username')}"
    except RuntimeError as ex:
        pass