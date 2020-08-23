

def no_args_slot():
    pass


def correct_names_and_args_slot(arg_1: int, arg_2: int):
    pass


def slot_1(arg_1):
    pass


def slot_2(arg_1: int = 1):
    pass


def slot_3(*args):
    pass


def slot_4(**kwargs):
    pass


def slot_5(*args, **kwargs):
    pass


def slot_6(*, arg_1):
    pass


def slot_7(*, arg_1: int = 1):
    pass


def slot_8(*, arg_1: int = 1, arg_2: int = 2):
    pass


def slot_9(name_1: int, name_2: int):
    pass


def wrong_signature_slots():
    return slot_1, slot_2, slot_3, slot_4, slot_5, slot_6, slot_7, slot_8, slot_9
