import requests
import utils

import edulink_errors as errors

# TODO:
    # Add add support for alternative login methods other than google, eg microsoft
    # Cross-reference Group ID's with relevant information to bulk out the information in Groups.

class Profile:
    def __init__(self, authtoken, school_name, school_logo_base64, pupil_forename, pupil_surname, pupil_username, avatar_base64, avatar_width, avatar_height, groups_year_id, groups_community_id, groups_form_id):
        self.authtoken = authtoken
        self.School = self.School(school_name, school_logo_base64)
        self.Pupil = self.Pupil(pupil_forename, pupil_surname, pupil_username, avatar_base64, avatar_width, avatar_height)
        self.Groups = self.Groups(groups_year_id, groups_community_id, groups_form_id)
    
    class School:
        def __init__(self, name, logo_base64):
            self.name = name
            self.logo_base64 = logo_base64

    class Pupil:
        def __init__(self, pupil_forename, pupil_surname, pupil_username, avatar_base64, avatar_width, avatar_height):
            self.forename = pupil_forename
            self.surname = pupil_surname
            self.name = pupil_forename + " " + pupil_surname
            self.username = pupil_username
            self.avatar = self.Avatar(avatar_base64, avatar_width, avatar_height)

        class Avatar:
            def __init__(self, base64, width, height):
                self.base64 = base64
                self.width = width
                self.height = height
                

    class Groups:
        def __init__(self, year_id, community_id, form_id):
            self.year = self.Year(year_id)
            self.community = self.Community(community_id)
            self.house = self.Community(community_id)
            self.form = self.Form(form_id)
            
        class Year:
            def __init__(self, id):
                self.id = id
                
        class Community:
            def __init__(self, id):
                self.id = id

        class Form:
            def __init__(self, id):
                self.id = id



def login(server: str, username: str, password: str):
    url = server + "?method=EduLink.Login"
    payload = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": "EduLink.Login",
        "params": {
            "establishment_id": "2",
            "fcm_token_old": "none",
            "from_app": False,
            "password": password,
            "ui_info": {
                "format": "2",
                "git_sha": utils.uuid(), # In official requests this is a SHA-1 however in practice it does not matter.
                "version": "0.5.181"
            },
            "username": username
        },
        "uuid": utils.uuid()
    }
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "X-API-Method": "EduLink.Login"
    }

    response = requests.post(url, json=payload, headers=headers)
    content = response.json()


    if content["result"]["success"] is True:
        content = content["result"] # To decrease code verbosity.

        authtoken = content["authtoken"]

        school_name = content["establishment"]["name"]
        school_logo_base64 = content["establishment"]["logo"]

        pupil_forename = content["user"]["forename"]
        pupil_surname = content["user"]["surname"]
        pupil_username = content["user"]["username"]

        avatar_base64 = content["user"]["avatar"]["photo"]
        avatar_width = content["user"]["avatar"]["width"]
        avatar_height = content["user"]["avatar"]["height"]

        groups_year_id = content["user"]["year_group_id"]
        groups_community_id = content["user"]["community_group_id"]
        groups_form_id = content["user"]["form_group_id"]
        

        user = Profile(authtoken, 
                    school_name, 
                    school_logo_base64, 
                    pupil_forename, 
                    pupil_surname, 
                    pupil_username, 
                    avatar_base64, 
                    avatar_width, 
                    avatar_height, 
                    groups_year_id, 
                    groups_community_id, 
                    groups_form_id)

        return user

    else:
        msg = content["result"]["error"]
        raise errors.SchoolDetailsError(msg)
        