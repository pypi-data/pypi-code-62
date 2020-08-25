import requests
import json
import pandas as pd
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
import pymysql

from helpers import *

#------------------------------------------------------------------------------------------------
# Level 1
#------------------------------------------------------------------------------------------------

def search_api(search_type='city',location="lonavala,%20maharashtra",guests=2,adults=2,childs=0,page_no=1):

  url = "https://searchapi.vistarooms.com/api/search/getresults"

  param={
    }

  payload = {
      
      "city": location,
      "search_type": "city",
      "checkin": "",
      "checkout": "",
      "total_guests": guests,
      "adults": adults,
      "childs": childs,
      "page": page_no,
      "min_bedrooms": 1,
      "max_bedrooms": 30,
      "amenity": [],
      "facilities": [],
      "price_start": 1000,
      "price_end": 5000000,
      "sort_by_price": ""
        
    }
  headers = {}

  response = requests.post(url, params=param, headers=headers, data=payload)
  search_data = json.loads(response.text.encode('utf8'))

  return search_data

def listing_api(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2),
                         guest=3,adult=3,child=0):
  
  url = "https://v3api.vistarooms.com/api/single-property"

  param={
          'slug': slug,
          'checkin': checkin,
          'checkout': checkout,
          'guest': guest,
          'adult': adult,
          'child': child    
      }

  payload = {}
  headers = {
  }

  response = requests.get(url, params=param, headers=headers, data = payload)
  property_deets = json.loads(response.text.encode('utf8'))
  return property_deets

def listing_other_details_api(slug='the-boulevard-villa'):

  url = "https://v3api.vistarooms.com/api/single-property-detail"

  param={
          'slug': slug,
      }

  payload = {}
  headers = {
  }
  
  response = requests.get(url, params=param, headers=headers, data = payload)
  property_other_deets = json.loads(response.text.encode('utf8'))
  return property_other_deets

def price_calculator_api(property_id='710', checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0):

  if type(checkin)==str:
    checkin = datetime.datetime.strptime(checkin,'%Y-%m-%d')
    checkout = datetime.datetime.strptime(checkout,'%Y-%m-%d')


  url = "https://v3api.vistarooms.com/api/price-breakup"
  
  param={
      'property_id': property_id,
      'checkin': checkin,
      'checkout': checkout,
      'guest': guest,
      'adult': adult,
      'child': child,   
      }

  payload = {}
  headers = {
  }

  response = requests.get(url, params=param, headers=headers, data = payload)
  pricing_deets = json.loads(response.text.encode('utf8'))
  return pricing_deets

def locations():
  locations = ["lonavala, maharashtra","goa, goa","alibaug, maharashtra","nainital, uttarakhand","chail, himanchal-pradesh","manali, himachal-pradesh","shimla, himanchal%20pradesh","ooty, tamil%20nadu","coorg, karnataka","dehradun, uttarakhand","jaipur, rajasthan","udaipur, rajasthan","mahabaleshwar, maharashtra","nashik, maharashtra"]
  return locations


#------------------------------------------------------------------------------------------------
# Level 2 
#------------------------------------------------------------------------------------------------


def search_locations_json(locations=["lonavala,%20maharashtra"],guests=2,get_all=False,wait_time=10):

  # Empty list to append (extend) all the data
  properties = []

  if get_all:
    locations = locations()

  # Outer loop - for each location
  for location in locations:

    page_no = 1

    # Inner Loop - for each page in location ( acc to the Vista Search API )
    while True:

      print(f"Page {page_no} for {location.split('%20')[0]} ")

      # Vista API call (search)
      search_data = search_api(location=location,guests=guests,page_no=page_no)

      # Break when you reach the last page for a location
      if not search_data['data']['properties']:
        break
        
      properties.extend(search_data['data']['properties'])
      page_no += 1

      time.sleep(wait_time)


  return properties

# Retruns a DATAFRAME for the above functions & **DROPS DUPLICATES (always use this for analysis)
def search_locations(locations=["lonavala,%20maharashtra"],guests=2,get_all=False,wait_time=10):
  villas = search_locations_json(locations=locations, guests=guests,get_all=get_all,wait_time=wait_time)
  villas = pd.DataFrame(villas)
  villas = villas.drop_duplicates('id')

  return villas


