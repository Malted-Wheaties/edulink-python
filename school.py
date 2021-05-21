import requests
import utils
# input
# school code/postcode

# output
# school server


# errors
# InvalidSchoolCode
class ProvisioningError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def server(code: str):
    # Provisioning request
    provisioning_url = "https://provisioning.edulinkone.com/?method=School.FromCode"
    provisioning_payload = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": "School.FromCode",
        "params": {
            "code": code
        },
        "uuid": utils.uuid()
    }

    provisioning_response = requests.post(provisioning_url, json=provisioning_payload)
    provisioning_content = provisioning_response.json()
    print(provisioning_content)

    if provisioning_content["result"]["success"] is True:
        return provisioning_content["result"]["school"]["server"]
    else:
        msg = provisioning_content["result"]["error"]
        raise ProvisioningError(msg)

"""
code <- USERINPUT

result = provisioning.get_server(code)

if result.success is False:
    msg = result.error
    raise ProvisioningError(msg)
"""

#
#