import http

from rest_framework.response import Response


def error_resp(code, message=''):
    data = {
        "error_code": code,
        'error_msg': message
    }
    resp = Response(data)
    return resp


def reformat_resp(code, meta, objects, message=''):
    data = {
        'code': code,
        'meta': meta,
        'objects': objects,
        'message': message,
    }
    resp = Response(data)
    return resp


def reformat_resp_(code, body, message=''):
    data = {
        'code': code,
        'body': body,
        'message': message
    }
    resp = Response(data)
    return resp


def reformat_resp_user(code, user, profile,  message=''):
    data = {
        'code': code,
        'user': user,
        'profile': profile,
        'message': message
    }
    resp = Response(data)
    return resp


def reformat_resp__(data):
    data = {
        'objects': data
    }
    return Response(data)