# Returns a JSON with the listing details
def listing(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2)):

  print("Fetching ",slug)
  # Vista API call (listing)
  property_deets = listing_api(slug=slug,guests=guests,checkin=checkin, checkout=checkout)
  
  # Get lat and long (diff API call)
  lat_long = listing_other_details_api(slug)['data']['location']

  # Get pricing for various durations
  weekday_pricing = price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(1))
  weekend_pricing = price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(5),checkout=next_weekday(5)+datetime.timedelta(1))
  entire_week_pricing = price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(7))
  entire_month_pricing = price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(30))

  # Add the extra fields in response (JSON)
  property_deets['data']['slug'] = slug
  property_deets['data']['lat'] = lat_long['latitude']
  property_deets['data']['lon'] = lat_long['longitude']
  property_deets['data']['checkin_date'] = checkin
  property_deets['data']['checkout_date'] = checkout
  property_deets['data']['weekday_pricing'] = weekday_pricing
  property_deets['data']['weekend_pricing'] = weekend_pricing
  property_deets['data']['entire_week_pricing'] = entire_week_pricing
  property_deets['data']['entire_month_pricing'] = entire_month_pricing
  property_deets['data']['price_per_room'] = property_deets['data']['price']['amount_to_be_paid']/property_deets['data']['property_detail']['number_of_rooms']

  return property_deets['data']

# Calculates the price for a duration (if unavailable, will automatically look for the next available dates) % Recursive function
def price_calculator(property_id, checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0, depth=0):

  date_diff = (checkout-checkin).days

  # Set the exit condition for the recursion depth ( to avoid an endless recursion / slowing down the scripts )
  if date_diff < 7:
    depth_lim = 15
    next_hop = 7
  elif date_diff >= 7 and date_diff < 29:
    depth_lim = 7
    next_hop = 7
  else:
    depth_lim = 5
    next_hop = date_diff
    
  if depth==depth_lim:
    return f"Villa Probably Inactive, checked till {checkin}"
  
  if type(checkin)==str:
    checkin = datetime.datetime.strptime(checkin,'%Y-%m-%d')
    checkout = datetime.datetime.strptime(checkout,'%Y-%m-%d')

  # Vista API call (Calculation)
  pricing = price_calculator_api(property_id=property_id, checkin=checkin, checkout=checkout, guest=guest, adult=adult, child=child)

  if 'error' in pricing.keys():

    # Recursion condition (Call self with next dates in case the dates are not available)
    if pricing['error'] == 'Booking Not Available for these dates':

      next_checkin = checkin + datetime.timedelta(next_hop)
      next_chekout = checkout + datetime.timedelta(next_hop)

      next_pricing = price_calculator(property_id,checkin=next_checkin ,checkout=next_chekout,depth=depth+1)
      return next_pricing

    # For other errors (Like invalid listing ID)
    else:
      return pricing['error']
      
    return next_pricing
  else:
    return pricing['data']['price']





#------------------------------------------------------------------------------------------------
# Level 3
#------------------------------------------------------------------------------------------------


# Use a list of slugs to generate a master DATAFRAME , this contains literally everything, ideal for any analysis on Vista
def master_dataframe(slugs=(['vista-greenwoods-five-villa','maison-calme-villa','vista-greenwoods-four-villa','mehta-mansion','villa-maira'])):
  
  total_slugs = len(slugs)
  temp_progress_counter = 0
  villas_deets = []   

  for slug in slugs:
    villa_deets = listing(slug=slug)
    villas_deets.append(villa_deets)
    villas_df = pd.DataFrame(villas_deets)

    temp_progress_counter += 1
    print("Done ",int((temp_progress_counter/total_slugs)*100),"%")

  prop_detail_df = pd.DataFrame(list(villas_df['property_detail']))
  agent_details_df =  pd.DataFrame(list(villas_df['agent_details']))
  price_df =  pd.DataFrame(list(villas_df['price']))

  literally_all_deets = pd.concat([prop_detail_df,villas_df,price_df,agent_details_df], axis=1)

  literally_all_deets = literally_all_deets.drop(['property_detail','mini_gallery', 'base_url',
       'agent_details', 'house_rule_pdf', 'mini_gallery_text',
       'seo','number_extra_guest', 'additionalcost',
       'days', 'min_occupancy', 'max_occupancy', 'amount_to_be_paid','total_guest',
       'extra_adult', 'extra_child', 'extra_adult_cost', 'extra_child_cost',
       'per_person','price','checkin_date','checkout_date','total_price','agent_short_words'], axis = 1)
  
  literally_all_deets['amenities'] = [[amenity['name'] for amenity in amenities] for amenities in literally_all_deets['amenities']]
  literally_all_deets['weekday_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['weekday_pricing']]
  literally_all_deets['weekend_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['weekend_pricing']]
  literally_all_deets['entire_week_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['entire_week_pricing']]
  literally_all_deets['entire_month_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['entire_month_pricing']]
  
  return literally_all_deets

def added_villas_dataframe(old_slugs,new_slugs):
  added_slugs = list(set(new_slugs).difference(set(old_slugs)))
  added_villas = []

  if added_slugs:
    added_villas = master_dataframe(added_slugs) 

  return added_villas




#------------------------------------------------------------------------------------------------
# SQL Functions
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
  db = "uat_ss_db"

  myConnection = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)

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
  db = "uat_ss_db"

  con = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)


  try:
    with con.cursor() as cur:
        cur.execute(query)
        con.commit()

  finally:
    con.close()







