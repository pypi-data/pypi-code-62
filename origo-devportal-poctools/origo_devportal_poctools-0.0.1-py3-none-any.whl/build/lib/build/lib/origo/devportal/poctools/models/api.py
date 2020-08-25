class API:
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, publisher):
        self._publisher = publisher

    def __init__(self, title, publisher):
        self._title = title
        self._publisher = publisher

    def serialize(self):
        return {
            'title': self._title,
            'publisher': self._publisher,
        }
