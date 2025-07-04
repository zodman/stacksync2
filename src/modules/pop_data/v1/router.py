from workflows_cdk import Response, Request
from flask import request as flask_request
from main import router

from utils import get_data, MissingTitle

import zd_google


@router.route("/execute", methods=["GET", "POST"])
def execute():
    try:
        data = get_data(flask_request)
    except MissingTitle:
        return Response(data={"message": "Missing request zd_title"}, status_code=400)

    title = data.get('zd_title')

    success = zd_google.pop_data(title)

    return Response(data=[], metadata={"success": success, 'data_append': title})
