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
    success = zd_google.delete_worksheet(title)

    return Response(data=[], metadata={"success": success,
                                       'data_deleted': title})


@router.route("/content", methods=["GET", "POST"])
def content():
    try:
        request = Request(flask_request)
        data = request.data

        content_object_names = data.get("content_object_names", ["titles"])
        content_objects = []

        for content_name in content_object_names:
            if content_name == "titles":
                worksheet_names = zd_google.list_worksheets_titles()

                data = [
                    {
                        "label": label,
                        "value": label
                    }
                    for idx, label in enumerate(worksheet_names)
                ]

                content_objects.append({
                    "content_object_name": "titles",
                    "data": data
                })

        return Response(data={"content_objects": content_objects})

    except Exception as e:
        return Response.error(str(e))

    return Response(data={"content_objects": []})
