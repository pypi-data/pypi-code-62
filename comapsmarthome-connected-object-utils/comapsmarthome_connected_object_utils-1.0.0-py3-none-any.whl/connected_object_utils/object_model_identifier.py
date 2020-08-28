from enum import Enum


class ObjectModel(Enum):
    GATEWAY = 1
    THERMOSTAT = 2
    PILOT_WIRE_HEATING_MODULE = 3
    DRY_CONTACT_HEATING_MODULE = 4
    RADIATOR_VALVE = 5


class UnrecognizedModelException(Exception):
    def __init__(self, serial_number):
        self.serial_number = serial_number


def get_model(serial_number):
    if not serial_number:
        raise UnrecognizedModelException(None)

    start = serial_number[:4]
    if start == '1c87':
        return ObjectModel.GATEWAY
    start = serial_number[:2]
    if start == 'aa':
        return ObjectModel.THERMOSTAT
    if start == 'bb':
        return ObjectModel.PILOT_WIRE_HEATING_MODULE
    if start == 'ba':
        return ObjectModel.DRY_CONTACT_HEATING_MODULE
    if start == 'ca':
        return ObjectModel.RADIATOR_VALVE
    raise UnrecognizedModelException(serial_number)


def is_gateway(serial_number):
    try:
        return get_model(serial_number) == ObjectModel.GATEWAY
    except UnrecognizedModelException:
        return False


def is_thermostat(serial_number):
    try:
        return get_model(serial_number) == ObjectModel.THERMOSTAT
    except UnrecognizedModelException:
        return False


def is_pilot_wire_heating_module(serial_number):
    try:
        return get_model(serial_number) == ObjectModel.PILOT_WIRE_HEATING_MODULE
    except UnrecognizedModelException:
        return False


def is_dry_contact_heating_module(serial_number):
    try:
        return get_model(serial_number) == ObjectModel.DRY_CONTACT_HEATING_MODULE
    except UnrecognizedModelException:
        return False


def is_heating_module(serial_number):
    return is_pilot_wire_heating_module(serial_number) or is_dry_contact_heating_module(serial_number)


def is_radiator_valve(serial_number):
    try:
        return get_model(serial_number) == ObjectModel.RADIATOR_VALVE
    except UnrecognizedModelException:
        return False
