import time 
class Cache:

    def __init__(self):
        self.store = {}
        self.default_ttl = 30

    def get(self, key):

        if key in self.store:

            entry = self.store[key]

            if time.time() > entry['expiry']:
                del self.store[key]

                return None
            
            return entry['value']
        else:
            return None
        
        
    def save(self, key, value, ttl=None):

        if ttl is None:
            ttl = self.default_ttl

        expiry = time.time() + ttl

        self.store[key] = {
            'value': value,
            'expiry': expiry
        }

    def clear(self):
        self.store = {}
        