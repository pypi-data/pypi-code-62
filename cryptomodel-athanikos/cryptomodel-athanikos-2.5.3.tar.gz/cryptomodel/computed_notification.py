import jsonpickle
from mongoengine import *

from calculator.helpers import if_none_raise
from cryptomodel.cryptostore import user_notification
from cryptomodel.notification_type import NOTIFICATION_TYPE

'''
Represents a a computed_user_notification 
Holds a notification 
Extends by holding the computed_date 
Result is programmatically added 
'''


class computed_notification(user_notification):
    meta = {'strict': False}
    computed_date = DateField()
    result = StringField()

    def set_result(self, value, computed_date):
        self.result = value
        self.computed_date = computed_date

    def get_result(self):
        if not hasattr(self, "result"):
            raise ValueError("does not exist : result ")
        if_none_raise(self.result)

        if self.notification_type == NOTIFICATION_TYPE.BALANCE.name:
            return jsonpickle.encode(self.result)
        else:
            raise NotImplementedError(self.notification_type)
