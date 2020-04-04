import os
import json
import requests
import pandas as pd

GOOG_KEY = os.environ['GOOGLE_API_KEY']
CIVIC_HOST = 'https://www.googleapis.com/civicinfo/v2'


def get_my_reps(address):
    path = 'representatives'
    params = {'address':address, 'levels':'country', 'key':GOOG_KEY}

    reps = requests.get('{}/{}'.format(CIVIC_HOST, path),
                        params=params)

    if reps.status_code != 200:
        raise Exception(reps.status_code, json.loads(reps.text)['error']['message'], 'Error at civic.get_my_reps')

    return pd.DataFrame(reps.json()['officials'])[['name','party','urls']]


def get_state_reps(state):
    path = 'representatives'
    division = 'ocd-division%2Fcountry%3Aus%2Fstate%3A{}'.format(state.lower())
    params = {'levels':'country', 'recursive':'true', 'key':GOOG_KEY}

    reps = requests.get('{}/{}/{}'.format(CIVIC_HOST, path, division),
                        params=params)

    if reps.status_code != 200:
        raise Exception(reps.status_code, json.loads(reps.text)['error']['message'], 'Error at civic.get_state_reps')

    return pd.DataFrame(reps.json()['officials'])[['name','party','urls']]
