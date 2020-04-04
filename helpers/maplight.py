import os
import requests
import pandas as pd

MAPLIGHT_HOST = 'https://api.maplight.org/maplight-api/fec'


def get_candidate_record(name, state):
    path = 'candidate_names'

    names = requests.get('{}/{}/{}'.format(MAPLIGHT_HOST, path, name))

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

    csv_url = requests.get(DOWNLOAD_URL, params=data).text

    return pd.read_csv(csv_url)
