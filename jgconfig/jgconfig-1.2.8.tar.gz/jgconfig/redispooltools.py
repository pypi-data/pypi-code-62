import redis


class RedisPoolTools:
    selfpool=None

    @staticmethod
    def initPools(host='127.0.0.1',port=6379,password=None):
        RedisPoolTools.selfpool = redis.ConnectionPool(host=host, port=port,password=password, decode_responses=True)

    def __init__(self):
        self.rd = redis.Redis(connection_pool=RedisPoolTools.selfpool)
        pass

    def StringSet(self,key,val,ex=None):
        self.rd.set(key, val,ex=ex)
    
    def StringGet(self,key):
        return self.rd.get(key)

    def HasSet(self,haskey,key,val,ex=None):
        self.rd.hset(haskey,key,val,ex)

    def HasGet(self,haskey,key):
        return self.rd.hget(haskey,key)

    # def timeout(self):
    #     self.rd.t

    def HasAll(self,name):
        return self.rd.hgetall(name)