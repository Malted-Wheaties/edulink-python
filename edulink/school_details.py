import requests
import utils

import edulink_errors as errors


class School:
    def __init__(self, name, google_login, logo_base64):
        self.name = name
        self.google_login = google_login
        self.logo_base64 = logo_base64


def school(code: str):
    url = f"https://{code}.edulinkone.com/api/?method=EduLink.SchoolDetails"
    payload = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": "EduLink.SchoolDetails",
        "params": {
            "establishment_id": "2",
            "from_app": False
        },
        "uuid": utils.uuid()
    }
    headers = {
        "Content-Type":
        "application/json;charset=UTF-8",
        "X-API-Method": "EduLink.SchoolDetails"
    }

    response = requests.post(url, json=payload, headers=headers)
    content = response.json()

    if content["result"]["success"] is True:
        name = content["result"]["establishment"]["name"]
        google_login = content["result"]["establishment"]["idp_login"]["google"]
        logo_base64 = content["result"]["establishment"]["logo"]

        school = School(name, google_login, logo_base64)
        return school

    else:
        msg = content["result"]["error"]
        raise errors.SchoolDetailsError(msg)
