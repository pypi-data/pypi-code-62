""" This module contains OpenWebNet messages definition """

import datetime
from dateutil.relativedelta import relativedelta
import pytz
import re

MESSAGE_TYPE_ACTIVE_POWER = "active_power"
MESSAGE_TYPE_HOURLY_CONSUMPTION = "hourly_consumption"
MESSAGE_TYPE_DAILY_CONSUMPTION = "daily_consumption"
MESSAGE_TYPE_MONTHLY_CONSUMPTION = "monthly_consumption"
MESSAGE_TYPE_CURRENT_DAY_CONSUMPTION = "current_day_partial_consumption"
MESSAGE_TYPE_CURRENT_MONTH_CONSUMPTION = "current_month_partial_consumption"

class OWNMessage():

    _ACK = re.compile(r"^\*#\*1##$") #  *#*1##
    _NACK = re.compile(r"^\*#\*0##$") #  *#*1##
    _COMMAND_SESSION = re.compile(r"^\*99\*0##$") #  *99*0##
    _EVENT_SESSION = re.compile(r"^\*99\*1##$") #  *99*1##
    _NONCE = re.compile(r"^\*#(\d+)##$") #  *#123456789##
    _SHA = re.compile(r"^\*98\*(\d)##$") #  *98*SHA##

    _STATUS = re.compile(r"^\*(?P<who>\d+)\*(?P<what>\d+)(?P<what_param>(?:#\d+)*)\*(?P<where>\*|#?\d+)(?P<where_param>(?:#\d+)*)##$") #  *WHO*WHAT*WHERE##
    _STATUS_REQUEST = re.compile(r"^\*#(?P<who>\d+)\*(?P<where>#?\d+)(?P<where_param>(?:#\d+)*)##$") #  *#WHO*WHERE
    _DIMENSION_WRITING = re.compile(r"^\*#(?P<who>\d+)\*(?P<where>#?\d+)?(?P<where_param>(?:#\d+)*)?\*#(?P<dimension>\d+)(?P<dimension_param>(?:#\d+)*)?(?P<dimension_value>(?:\*\d+)+)##$") #  *#WHO*WHERE*#DIMENSION*VAL1*VALn##
    _DIMENSION_REQUEST = re.compile(r"^\*#(?P<who>\d+)\*(?P<where>#?\d+)?(?P<where_param>(?:#\d+)*)?\*(?P<dimension>\d+)##$") #  *#WHO*WHERE*DIMENSION##
    _DIMENSION_REQUEST_REPLY = re.compile(r"^\*#(?P<who>\d+)\*(?P<where>#?\d+)?(?P<where_param>(?:#\d+)*)?\*(?P<dimension>\d+)(?P<dimension_param>(?:#\d+)*)?(?P<dimension_value>(?:\*\d+)+)##$") #  *#WHO*WHERE*DIMENSION*VAL1*VALn##

    """ Base class for all OWN messages """
    def __init__(self, data):
        self._raw = data
        self._human_readable_log = self._raw
        self._family = ""
        self._who = ""
        self._where = ""

        if self._STATUS.match(self._raw):
            self._match = self._STATUS.match(self._raw)
            self._family = 'EVENT'
            self._type = 'STATUS'
            self._who = int(self._match.group('who'))
            self._what = int(self._match.group('what'))
            if self._what == 1000:
                self._family = 'COMMAND_TRANSLATION'
            self._what_param = self._match.group('what_param').split('#')
            del self._what_param[0]
            self._where = self._match.group('where')
            self._where_param = self._match.group('where_param').split('#')
            del self._where_param[0]
            self._dimension = None
            self._dimension_param = None
            self._dimension_value = None

        elif self._STATUS_REQUEST.match(self._raw):
            self._match = self._STATUS_REQUEST.match(self._raw)
            self._family = 'REQUEST'
            self._type = 'STATUS_REQUEST'
            self._who = int(self._match.group('who'))
            self._what = None
            self._what_param = None
            self._where = self._match.group('where')
            self._where_param = self._match.group('where_param').split('#')
            del self._where_param[0]
            self._dimension = None
            self._dimension_param = None
            self._dimension_value = None
        
        elif self._DIMENSION_REQUEST.match(self._raw):
            self._match = self._DIMENSION_REQUEST.match(self._raw)
            self._family = 'REQUEST'
            self._type = 'DIMENSION_REQUEST'
            self._who = int(self._match.group('who'))
            self._what = None
            self._what_param = None
            self._where = self._match.group('where')
            self._where_param = self._match.group('where_param').split('#')
            del self._where_param[0]
            self._dimension = int(self._match.group('dimension'))
            self._dimension_param = None
            self._dimension_value = None

        elif self._DIMENSION_REQUEST_REPLY.match(self._raw):
            self._match = self._DIMENSION_REQUEST_REPLY.match(self._raw)
            self._family = 'EVENT'
            self._type = 'DIMENSION_REQUEST_REPLY'
            self._who = int(self._match.group('who'))
            self._what = None
            self._what_param = None
            self._where = self._match.group('where')
            self._where_param = self._match.group('where_param').split('#')
            del self._where_param[0]
            self._dimension = int(self._match.group('dimension'))
            self._dimension_param = self._match.group('dimension_param').split('#')
            del self._dimension_param[0]
            self._dimension_value = self._match.group('dimension_value').split('*')
            del self._dimension_value[0]

        elif self._DIMENSION_WRITING.match(self._raw):
            self._match = self._DIMENSION_WRITING.match(self._raw)
            self._family = 'COMMAND'
            self._type = 'DIMENSION_WRITING'
            self._who = int(self._match.group('who'))
            self._what = None
            self._what_param = None
            self._where = self._match.group('where')
            self._where_param = self._match.group('where_param').split('#')
            del self._where_param[0]
            self._dimension = int(self._match.group('dimension'))
            self._dimension_param = self._match.group('dimension_param').split('#')
            del self._dimension_param[0]
            self._dimension_value = self._match.group('dimension_value').split('*')
            del self._dimension_value[0]
    
    @classmethod
    def parse(cls, data):
        if (cls._ACK.match(data) or 
            cls._NACK.match(data) or
            cls._COMMAND_SESSION.match(data) or
            cls._EVENT_SESSION.match(data) or
            cls._NONCE.match(data) or
            cls._SHA.match(data)):
            return OWNSignaling(data)
        elif (cls._STATUS.match(data) or
            cls._DIMENSION_REQUEST_REPLY.match(data)):
            return OWNEvent.parse(data)
        elif (cls._STATUS_REQUEST.match(data) or
            cls._DIMENSION_REQUEST.match(data) or
            cls._DIMENSION_WRITING.match(data)):
            return OWNCommand.parse(data)
        else:
            return None

    def is_event(self) -> bool:
        return self._family == 'EVENT'

    def is_command(self) -> bool:
        return self._family == 'COMMAND'

    def is_request(self) -> bool:
        return self._family == 'REQUEST'

    def is_translation(self) -> bool:
        return self._family == 'COMMAND_TRANSLATION'

    @property
    def who(self) -> str:
        """ The 'who' ID of the subject of this message """
        return self._who

    @property
    def where(self) -> str:
        """ The 'where' ID of the subject of this message """
        return self._where#[1:] if self._where.startswith('#') else self._where

    @property
    def entity(self) -> str:
        """ The ID of the subject of this message """
        return self.unique_id

    @property
    def unique_id(self) -> str:
        """ The ID of the subject of this message """
        return f"{self.who}-{self.where}"
    
    @property
    def human_readable_log(self) -> str:
        """ A human readable log of the event """
        return self._human_readable_log

    def __repr__(self) -> str:
        return self._raw

    def __str__(self) -> str:
        return self._raw

