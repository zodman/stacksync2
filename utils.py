from workflows_cdk import Response, Request
from flask import request as flask_request


class MissinTitle(Exception):
    pass


def get_data(flask_request):
    request = Request(flask_request)

    data = request.data

    title = data.get('zd_title')

    if not title:
        raise MissinTitle('zd_title')
