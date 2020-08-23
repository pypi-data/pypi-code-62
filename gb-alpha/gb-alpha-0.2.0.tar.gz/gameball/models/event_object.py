class eventObject(object):
    def __init__(
        self,
        player_unique_id,
        events = {},
        player_type_id= None,
        is_positive = None,
        player_attributes = {}

    ):
        self.player_unique_id = player_unique_id
        self.events = events
        self.player_type_id = player_type_id
        self.is_positive = is_positive
        self.player_attributes = player_attributes

    def add_event(self, event_name, event_metadata = {}):
        self.events[event_name] = event_metadata
    
    def set_player_type(self, type_id):
        self.player_type_id = type_id

    def add_player_attribute(self, attribute_name, value):
        self.player_attributes[attribute_name] = value
    
    def add_custom_player_attribute(self, attribute_name, value):
        custom_chk = self.player_attributes.get('custom', None)
        if custom_chk is None:
            self.player_attributes['custom'] = {}
        self.player_attributes['custom'][attribute_name] = value