class OWNEvent(OWNMessage):
    """ This class is a subclass of messages. All messages received during an event session are events.
    Dividing this in a subclass provides better clarity """

    def __init__(self, data):
        super().__init__(data)

    @classmethod
    def parse(cls, data):
        _match = re.match(r"^\*#?(?P<who>\d+)\*.+##$", data)
        
        if _match:
            _who = int(_match.group('who'))
        
            if _who == 0:
                return OWNScenarioEvent(data)
            elif _who == 1:
                return OWNLightingEvent(data)
            elif _who == 2:
                return OWNAutomationEvent(data)
            elif _who == 4:
                return OWNHeatingEvent(data)
            elif _who == 5:
                return OWNAlarmEvent(data)
            elif _who == 9:
                return OWNAuxEvent(data)
            elif _who == 13:
                return OWNGatewayEvent(data)
            elif _who == 15:
                return OWNCENEvent(data)
            elif _who == 17:
                return OWNSceneEvent(data)
            elif _who == 18:
                return OWNEnergyEvent(data)
            elif _who == 25:
                _where = re.match(r"^\*.+\*(?P<where>\d+)##$", data).group('where')
                if _where.startswith('2'):
                    return OWNCENPlusEvent(data)
                elif _where.startswith('3'):
                    return OWNDryContactEvent(data)

        return None

class OWNScenarioEvent(OWNEvent):

    def __init__(self, data):
        super().__init__(data)

        self._scenario = self._what
        self._control_panel = self._where
        self._human_readable_log = f"Scenario {self._scenario} from control panel {self._control_panel} has been launched."

    @property
    def scenario(self):
        return self._scenario

    @property
    def controlPanel(self):
        return self._control_panel

class OWNLightingEvent(OWNEvent):

    def __init__(self, data):
        super().__init__(data)

        self._state = None
        self._brightness = None
        self._timer = None

        if self._what is not None and self._what != 1000:
            self._state = self._what

            if self._state == 0:
                self._human_readable_log = f"Light {self._where} is switched off."
            elif self._state == 1:
                self._human_readable_log = f"Light {self._where} is switched on."
            elif self._state > 1 and self._state < 11:
                self._brightness = self._state * 10
                self._human_readable_log = f"Light {self._where} is switched on at {self._brightness}%."
            elif self._state == 11:
                self._timer = 60
                self._human_readable_log = f"Light {self._where} is switched on for {self._timer}s."
            elif self._state == 12:
                self._timer = 120
                self._human_readable_log = f"Light {self._where} is switched on for {self._timer}s."
            elif self._state == 13:
                self._timer = 180
                self._human_readable_log = f"Light {self._where} is switched on for {self._timer}s."
            elif self._state == 14:
                self._timer = 240
                self._human_readable_log = f"Light {self._where} is switched on for {self._timer}s."
            elif self._state == 15:
                self._timer = 300
                self._human_readable_log = f"Light {self._where} is switched on for {self._timer}s."
            elif self._state == 16:
                self._timer = 900
                self._human_readable_log = f"Light {self._where} is switched on for {self._timer}s."
            elif self._state == 17:
                self._timer = 30
                self._human_readable_log = f"Light {self._where} is switched on for {self._timer}s."
            elif self._state == 18:
                self._timer = 0.5
                self._human_readable_log = f"Light {self._where} is switched on for {self._timer}s."
        
        if self._dimension is not None:
            if self._dimension == 1:
                self._brightness = int(self._dimension_value[0]) - 100
                if self._brightness == 0:
                    self._state = 0
                    self._human_readable_log = f"Light {self._where} is switched off."
                else:
                    self._state = 1
                    self._human_readable_log = f"Light {self._where} is switched on at {self._brightness}%."
            elif self._dimension == 2:
                self._timer = int(self._dimension_value[0])*3600 + int(self._dimension_value[1])*60 + int(self._dimension_value[2])
                self._human_readable_log = f"Light {self._where} is switched on for {self._timer}s."

    @property
    def brightness(self):
        return self._brightness

    @property
    def is_on(self):
        return self._state > 0
    
    @property
    def timer(self):
        return self._timer

