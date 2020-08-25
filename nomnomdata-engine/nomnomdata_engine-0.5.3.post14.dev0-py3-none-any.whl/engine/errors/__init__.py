class ValidationError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = []

    def add_key(self, key):
        self.keys.append(key)

    def __str__(self):
        return ".".join(reversed(self.keys)) + ": " + super().__str__()


class MissingParameters(ValidationError):
    def __str__(self):
        return ".".join(reversed(self.keys)) + " is missing"
