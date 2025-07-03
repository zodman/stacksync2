from workflows_cdk import Response, Request
from flask import request as flask_request
from main import router

import zd_google
from utils import get_data, MissingTitle


@router.route("/execute", methods=["GET", "POST"])
def execute():

    try:
        data = get_data(flask_request)
    except MissingTitle:
        return Response(data={"message": "Missing request zd_title"}, status_code=400)

    sheet_data = data.get('zd_data')

    success = zd_google.append_data(title, [sheet_data])

    return Response(data=[], metadata={"success": success, 'data_append': title})
