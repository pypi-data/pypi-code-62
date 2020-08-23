from gameball.exceptions.gameball_exception import GameballException
from datetime import datetime
import gameball.utils

class playerObject(object):
    def __init__(
        self,
        player_unique_id,
        player_attributes = {},
        player_type_id= None,
        device_token = None,
        os_type = None,
        is_deleted = None,
        creation_date = None,
        last_update = None
    ):
        if len(str(player_unique_id)) < 1 or len(str(player_unique_id)) > 50:
            raise GameballException('player_unique_id should be between 1 and 50 letters')
        else:
            self.player_unique_id = player_unique_id
            
        self.player_type_id = player_type_id
        self.player_attributes = player_attributes
        self.device_token = device_token
        self.os_type = os_type
        self.is_deleted = is_deleted
        self.creation_date = creation_date
        self.last_update = last_update

    def add_player_attribute(self, attribute_name, value):
        self.player_attributes[attribute_name] = value
    
    def add_custom_player_attribute(self, attribute_name, value):
        custom_chk = self.player_attributes.get('custom', None)
        if custom_chk is None:
            self.player_attributes['custom'] = {}
        self.player_attributes['custom'][attribute_name] = value

    def set_player_type(self, type_id):
        self.player_type_id = type_id
    
    def set_device_token(self, device_token):
        self.device_token = device_token

    def set_os_type(self, os_type):
        self.os_type = os_type

    def set_is_deleted(self, is_deleted):
        self.is_deleted = is_deleted

    def set_creation_date(self, creation_date):
        self.creation_date = creation_date

    def set_last_update(self, last_update):
        self.last_update = last_update