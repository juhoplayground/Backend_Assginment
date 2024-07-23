from app.config.redis_config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB
import redis

class RedisClient:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)

    def get_value(self, key):
        value = self.redis_client.get(key)
        if value:
            value = value.decode('utf-8')
        return value
    
    def set_value(self, key, value, timeout):
        self.redis_client.set(key, value, timeout)
        
    def set_statistics(self, key):
        self.redis_client.incr(key)