class OWNAutomationEvent(OWNEvent):
    def __init__(self, data):
        super().__init__(data)

        self._state = None
        self._position = None
        self._priority = None
        self._info = None
        self._is_opening = None
        self._is_closing = None
        self._is_closed = None

        if self._what is not None and self._what != 1000:
            self._state = self._what

        if self._dimension is not None:
            if self._dimension == 10:
                self._state = int(self._dimension_value[0])
                self._position = int(self._dimension_value[1])
                self._priority = int(self._dimension_value[2])
                self._info = int(self._dimension_value[3])

        if self._state == 0:
            self._human_readable_log = f"Cover {self._where} stopped."
            self._is_opening = False
            self._is_closing = False
        elif self._state == 10:
            self._is_opening = False
            self._is_closing = False
            if self._position == 0:
                self._human_readable_log = f"Cover {self._where} is closed."
                self._is_closed = True
            else:
                self._human_readable_log = f"Cover {self._where} is opened at {self._position}%."
                self._is_closed = False
        else:
            if self._state == 1:
                self._human_readable_log = f"Cover {self._where} is opening."
                self._is_opening = True
                self._is_closing = False
            elif self._state == 11 or  self._state == 13:
                self._human_readable_log = f"Cover {self._where} is opening from intial position {self._position}."
                self._is_opening = True
                self._is_closing = False
                self._is_closed = False
            elif self._state == 2:
                self._human_readable_log = f"Cover {self._where} is closing."
                self._is_closing = True
                self._is_opening = False
            elif self._state == 12 or self._state == 14:
                self._human_readable_log = f"Cover {self._where} is closing from intial position {self._position}."
                self._is_closing = True
                self._is_opening = False
                self._is_closed = False
    
    @property
    def state(self):
        return self._state
    
    @property
    def is_opening(self):
        return self._is_opening

    @property
    def is_closing(self):
        return self._is_closing

    @property
    def is_closed(self):
        return self._is_closed

    @property
    def currentPosition(self):
        return self._position

class OWNHeatingEvent(OWNEvent):

    def __init__(self, data):
        super().__init__(data)

class OWNAlarmEvent(OWNEvent):

    def __init__(self, data):
        super().__init__(data)

        self._state_code = int(self._what)
        self._state = None
        self._system = False
        self._zone = None
        self._sensor = None

        if self._where == "*":
            self._system = True
            self._human_readable_log = "System is reporting: "
        elif self._where.startswith('#'):
            self._zone = self._where[1:]
            if self._zone == '12':
                self._zone = 'c'
            elif self._zone == '15':
                self._zone = 'f'
            else:
                self._sensor = int(self._zone[1:])
                self._zone = int(self._zone[0])
            self._human_readable_log = f"Zone {self._zone} is reporting: "
        else:
            self._zone = int(self._where[0])
            self._sensor = int(self._where[1:])
            if self._zone == 0 :
                self._human_readable_log = f"Device {self._sensor} in input zone is reporting: "
            else:
                self._human_readable_log = f"Sensor {self._sensor} in zone {self._zone} is reporting: "

        if self._state_code == 0:
            self._state = 'maintenance'
        elif self._state_code == 1:
            self._state = 'activation'
        elif self._state_code == 2:
            self._state = 'deactivation'
        elif self._state_code == 3:
            self._state = 'delay end'
        elif self._state_code == 4:
            self._state = 'system battery fault'
        elif self._state_code == 5:
            self._state = 'battery ok'
        elif self._state_code == 6:
            self._state = 'no network'
        elif self._state_code == 7:
            self._state = 'network present'
        elif self._state_code == 8:
            self._state = 'engage'
        elif self._state_code == 9:
            self._state = 'disengage'
        elif self._state_code == 10:
            self._state = 'battery unloads'
        elif self._state_code == 11:
            self._state = 'active zone'
        elif self._state_code == 12:
            self._state = 'technical alarm'
        elif self._state_code == 13:
            self._state = 'reset technical alarm'
        elif self._state_code == 14:
            self._state = 'no reception'
        elif self._state_code == 15:
            self._state = 'intrusion alarm'
        elif self._state_code == 16:
            self._state = 'tampering'
        elif self._state_code == 17:
            self._state = 'anti-panic alarm'
        elif self._state_code == 18:
            self._state = 'non-active zone'
        elif self._state_code == 26:
            self._state = 'start programming'
        elif self._state_code == 27:
            self._state = 'stop programming'
        elif self._state_code == 31:
            self._state = 'silent alarm'

        self._human_readable_log = f"{self._human_readable_log}'{self._state}'."

    @property
    def general(self):
        return self._system
    
    @property
    def zone(self):
        return self._zone

    @property
    def sensor(self):
        return self._sensor

    @property
    def is_active(self):
        return self._state_code == 1 or self._state_code == 11

    @property
    def is_engaged(self):
        return self._state_code == 8

    @property
    def is_alarm(self):
        return self._state_code == 12 or self._state_code == 15 or self._state_code == 16 or self._state_code == 17 or self._state_code == 31
            
