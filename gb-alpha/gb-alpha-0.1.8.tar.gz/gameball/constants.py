from __future__ import absolute_import, division, print_function

# Configuration variables

api_key = None
transaction_key = None
default_http_client = None
api_base = "https://gb-api.azurewebsites.net/api/v2.0/integrations/"

events = 'event'
referral = 'referral'
reward_points = 'transaction/reward'
player_points_balance = 'transaction/balance'
hold_Points = 'transaction/hold'
redeem_points = 'transaction/redeem'
reverse_transaction = 'transaction/cancel'
reverse_hold = 'transaction/hold'
create_player = 'player'
player_info = 'player/info'
create_coupon = 'coupon'
validate_coupon = 'coupon/validate'
redeem_coupon = 'coupon/redeem'
send_action = 'action'
