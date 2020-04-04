import os
import requests
import json
import pandas as pd

MAPLIGHT_HOST = 'https://api.maplight.org/maplight-api/fec'


def get_candidate_record(name, state):
    path = 'candidate_names'

    names = requests.get('{}/{}/{}'.format(MAPLIGHT_HOST, path, name))

    if names.status_code != 200:
        raise Exception(names.status_code, json.loads(names.text)['error']['message'], 'Error at maplight.get_candidate_record')

    for name in names.json()['data']['candidate_names']:
        if state.upper() in name['CandidateLabel']:
            name['Party'] = name['CandidateLabel'].split('(')[1][0]
            return name


def get_all_contributions(mlid, cycle):
    DOWNLOAD_URL = 'https://search.maplight.org/fec-search/download'

    data = {
        'donor_text': "",
        'donor_organization': "",
        'election_cycle[]': [str(cycle)],
        'candidate_mlid': str(mlid),
        'rows': "999999",
        'corp_pac': "0"
        }

    csv_url = requests.get(DOWNLOAD_URL, params=data)

    if csv_url.status_code != 200:
        raise Exception(csv_url.status_code, json.loads(csv_url.text)['error']['message'], 'Error at maplight.get_all_contributions')

    return pd.read_csv(csv_url.text)