class OWNAuxEvent(OWNEvent):

    def __init__(self, data):
        super().__init__(data)

        self._channel = self._where

        self._state = self._what
        if self._state == 0:
            self._human_readable_log = f"Auxilliary channel {self._channel} is set to 'OFF'."
        elif self._state == 1:
            self._human_readable_log = f"Auxilliary channel {self._channel} is set to 'ON'."
        elif self._state == 2:
            self._human_readable_log = f"Auxilliary channel {self._channel} is set to 'TOGGLE'."
        elif self._state == 3:
            self._human_readable_log = f"Auxilliary channel {self._channel} is set to 'STOP'."
        elif self._state == 4:
            self._human_readable_log = f"Auxilliary channel {self._channel} is set to 'UP'."
        elif self._state == 5:
            self._human_readable_log = f"Auxilliary channel {self._channel} is set to 'DOWN'."
        elif self._state == 6:
            self._human_readable_log = f"Auxilliary channel {self._channel} is set to 'ENABLED'."
        elif self._state == 7:
            self._human_readable_log = f"Auxilliary channel {self._channel} is set to 'DISABLED'."
        elif self._state == 8:
            self._human_readable_log = f"Auxilliary channel {self._channel} is set to 'RESET_GEN'."
        elif self._state == 9:
            self._human_readable_log = f"Auxilliary channel {self._channel} is set to 'RESET_BI'."
        elif self._state == 10:
            self._human_readable_log = f"Auxilliary channel {self._channel} is set to 'RESET_TRI'."

    @property
    def channel(self):
        return self._channel

    @property
    def state_code(self):
        return self._state

    @property
    def is_on(self):
        return self._state == 1      

class OWNGatewayEvent(OWNEvent):

    def __init__(self, data):
        super().__init__(data)

        self._year = None
        self._month  = None
        self._day = None
        self._hour = None
        self._minute = None
        self._second = None
        self._timezone = None

        self._time = None
        self._date = None
        self._datetime = None

        self._ip_address = None
        self._netmask = None
        self._mac_address = None

        self._device_type = None
        self._firmware_version = None

        self._uptime = None

        self._kernel_version = None
        self._distribution_version = None

        if self._dimension == 0:
            self._hour = self._dimension_value[0]
            self._minute = self._dimension_value[1]
            self._second = self._dimension_value[2]
            self._timezone = f"+{self._dimension_value[3][1:]}" if self._dimension_value[3][0] == "0" else f"-{self._dimension_value[3][1:]}"
            self._time = datetime.time.fromisoformat(f"{self._hour}:{self._minute}:{self._second}{self._timezone}:00")
            self._human_readable_log = f"Gateway's internal time is: {self._hour}:{self._minute}:{self._second} UTC {self._timezone}."

        elif self._dimension == 1:
            self._year = self._dimension_value[3]
            self._month = self._dimension_value[2]
            self._day = self._dimension_value[1]
            self._date = datetime.date(year=int(self._year), month=int(self._month), day=int(self._day))
            self._human_readable_log = f"Gateway's internal date is: {self._year}-{self._month}-{self._day}."

        elif self._dimension == 10:
            self._ip_address = f"{self._dimension_value[0]}.{self._dimension_value[1]}.{self._dimension_value[2]}.{self._dimension_value[3]}"
            self._human_readable_log = f"Gateway's IP address is: {self._ip_address}."

        elif self._dimension == 11:
            self._netmask = f"{self._dimension_value[0]}.{self._dimension_value[1]}.{self._dimension_value[2]}.{self._dimension_value[3]}"
            self._human_readable_log = f"Gateway's netmask is: {self._netmask}."

        elif self._dimension == 12:
            self._mac_address = f"{int(self._dimension_value[0]):02x}:{int(self._dimension_value[1]):02x}:{int(self._dimension_value[2]):02x}:{int(self._dimension_value[3]):02x}:{int(self._dimension_value[4]):02x}:{int(self._dimension_value[5]):02x}"
            self._human_readable_log = f"Gateway's MAC address is: {self._mac_address}."
            
        elif self._dimension == 15:
            if self._dimension_value[0] == "2":
                self._device_type = "MHServer"
            elif self._dimension_value[0] == "4":
                self._device_type = "MH200"
            elif self._dimension_value[0] == "6":
                self._device_type = "F452"
            elif self._dimension_value[0] == "7":
                self._device_type = "F452V"
            elif self._dimension_value[0] == "11":
                self._device_type = "MHServer2"
            elif self._dimension_value[0] == "13":
                self._device_type = "H4684"
            elif self._dimension_value[0] == "200":
                self._device_type = "F454"
            else:
                self._device_type = f"Unknown ({self._dimension_value[0]})"
            self._human_readable_log = f"Gateway device type is: {self._device_type}."
            
        elif self._dimension == 16:
            self._firmware_version = f"{self._dimension_value[0]}.{self._dimension_value[1]}.{self._dimension_value[2]}"
            self._human_readable_log = f"Gateway's firmware version is: {self._firmware_version}."

        elif self._dimension == 19:
            self._uptime = datetime.timedelta(days=int(self._dimension_value[0]), hours=int(self._dimension_value[1]), minutes=int(self._dimension_value[2]), seconds=int(self._dimension_value[3]))
            self._human_readable_log = f"Gateway's uptime is: {self._uptime}."

        elif self._dimension == 22:
            self._hour = self._dimension_value[0]
            self._minute = self._dimension_value[1]
            self._second = self._dimension_value[2]
            self._timezone = f"+{self._dimension_value[3][1:]}" if self._dimension_value[3][0] == "0" else f"-{self._dimension_value[3][1:]}"
            self._day = self._dimension_value[5]
            self._month = self._dimension_value[6]
            self._year = self._dimension_value[7]
            self._datetime = datetime.datetime.fromisoformat(f"{self._year}-{self._month}-{self._day}*{self._hour}:{self._minute}:{self._second}{self._timezone}:00")
            self._human_readable_log = f"Gateway's internal datetime is: {self._datetime}."
    
        elif self._dimension == 23:
            self._kernel_version = f"{self._dimension_value[0]}.{self._dimension_value[1]}.{self._dimension_value[2]}"
            self._human_readable_log = f"Gateway's kernel version is: {self._kernel_version}."
            
        elif self._dimension == 24:
            self._distribution_version = f"{self._dimension_value[0]}.{self._dimension_value[1]}.{self._dimension_value[2]}"
            self._human_readable_log = f"Gateway's distribution version is: {self._distribution_version}."

