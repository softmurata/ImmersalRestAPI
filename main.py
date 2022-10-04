import requests
import json
import base64

apiroot = "https://api.immersal.com/1.15.0"
token = "52df255a3971bd4062048b1fed79494f7af9281270b1fffce4bfe30d3520d823"
email = "tatsuromurata317@gmail.com"
password = "rtfd2018"


def Login(url, username, password):
    complete_url = url + '/login'

    data = {
        "login": username,
        "password": password
    }

    json_data = json.dumps(data)

    r = requests.post(complete_url, data=json_data)
    print(r.text)

def AccountStatus(url, token):
    complete_url = url + '/status'

    data = {
        "token": token,
        "bank" : 0, # default workspace/image bank
    }

    json_data = json.dumps(data)

    r = requests.post(complete_url, data=json_data)
    print(r.text)

def ListJobs(url, token):
    complete_url = url + '/list'

    data = {
        "token": token,
        "bank": 0 # default workspace/image bank
    }

    json_data = json.dumps(data)

    r = requests.post(complete_url, data=json_data)
    print(r.text)

def ListJobsGPS(url, token, latitude, longitude, radius):
    complete_url = url + '/geolist'

    data = {
        "token": token,
        "bank": 0, # default workspace/image bank
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius
    }

    json_data = json.dumps(data)

    r = requests.post(complete_url, data=json_data)
    print(r.text)

# server localize
def ConvertToBase64(src_filepath):
    with open(src_filepath, 'rb') as imageFileAsBinary:
        fileContent = imageFileAsBinary.read()
        b64_encoded_img = base64.b64encode(fileContent)

        return b64_encoded_img

def ServerLocalize(url, token, imagePath):
    complete_url = url + '/localizeb64'

    mapId = 41769

    data = {
        "token": token,
        "fx": 1455.738159, # image focal length in pixels on x axis
        "fy": 1455.738159, # image focal length in pixels on y axis
        "ox": 962.615967, # image principal point on x axis
        "oy": 694.292175, # image principal point on y axis
        "b64": str(ConvertToBase64(imagePath), 'utf-8'), # base64 encoded .png image
        "mapIds": [{"id": mapId}] # a list of map ids to localize against
    }

    json_data = json.dumps(data)

    r = requests.post(complete_url, data=json_data)
    print(r.json())
    print(r.text)

if __name__ == "__main__":
    # Login(apiroot, email, password)
    # AccountStatus(apiroot, token)
    # ListJobs(apiroot, token)
    # ListJobsGPS(apiroot, token, 35.70781, 139.72868, 10)
    ServerLocalize(apiroot, token, "IMG_1109.png")



