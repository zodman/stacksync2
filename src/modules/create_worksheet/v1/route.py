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

    success = False
    try:
        success = zd_google.create_worksheet(title)
    except zd_google.WorksheetExists:
        return Response(data={"message": f"worksheet with {title} exists"}, status_code=400)

    return Response(data=[], metadata={"success": success, 'data_created': title})