class OWNCENEvent(OWNEvent):

    def __init__(self, data):
        super().__init__(data)

        try:
            self._state = self._what_param[0]
        except IndexError:    
            self._state = None
        self.push_button = self._what
        self.object = self._where

        if self._state == None:
            self._human_readable_log = f"Button {self.push_button} of CEN object {self.object} has been pressed."
        elif int(self._state) == 3:
            self._human_readable_log = f"Button {self.push_button} of CEN object {self.object} is being held pressed."
        elif int(self._state) == 1:
            self._human_readable_log = f"Button {self.push_button} of CEN object {self.object} has been released after a short press."
        elif int(self._state) == 2:
            self._human_readable_log = f"Button {self.push_button} of CEN object {self.object} has been released after a long press."

    @property
    def is_pressed(self):
        return self._state == None

    @property
    def is_held(self):
        return int(self._state) == 3

    @property
    def is_released_after_short_press(self):
        return int(self._state) == 1

    @property
    def is_released_after_long_press(self):
        return int(self._state) == 2

class OWNSceneEvent(OWNEvent):

    def __init__(self, data):
        super().__init__(data)

        self._scene = self._where
        self._state = self._what

        if self._state == 1:
            _status = "started"
        elif self._state == 2:
            _status = "stoped"
        elif self._state == 3:
            _status = "enabled"
        elif self._state == 4:
            _status = "disabled"

        self._human_readable_log = f"Scene {self._scene} is {_status}."

    @property
    def scenario(self):
        return self._scene

    @property
    def state(self):
        return self._state

    @property
    def is_on(self):
        if self._state == 1:
            return True
        elif self._state == 2:
            return False
        else:
            return None
    
    @property
    def is_enabled(self):
        if self._state == 3:
            return True
        elif self._state == 4:
            return False
        else:
            return None

