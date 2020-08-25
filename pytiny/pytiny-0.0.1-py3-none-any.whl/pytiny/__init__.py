import json


class PyTiny(object):
    """PyTiny is an in-memory key–value database written in Python."""

    def __init__(self):
        self.db = {}

    def bring(self, location):
        """Import a file. This will be delete all data stored before, 
        and will be restore the new data from the file."""
        name = f"{location}.db"
        with open(name, "r") as f:
            self.db = json.load(f)

    def export(self, location):
        """Export the data to a .db file"""
        name = f"{location}.db"
        with open(name, "w") as f:
            json.dump(self.db, f)

    def reset(self):
        """Reset the data. All data stored will be delete."""
        self.db = {}
        return True

    def set(self, key, value):
        """Set a key and value"""
        try:
            self.db[str(key)] = value
        except Exception as e:
            error = f"Error. An error occurred while saving the data: {e}"
            print(error)
            return False

    def get(self, key):
        """Get a value from a key"""
        try:
            return self.db[key]
        except KeyError:
            error = f"Error. No value could be found for '{key}'"
            print(error)
            return False

    def delete(self, key):
        """Delete a value from a key"""
        if key in self.db:
            del self.db[key]
        else:
            error = f"Error. No value could be found for '{key}'"
            print(error)
            return False
