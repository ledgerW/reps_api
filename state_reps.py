import sys
sys.path.append('..')

import os
import json
import requests
import logging
import boto3
import pandas as pd
from helpers.civic import get_state_reps
from helpers.maplight import get_candidate_record, get_all_contributions

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True
}

#logger = logging.getLogger()
#logger.setLevel(logging.INFO)

GOOG_KEY = os.environ['GOOGLE_API_KEY']
STAGE = os.environ['STAGE']

client = boto3.client('lambda')


def get(event, context):
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
            'headers': headers,
            'body': 'Invalid query parameters.'
            }

    try:
        # pulling reps from Civic API
        state_reps = get_state_reps(state)

        # pulling rep record from Maplight API
        ml_names = pd.DataFrame([get_candidate_record(name, state) for name in state_reps.name if name != 'VACANT'])

        # pulling ALL contributions for each rep from Maplight API
        all_contrib = pd.DataFrame()
        for mlid in ml_names.CandidateMaplightID:
            response = client.invoke(
                FunctionName='reps-api-{}-worker'.format(STAGE),
                InvocationType='Event',
                Payload=json.dumps({"mlid": mlid, "cycle": cycle})
            )
            print(response.json())
            contrib = pd.read_json(response.json()['body'], orient='records')
            all_contrib = pd.concat([all_contrib, contrib], ignore_index=True)

        #all_contrib = pd.concat([get_all_contributions(mlid, cycle) for mlid in ml_names.CandidateMaplightID], ignore_index=True)
        if all_contrib.shape[0] == 0:
            raise Exception(400, 'No contributions found; double-check params', 'Error at maplight.get_all_contributions')

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
            'headers': headers,
            'body': summary.to_json(orient='records')
            }
    except Exception as e:
        response = {
            'statusCode': 400,
            'headers': headers,
            'body': str(e)
            }

    return response


def worker(event, context):
    contrib = get_all_contributions(event['mlid'], event['cycle'])

    response = {
        'statusCode': 200,
        'headers': headers,
        'body': contrib.to_json(orient='records')
    }

    return response