class OWNEnergyEvent(OWNEvent):

    def __init__(self, data):
        super().__init__(data)

        if  not self._where.startswith('5'):
            return None
        
        self._type = None
        self._sensor = self._where[1:]
        self._active_power = 0
        self._hourly_consumption = dict()
        self._daily_consumption = dict()
        self._current_day_partial_consumption = 0
        self._monthly_consumption = dict()
        self._current_month_partial_consumption = 0
        
        if self._dimension is not None:
            if self._dimension == 113:
                self._type = MESSAGE_TYPE_ACTIVE_POWER
                self._active_power = int(self._dimension_value[0])
                self._human_readable_log = f"Sensor {self._sensor} is reporting an active power draw of {self._active_power} W."
            elif self._dimension == 511:
                _now = datetime.date.today()
                _messageDate =  datetime.date(_now.year, int(self._dimension_param[0]), int(self._dimension_param[1]))
                if _messageDate > _now:
                    _messageDate.replace(year= _now.year - 1)

                if int(self._dimension_value[0]) != 25:
                    self._type = MESSAGE_TYPE_HOURLY_CONSUMPTION
                    self._hourly_consumption['date'] = _messageDate
                    self._hourly_consumption['hour'] = int(self._dimension_value[0])
                    self._hourly_consumption['value'] = int(self._dimension_value[1])
                    self._human_readable_log = f"Sensor {self._sensor} is reporting a power consumtion of {self._hourly_consumption['value']} Wh for {self._hourly_consumption['date']} at {self._hourly_consumption['hour']}."
                else:
                    self._type = MESSAGE_TYPE_DAILY_CONSUMPTION
                    self._daily_consumption['date'] = _messageDate
                    self._daily_consumption['value'] = int(self._dimension_value[1])
                    self._human_readable_log = f"Sensor {self._sensor} is reporting a power consumtion of {self._daily_consumption['value']} Wh for {self._daily_consumption['date']}."
            elif self._dimension == 513 or self._dimension == 514:
                _now = datetime.date.today()
                _messageMonth = datetime.date(_now.year, int(self._dimension_param[0]), 1)
                try:
                    if self._dimension == 513 and _messageMonth > _now:
                        _messageDate = datetime.date(_now.year - 1, int(self._dimension_param[0]), int(self._dimension_value[0]))
                    elif self._dimension == 514:
                        if _messageMonth > _now:
                            _messageDate = datetime.date(_now.year - 2, int(self._dimension_param[0]), int(self._dimension_value[0]))
                        else:
                            _messageDate = datetime.date(_now.year - 1, int(self._dimension_param[0]), int(self._dimension_value[0]))
                    else:
                        _messageDate = datetime.date(_now.year, int(self._dimension_param[0]), int(self._dimension_value[0]))
                except ValueError as e:
                    return None
                self._type = MESSAGE_TYPE_DAILY_CONSUMPTION
                self._daily_consumption['date'] = _messageDate
                self._daily_consumption['value'] = int(self._dimension_value[1])
                self._human_readable_log = f"Sensor {self._sensor} is reporting a power consumtion of {self._daily_consumption['value']} Wh for {self._daily_consumption['date']}."
            elif self._dimension == 54:
                self._type = MESSAGE_TYPE_CURRENT_DAY_CONSUMPTION
                self._current_day_partial_consumption = int(self._dimension_value[0])
                self._human_readable_log = f"Sensor {self._sensor} is reporting a power consumtion of {self._current_day_partial_consumption} Wh up to now today."
            elif self._dimension == 52:
                self._type = MESSAGE_TYPE_MONTHLY_CONSUMPTION
                _messageDate =  datetime.date(int(f"20{self._dimension_param[0]}"), self._dimension_param[1], 1)
                self._monthly_consumption['date'] = _messageDate
                self._monthly_consumption['value'] = int(self._dimension_value[0])
                self._human_readable_log = f"Sensor {self._sensor} is reporting a power consumtion of {self._monthly_consumption['value']} Wh for {self._monthly_consumption['date'].strftime('%B %Y')}."
            elif self._dimension == 53:
                self._type = MESSAGE_TYPE_CURRENT_MONTH_CONSUMPTION
                self._current_month_partial_consumption = int(self._dimension_value[0])
                self._human_readable_log = f"Sensor {self._sensor} is reporting a power consumtion of {self._current_month_partial_consumption} Wh up to now this month."

    @property
    def message_type(self):
        return self._type

    @property
    def active_power(self):
        return self._active_power
    
    @property
    def hourly_consumption(self):
        return self._hourly_consumption
    
    @property
    def daily_consumption(self):
        return self._daily_consumption
    
    @property
    def current_day_partial_consumption(self):
        return self._current_day_partial_consumption
    
    @property
    def monthly_consumption(self):
        return self._monthly_consumption

    @property
    def current_month_partial_consumption(self):
        return self._current_month_partial_consumption

    @property
    def human_readable_log(self):
        return self._human_readable_log
        
class OWNDryContactEvent(OWNEvent):

    def __init__(self, data):
        super().__init__(data)

        self._state = 1 if self._what == 31 else 0
        self._detection = int(self._what_param[0])
        self._sensor = self._where[1:]

        if self._detection == 1:
            self._human_readable_log = f"Sensor {self._sensor} detected {'ON' if self._state == 1 else 'OFF'}."
        else:
            self._human_readable_log = f"Sensor {self._sensor} reported {'ON' if self._state == 1 else 'OFF'}."

    @property
    def is_on(self):
        return self._state == 1
    
    @property
    def is_detection(self):
        return self._detection == 1

    @property
    def human_readable_log(self):
        return self._human_readable_log

class OWNCENPlusEvent(OWNEvent):

    def __init__(self, data):
        super().__init__(data)

        self._state = self._what
        self.push_button = int(self._what_param[0])
        self.object = self._where[1:]

        if self._state == 21:
            self._human_readable_log = f"Button {self.push_button} of CEN+ object {self.object} has been pressed"
        elif self._state == 22:
            self._human_readable_log = f"Button {self.push_button} of CEN+ object {self.object} is being held pressed"
        elif self._state == 23:
            self._human_readable_log = f"Button {self.push_button} of CEN+ object {self.object} is still being held pressed"
        elif self._state == 24:
            self._human_readable_log = f"Button {self.push_button} of CEN+ object {self.object} has been released"
        elif self._state == 25:
            self._human_readable_log = f"Button {self.push_button} of CEN+ object {self.object} has been slowly rotated clockwise"
        elif self._state == 26:
            self._human_readable_log = f"Button {self.push_button} of CEN+ object {self.object} has been quickly rotated clockwise"
        elif self._state == 27:
            self._human_readable_log = f"Button {self.push_button} of CEN+ object {self.object} has been slowly rotated counter-clockwise"
        elif self._state == 28:
            self._human_readable_log = f"Button {self.push_button} of CEN+ object {self.object} has been quickly rotated counter-clockwise"
    
    @property
    def is_short_pressed(self):
        return self._state == 21

    @property
    def is_held(self):
        return self._state == 22
    
    @property
    def is_still_held(self):
        return self._state == 23

    @property
    def is_released(self):
        return self._state == 24

    @property
    def is_slowly_turned_CW(self):
        return self._state == 25

    @property
    def is_quickly_turned_CW(self):
        return self._state == 26

    @property
    def is_slowly_turned_CCW(self):
        return self._state == 27

    @property
    def is_quickly_turned_CCW(self):
        return self._state == 28

    @property
    def human_readable_log(self):
        return self._human_readable_log

