from app.schemas.utils import error_handler, bad_request_handler, success_handler, unauthorized_handler


def error_response(e):
    return error_handler()

def bad_request_response(**kwargs):
    return bad_request_handler(kwargs)

def success_response(data, **kwargs):
    return success_handler(data, kwargs)

def unauthorized_response(**kwargs):
    return unauthorized_handler(kwargs)
