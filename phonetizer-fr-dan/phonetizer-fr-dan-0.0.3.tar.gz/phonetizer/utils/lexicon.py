import logging
import os
import pandas as pd

def load_lexicon():
    try:
        df = pd.read_parquet('gs://phonetizer/static/lexicon.parquet')
    except OSError as e:
        logging.warning('lexicon was not found. Building it.')
        df = create_lexicon()
    return df

def create_lexicon():
    df = pd.read_csv(os.environ.get('SOURCE_URL', 'http://www.lexique.org/databases/Lexique383/Lexique383.tsv'), sep="\t")
    df = (
        df
        [['ortho', 'phon']]
        .loc[lambda row: ~ row.ortho.isna()]
        .loc[lambda row: ~ row.ortho.str.contains(' ')]
    )
    df.to_parquet('gs://phonetizer/static/lexicon.parquet')
    return df
