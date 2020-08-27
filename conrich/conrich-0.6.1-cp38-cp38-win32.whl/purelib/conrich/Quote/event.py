

class Event():
    def __init__(self):
        self.listeners = []

    def __iadd__(self, listener):
        """Shortcut for using += to add a listener."""
        self.listeners.append(listener)
        return self

    def notify(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)


my_event = Event()
def print_person_info(name, age, sex):
    print("Hello! I am {}, I'm a {}-year-old {}".format(name, age, sex))

my_event += print_person_info
my_event.notify('Markus', 23, 'male')