class OWNCommand(OWNMessage):
    """ This class is a subclass of messages. All messages sent during a command session are commands.
    Dividing this in a subclass provides better clarity """

    def __init__(self, data):
        super().__init__(data)

    @classmethod
    def parse(cls, data):
        _match = re.match(r"^\*#?(?P<who>\d+)\*.+##$", data)
        
        if _match:
            _who = int(_match.group('who'))
        
            if _who == 0:
                return cls(data)
            elif _who == 1:
                return OWNLightingCommand(data)
            elif _who == 2:
                return OWNAutomationCommand(data)
            elif _who == 4:
                return cls(data)
            elif _who == 5:
                return cls(data)
            elif _who == 9:
                return cls(data)
            elif _who == 13:
                return OWNGatewayCommand(data)
            elif _who == 15:
                return cls(data)
            elif _who == 17:
                return cls(data)
            elif _who == 18:
                return OWNEnergyCommand(data)
            elif _who == 25:
                _where = re.match(r"^\*.+\*(?P<where>\d+)##$", data).group('where')
                if _where.startswith('2'):
                    return cls(data)
                elif _where.startswith('3'):
                    return OWNDryContactCommand(data)

        return None

class OWNLightingCommand(OWNCommand):

    def __init__(self, data):
        super().__init__(data)
    
    @classmethod
    def status(cls, where):
        message = cls(f"*#1*{where}##")
        message._human_readable_log = f"Requesting light or switch {where} status."
        return message

    @classmethod
    def switch_on(cls, where):
        message = cls(f"*1*1*{where}##")
        message._human_readable_log = f"Switching ON light or switch {where}."
        return message

    @classmethod
    def switch_off(cls, where):
        message = cls(f"*1*0*{where}##")
        message._human_readable_log = f"Switching OFF light or switch {where}."
        return message

    @classmethod
    def set_brightness(cls, where, _level=30):
        command_level = int(_level)+100
        message = cls(f"*#1*{where}*#1*{command_level}*0##")
        message._human_readable_log = f"Setting light {where} brightness to {_level}%."
        return message

class OWNAutomationCommand(OWNCommand):

    def __init__(self, data):
        super().__init__(data)
    
    @classmethod
    def status(cls, where):
        message = cls(f"*#2*{where}##")
        message._human_readable_log = f"Requesting shutter {where} status."
        return message

    @classmethod
    def raise_shutter(cls, where):
        message = cls(f"*2*1*{where}##")
        message._human_readable_log = f"Raising shutter {where}."
        return message
    
    @classmethod
    def lower_shutter(cls, where):
        message = cls(f"*2*2*{where}##")
        message._human_readable_log = f"Lowering shutter {where}."
        return message

    @classmethod
    def stop_shutter(cls, where):
        message = cls(f"*2*0*{where}##")
        message._human_readable_log = f"Stoping shutter {where}."
        return message

    @classmethod
    def set_shutter_level(cls, where, level=30):
        message = cls(f"*#2*{where}*#11#001*{level}##")
        message._human_readable_log = f"Setting shutter {where} position to {level}%."
        return message

class OWNGatewayCommand(OWNCommand):

    def __init__(self, data):
        super().__init__(data)

        self._year = None
        self._month  = None
        self._day = None
        self._hour = None
        self._minute = None
        self._second = None
        self._timezone = None

        self._time = None
        self._date = None
        self._datetime = None

        if self._dimension == 0:
            self._hour = self._dimension_value[0]
            self._minute = self._dimension_value[1]
            self._second = self._dimension_value[2]
            self._timezone = f"+{self._dimension_value[3][1:]}" if self._dimension_value[3][0] == "0" else f"-{self._dimension_value[3][1:]}"
            self._time = datetime.time.fromisoformat(f"{self._hour}:{self._minute}:{self._second}{self._timezone}:00")
            self._human_readable_log = f"Gateway broadcasting internal time: {self._time}."

        elif self._dimension == 1:
            self._year = self._dimension_value[3]
            self._month = self._dimension_value[2]
            self._day = self._dimension_value[1]
            self._date = datetime.date(year=int(self._year), month=int(self._month), day=int(self._day))
            self._human_readable_log = f"Gateway broadcasting internal date: {self._date}."

        elif self._dimension == 22:
            self._hour = self._dimension_value[0]
            self._minute = self._dimension_value[1]
            self._second = self._dimension_value[2]
            self._timezone = f"+{self._dimension_value[3][1:]}" if self._dimension_value[3][0] == "0" else f"-{self._dimension_value[3][1:]}"
            self._day = self._dimension_value[5]
            self._month = self._dimension_value[6]
            self._year = self._dimension_value[7]
            self._datetime = datetime.datetime.fromisoformat(f"{self._year}-{self._month}-{self._day}*{self._hour}:{self._minute}:{self._second}{self._timezone}:00")
            self._human_readable_log = f"Gateway broadcasting internal datetime: {self._datetime}."
    
    @classmethod
    def set_datetime_to_now(cls, time_zone: str):
        timezone = pytz.timezone(time_zone)
        now = timezone.localize(datetime.datetime.now())
        timezone_offset = f"0{now.strftime('%z')[1:3]}" if now.strftime('%z')[0] == "+" else f"1{now.strftime('%z')[1:3]}"
        message = cls(f"*#13**#22*{now.strftime('%H*%M*%S')}*{timezone_offset}*0{now.strftime('%w*%d*%m*%Y##')}")
        message._human_readable_log = f"Setting gateway time to: {message._datetime}."
        return message

    @classmethod
    def set_date_to_today(cls, time_zone: str):
        timezone = pytz.timezone(time_zone)
        now = timezone.localize(datetime.datetime.now())
        message = cls(f"*#13**#1*0{now.strftime('%w*%d*%m*%Y##')}")
        message._human_readable_log = f"Setting gateway date to: {message._date}."
        return message

    @classmethod
    def set_time_to_now(cls, time_zone: str):
        timezone = pytz.timezone(time_zone)
        now = timezone.localize(datetime.datetime.now())
        timezone_offset = f"0{now.strftime('%z')[1:3]}" if now.strftime('%z')[0] == "+" else f"1{now.strftime('%z')[1:3]}"
        message = cls(f"*#13**#0*{now.strftime('%H*%M*%S')}*{timezone_offset}*##")
        message._human_readable_log = f"Setting gateway time to: {message._time}."
        return message

