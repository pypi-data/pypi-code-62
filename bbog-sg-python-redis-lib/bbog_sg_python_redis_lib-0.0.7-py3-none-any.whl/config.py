"""default config for redis api"""
import os

API_URL = {'QA': 'https://ig242h05jg-{}.execute-api.us-east-1.amazonaws.com/QA',
           'STG': 'https://gvohjacbw5-{}.execute-api.us-east-1.amazonaws.com/STG',
           'PROD': 'https://9vx5eofbf4-{}.execute-api.us-east-1.amazonaws.com/PROD'}

API_URL_OLD = {'QA': 'https://ig242h05jg-vpce-06e9678f9d1e184b3.execute-api.us-east-1.amazonaws.com/QA',
               'STG': 'https://gvohjacbw5-vpce-040d9ee0ac555eeb4.execute-api.us-east-1.amazonaws.com/STG',
               'PROD': 'https://9vx5eofbf4-vpce-09f41abfda181e07f.execute-api.us-east-1.amazonaws.com/PROD'}

ENVIRONMENT = os.getenv('ENVIRONMENT', 'QA')
VPCE_ID = os.getenv('VPCE_ID', None)
API_KEY = os.getenv('REDIS_API_KEY', None)
OLD_ACCOUNT = os.getenv('OLD_ACCOUNT', 'true')
