import requests
import utils

import edulink_errors as errors

def server(code: str):
    url = "https://provisioning.edulinkone.com/?method=School.FromCode"
    payload = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": "School.FromCode",
        "params": {
            "code": code
        },
        "uuid": utils.uuid()
    }

    response = requests.post(url, json=payload)
    content = response.json()

    if content["result"]["success"] is True:
        return content["result"]["school"]["server"]
    else:
        msg = content["result"]["error"]
        raise errors.ProvisioningError(msg)