import requests
import json
import pandas as pd
import datetime
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
import pymysql


#------------------------------------------------------------------------------------------------
# SQL Wrapper
#------------------------------------------------------------------------------------------------


def sql_query(query,cypher_key):
  # Returns a daframe object of the query response

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
  user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
  pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
  myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
  myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
  db = cipher_suite.decrypt(database_enc).decode("utf-8")

  myConnection = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)

  if query.split(' ')[0] != 'SELECT':
    print("Error. Please only use non destructive (SELECT) queries.")
    return "Please only use non destructive (SELECT) queries."

  response_df = pd.io.sql.read_sql(query, con=myConnection)

  myConnection.close()

  return response_df

def sql_query_destructive(query,cypher_key):

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
  user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
  pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
  myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
  myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
  db = cipher_suite.decrypt(database_enc).decode("utf-8")

  con = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)


  try:
    with con.cursor() as cur:
        cur.execute(query)
        con.commit()

  finally:
    con.close()









#------------------------------------------------------------------------------------------------
# APIs
#------------------------------------------------------------------------------------------------


def ss_calendar(listing_ids,check_in,check_out):

  parsed_listing_ids = str(listing_ids)[1:-1]
  parsed_listing_ids = parsed_listing_ids.replace("'","").replace(" ","")

  url = "https://www.saffronstays.com/calender_node.php"

  params={
      "listingList": parsed_listing_ids,
      "checkIn":check_in,
      "checkOut":check_out
      
  }
  payload = {}
  headers= {}

  response = requests.get(url, headers=headers, data = payload,params=params)
  response = json.loads(response.text.encode('utf8'))
  return response