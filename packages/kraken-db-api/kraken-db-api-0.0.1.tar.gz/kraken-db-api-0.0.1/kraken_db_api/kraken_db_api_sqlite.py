import requests
import json
import os
import time


headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def get(record_type = None, record_id = None, key = None, value = None):

    params = {
        'record_type': record_type,
        'record_id': record_id,
        'key': key,
        'value': value,
        'format': 'json'
    }

    mod_url = get_db_url()
    
    records = request_get(mod_url, params)


    return records

def get_summary(record_type = None, record_id = None, key = None, value = None):

    params = {
        'record_type': record_type,
        'record_id': record_id,
        'key': key,
        'value': value,
        'format': 'json'
    }

    mod_url = get_db_url()
    mod_url = mod_url + '/summary'
    

    records = request_get(mod_url, params)


    return records

def search(params):

    
    mod_url = get_db_url()
    mod_url = mod_url + '/search'
    print(mod_url)

    records = request_get(mod_url, params)


    return records

def post(observations):

    params = {

    }

    mod_url = get_db_url()


    data = json.dumps(observations, default = str)

    r = request_post(mod_url, params, data)

    return 


def set_db_url(url):

    os.environ['DB_URL'] = url
    return


def get_db_url():

    DB_URL = os.getenv('DB_URL')

    print('DB_URL', DB_URL)
    if DB_URL:
        return DB_URL + '/api'

    else:
        return 'https://krakendb.tactik8.repl.co/api'


def request_get(url, params = {}, data = {}):
    
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    while True:
        
        try:
            r = requests.get(url, headers = headers, params=params, data = data)
            break
        except Exception as e:
            print('Error getting api', e)
            time.sleep(1)

    records = r.json()

    return records


def request_post(url, params = {}, data = {}):
    
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    while True:
        
        try:
            r = requests.post(url, headers = headers, params=params, data = data)
            break
        except Exception as e:
            print('Error getting api', e)
            time.sleep(1)

    return 