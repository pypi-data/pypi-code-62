class node():
    def __init__(self, value=None, nextlink=None):
        self.set_value(value)
        self.set_next(nextlink)
    
    def set_value(self, value=None):
        self.value = value
    
    def set_next(self, value):
        self.nextlink = value
    
    def get_value(self):
        return self.value
    
    def get_next(self):
        return self.nextlink
    
    def __str__(self):
        return self.value

class linked_list():
    def __init__(self, value=None):
        self.head_val = None
        self.set_head(value)
    
    def set_head(self, value=None):
        head = self.get_head()
        self.head_val = value
        try: self.head_val.set_next(head)
        except: pass
    
    def get_head(self):
        return self.head_val
