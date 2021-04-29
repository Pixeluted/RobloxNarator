import requests
import json

def getGroupName(ID):
    response = json.loads(requests.get(f'https://groups.roblox.com/v1/groups/{ID}').text)
    return response["name"]

def isThisGroupValid(ID):
    response = json.loads(requests.get(f'https://groups.roblox.com/v1/groups/{ID}').text)

    if 'errors' in response:
        return False
    else:
        return True