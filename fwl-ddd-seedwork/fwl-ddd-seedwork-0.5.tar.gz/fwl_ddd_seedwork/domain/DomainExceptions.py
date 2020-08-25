class DomainError(Exception):
    def __init__(self, notifications, message):
        super().__init__(message)
        self.notifications = notifications


class ValueObjectError(Exception):
    def __init__(self, vo_name, message):
        self.message: dict = {vo_name: message}
