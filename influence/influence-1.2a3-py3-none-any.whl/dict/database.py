class Database:
    def __init__(self, initial_capacity=1000):
        self.__l = [None for i in range(initial_capacity)]
        self.capacity = initial_capacity
        self.size = len(self.__l)
        self.__index = 0
    def add(self, **kwargs):
        tstart = time.time()
        if self.__index < self.size:
            self.__l[self.__index] = kwargs
            self.__index += 1
        else:
            #allocation
            a = [i for i in self.__l]
            b = [None for i in range(self.capacity)]
            a = a + b
            self.capacity *= 2
            self.size = len(a)
            self.__l = a
            self.__l[self.__index] = kwargs
            self.__index += 1
    def items(self):
        for i in self.__l:
            yield i
    def __len__(self):
        return len(self.__l)
    def __getitem__(self, key):
        return self.__l[key]
    def __setitem__(self, key, item):
        self.__l[key] = item
    def __contains__(self, item):
        for i in Database.items(self):
            if i == item:
                return True
        return False

