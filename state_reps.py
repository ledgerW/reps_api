import sys
sys.path.append('..')

import os
import json
import requests
import logging
import pandas as pd
from helpers.civic import get_state_reps
from helpers.maplight import get_candidate_record, get_all_contributions

logger = logging.getLogger()
logger.setLevel(logging.INFO)

GOOG_KEY = os.environ['GOOGLE_API_KEY']


def get(event, context):
    #logger.info(event)
    params = event['queryStringParameters']
    state = params.get('state')
    cycle = params.get('cycle', '2020')
    groupby = params.get('groupby', 'CandidateOffice|CandidateParty')

    try:
        assert set(groupby.split('|')).issubset(['CandidateName','CandidateOffice','CandidateParty'])
        assert state is not None
    except:
        return {
            'statusCode': 500,
            'body': 'Invalid query parameters.'
            }

    try:
        # pulling reps from Civic API
        state_reps = get_state_reps(state)

        # pulling rep record from Maplight API
        ml_names = pd.DataFrame([get_candidate_record(name, state) for name in state_reps.name if name != 'VACANT'])

        # pulling ALL contributions for each rep from Maplight API
        all_contrib = pd.concat([get_all_contributions(mlid, cycle) for mlid in ml_names.CandidateMaplightID], ignore_index=True)

        # summarize
        summary = all_contrib\
            .groupby(groupby.split('|'))\
            .agg(give_count=('TransactionAmount', 'count'),
                 give_sum=('TransactionAmount', 'sum'),
                 give_mean=('TransactionAmount', 'mean'),
                 give_median=('TransactionAmount', 'median'),
                 give_min=('TransactionAmount', 'min'),
                 give_max=('TransactionAmount', 'max'))\
            .reset_index()

        response = {
            'statusCode': 200,
            'body': summary.to_json(orient='records')
            }
    except Exception as e:
        response = {
            'statusCode': 400,
            'body': str(e)
            }

    return response