
from datetime import datetime,timedelta
import gzip
from io import BytesIO
import logging
import os
import pkg_resources
import warnings

import pandas as pd
import requests

# soft int parser
def tryInt(i):
    """Soft int parser. If not possible, bypasses input.
    
    Args:
        i (any): Value to parse int from.
    """
    try: return int(i)
    except: return i

def _parse_deaths(chunksize = 1):
    """Parses deaths from file.
    
    Args:
        chunksize (int, optional): Size of chunk to process data by (in thousands). Default is 1 (1000 lines in chunk).
    """
    logging.warning("input has over 200MB, processing will take a few minutes (for me 15 min)")
    # download
    url = 'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/demo_r_mweek3.tsv.gz'
    zipinput = requests.get(url, stream=True)
    # process
    with gzip.GzipFile(fileobj = BytesIO(zipinput.content), mode = "r") as z:
        logging.info("parsing zip file")
        
        for i,chunk in enumerate(pd.read_csv(z, sep=",|\t", engine = "python", chunksize = chunksize * 10**3)):
            # columns
            chunk.columns = [c.strip() for c in chunk.columns]
            data_columns = set(chunk.columns) - {'unit','sex','age','geo\\time'}

            # parse data
            chunk[ list(data_columns) ] = chunk.loc[ :,list(data_columns) ]\
                .replace({r'\s*:\s*': None, r'[^0-9]*([0-9]+)[^0-9]*': r'\1'}, regex = True)\
                .apply(tryInt)
            chunk = chunk.loc[:,:]\
                .drop(['unit'], axis = 1)
            # parse age groups
            chunk['age'] = chunk.loc[:,'age']\
                .replace({'Y_LT5': 'Y0-4', 'Y_GE90': 'Y90', 'Y_GE85': 'Y85'})\
                .replace({r'(.*)-(.*)':r'\1_\2', r'Y(.*)':r'\1'}, regex = True)
            # melt weeks to value
            chunk = chunk.melt(id_vars = ['sex','age','geo\\time'],
                               value_vars = data_columns,
                               var_name = "yearweek",
                               value_name = "deaths")
            chunk["year"] = chunk.yearweek.apply(lambda yw: int(yw.split("W")[0]))
            chunk["week"] = chunk.yearweek.apply(lambda yw: int(yw.split("W")[1]))
            
            chunk = chunk[["geo\\time","sex","age","year","week","deaths"]]
            chunk.columns = ["region","sex","age","year","week","deaths"]
            
            yield chunk

def deaths_to_file():
    """Saves deaths to file."""
    filename = pkg_resources.resource_filename(__name__, "data/deaths.csv")
    for i,chunk in enumerate(_parse_deaths()):
        # write
        if i == 0: chunk.to_csv(filename, mode='w', header=True, index=False)
        else: chunk.to_csv(filename, mode='a', header=False, index=False)

def deaths(regions = None, sex = None, age = None, start = None):
    """Reads data from Eurostat, filters and saves to CSV.
    
    Args:
        regions (list, optional): Filter of countries.
        
        start (datetime, optional): Start time. Will be rounded to week. Endtime is always end of data.
                                    Default is all the data (no filtering).
    """
    chunksize = 1
    data = None
    for i,chunk in enumerate(_parse_deaths(chunksize = chunksize)):
        # filter by region
        if regions:
            f = None
            for pre in regions:
                matches = chunk['region'].str.startswith(pre)
                f = f | matches if f is not None else matches
            chunk = chunk[f]
            # all chunk filtered out
            if len(chunk.index) == 0:
                logging.info(f"whole chunk filtered out")
                continue
        # filter by sex
        if sex:
            chunk = chunk[chunk.sex.isin(sex)]
            if len(chunk.index) == 0:
                logging.info(f"whole chunk filtered out")
                continue
        # filter by age
        if age:
            chunk = chunk[chunk.age.isin(age)]
            if len(chunk.index) == 0:
                logging.info(f"whole chunk filtered out")
                continue
        # filter by start
        if start:
            chunk = chunk[(chunk.year > start.year) |
                          ((chunk.year == start.year) & (chunk.week >= start.isocalendar()[1]))]
            if len(chunk.index) == 0:
                logging.info(f"whole chunk filtered out")
                continue
            
        if data is None: data = chunk
        else: data = data.append(chunk)
        logging.info(f"parsed {chunksize * (i + 1) * 10**3} lines")
    
    return data

__all__ = ["deaths"]

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    x = deaths(["CZ","PL"], start = datetime(2019,1,1))
    print(x)