class OWNEnergyCommand(OWNCommand):

    def __init__(self, data):
        super().__init__(data)

    @classmethod
    def start_sending_instant_power(cls, where, duration: int = 65):
        duration = 255 if duration > 255 else duration
        message = cls(f"*#18*{where}*#1200#1*{duration}##")
        message._human_readable_log = f"Requesting instant power draw update from sensor {where} for {duration} minutes."
        return message

    @classmethod
    def get_hourly_consumption(cls, where, date: datetime.date):
        date_month = date.month
        date_day = date.day
        today = datetime.date.today()
        one_year_ago = datetime.date(year=today.year-1, month=today.month, day=today.day)
        if date < one_year_ago:
            return None
        message = cls(f"*#18*{where}*511#{date.month}#{date.day}##")
        message._human_readable_log = f"Requesting hourly power consumption from sensor {where} for {date}."
        return message

    @classmethod
    def get_partial_daily_consumption(cls, where):
        message = cls(f"*#18*{where}*54##")
        message._human_readable_log = f"Requesting today's partial power consumption from sensor {where}."
        return message

    @classmethod
    def get_daily_consumption(cls, where, year, month):
        today = datetime.date.today()
        one_year_ago = today - relativedelta(years=1)
        two_year_ago = today - relativedelta(years=2)
        target = datetime.date(year=year, month=month, day=1)
        if target > today:
            return None
        elif target > one_year_ago:
            message = cls(f"*18*59#{month}*{where}##")
        elif target > two_year_ago:
            message = cls(f"*18*510#{month}*{where}##")
        else:
            return None
        message._human_readable_log = f"Requesting daily power consumption for {year}-{month} from sensor {where}."
        return message

    @classmethod
    def get_monthly_consumption(cls, where, year, month):
        message = cls(f"*#18*{where}*52#{str(year)[2:]}#{month}##")
        message._human_readable_log = f"Requesting monthly power consumption for {year}-{month} from sensor {where}."
        return message



class OWNDryContactCommand(OWNCommand):

    def __init__(self, data):
        super().__init__(data)
    
    @classmethod
    def status(cls, where):
        message = cls(f"*#25*{where}##")
        message._human_readable_log = f"Requesting dry contact {where} status."
        return message

class OWNSignaling(OWNMessage):
    """ This class is a subclass of messages. It is dedicated to signaling messages such as ACK or Authentication negotiation """

    def __init__(self, data):
        self._raw = data

        if self._ACK.match(self._raw):
            self._match = self._ACK.match(self._raw)
            self._family = 'SIGNALING'
            self._type = 'ACK'
            self._human_readable_log = "ACK."
        elif self._NACK.match(self._raw):
            self._match = self._NACK.match(self._raw)
            self._family = 'SIGNALING'
            self._type = 'NACK'
            self._human_readable_log = "NACK."
        elif self._NONCE.match(self._raw):
            self._match = self._NONCE.match(self._raw)
            self._family = 'SIGNALING'
            self._type = 'NONCE'
            self._human_readable_log = f"Nonce challenge received: {self._match.group(1)}."
        elif self._SHA.match(self._raw):
            self._match = self._SHA.match(self._raw)
            self._family = 'SIGNALING'
            self._type = 'SHA'
            self._human_readable_log = f"SHA{'-1' if self._match.group(1) else '-256'} challenge received."
        elif self._COMMAND_SESSION.match(self._raw):
            self._match = self._COMMAND_SESSION.match(self._raw)
            self._family = 'SIGNALING'
            self._type = 'COMMAND_SESSION'
            self._human_readable_log = "Command session requested."
        elif self._EVENT_SESSION.match(self._raw):
            self._match = self._EVENT_SESSION.match(self._raw)
            self._family = 'SIGNALING'
            self._type = 'EVENT_SESSION'
            self._human_readable_log = "Event session requested."

    @property
    def nonce(self):
        """ Return the authentication nonce IF the message is a nonce message """
        if self.is_nonce:
            return self._match.group(1)
        else:
            return None

    @property
    def sha_version(self):
        """ Return the authentication SHA version IF the message is a SHA challenge message """
        if self.is_SHA:
            return self._match.group(1)
        else:
            return None

    def is_ACK(self) -> bool:
        return self._type == 'ACK'

    def is_NACK(self) -> bool:
        return self._type == 'NACK'

    def is_nonce(self) -> bool:
        return self._type == 'NONCE'

    def is_SHA(self) -> bool:
        return self._type == 'SHA'