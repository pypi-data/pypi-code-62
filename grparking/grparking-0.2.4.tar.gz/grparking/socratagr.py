import requests
import os
import pandas as pd
from socrata.authorization import Authorization
from socrata import Socrata


# RENAME RAMPS FUNCTION
def rename_ramp(fourfour, column, current_name, replacement, update_config, blanks=False, blank_names=None):
    # GET EXISTING DATA
    url = 'https://data.grandrapidsmi.gov/resource/' + \
          fourfour + \
          '.json?$limit=10000000&$where=' + \
          column + "='" + \
          current_name + "'"

    df = requests.get(url, auth=(os.environ['SOCRATA_USERNAME'], os.environ['SOCRATA_PASSWORD']))

    df = pd.DataFrame(df.json())

    # RECODE VARIABLE
    df[column] = replacement

    # ADD COLUMNS WITH BLANK VALUES
    if blanks is True:
        for column in blank_names:
            df[column] = None

    # SOCRATA AUTH
    auth = Authorization(
        'data.grandrapidsmi.gov',
        os.environ['SOCRATA_USERNAME'],
        os.environ['SOCRATA_PASSWORD']
    )
    socrata = Socrata(auth)

    # REPLACE EXISTING DATA WITH RECODED DATA
    (ok, view) = socrata.views.lookup(fourfour)
    (revision, job) = socrata.using_config(
        update_config,
        view
    ).df(df)
    (ok, job) = job.wait_for_finish(progress=lambda job: print('Ramp Replacement Progress: ', job.attributes['status']))
