import socket
import os
import json
import requests
from datetime import datetime, timedelta

url = 'https://1pjmo69bw2.execute-api.ap-northeast-2.amazonaws.com/rpi_weather/upload'
file_path = '/home/telofarm01/jsonfile/testfile.json'
def is_internet_connected():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        pass
    return False


def round_seconds(dt):
    return dt.replace(second=0)

def savelocal(data):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing_data = json.load(f)
        existing_data.append(data)
        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)
    else:
        with open(file_path, "w") as f:
            json.dump([data], f, indent=4)
       
def saveserver(data):
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing_data = json.load(f)
            
        existing_data.append(data)
        print(existing_data)
        
        response = requests.post(url, json=existing_data)
        
        print(response.status_code)
        os.remove(file_path)
    else:
        data = [data]
        response = requests.post(url, json=data)
        print(response.status_code)
