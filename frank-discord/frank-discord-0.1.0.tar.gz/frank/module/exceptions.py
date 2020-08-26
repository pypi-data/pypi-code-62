class InvalidCommand(Exception):
    pass


class DuplicateCommand(Exception):
    pass


class MultipleDefaults(Exception):
    message = 'Multiple default commands detected'
