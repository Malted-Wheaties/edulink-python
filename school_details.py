import requests
import utils

import edulink_errors as errors


# TODO: Alternative login methods, eg Microsoft
class School:
    def __init__(self, name, google_login, logo):
        self.name = name
        self.google_login = google_login
        self.logo = logo


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
        logo = content["result"]["establishment"]["logo"]

        school = School(name, google_login, logo)
        return school

    else:
        msg = content["result"]["error"]
        raise errors.SchoolDetailsError(msg)


def save_logo(school: School): pass
