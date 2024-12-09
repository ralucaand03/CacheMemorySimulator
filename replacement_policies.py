import random
from collections import OrderedDict

class LRUalghorithm:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def access(self, item):
        """Simulates accessing an item in the cache."""
        if item in self.cache:
            self.cache.move_to_end(item)
            print(f"Cache hit: {item}")
            box_number = len(self.cache) - 1
        else:
            if len(self.cache) >= self.capacity:
                evicted = self.cache.popitem(last=False)
                print(f"Cache miss: {item} | Evicted: {evicted[0]}")
            else:
                print(f"Cache miss: {item}")
            self.cache[item] = True 
    
    def get_cache(self):
        return self.cache 

    def display_cache(self):
        print("Current Cache:", list(self.cache.keys()))

#---------------------------------------------------------------------------------------------------------------------

class FIFOalgorithm:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []  

    def access(self, item):
        """Simulates accessing an item in the cache."""
        if item in self.cache:
            print(f"Cache hit: {item}")
        else:
            # Cache miss
            if len(self.cache) >= self.capacity:
                evicted = self.cache.pop(0)
                print(f"Cache miss: {item} | Evicted: {evicted}")
            else:
                print(f"Cache miss: {item}")
            self.cache.append(item)
    def get_cache(self):
        return self.cache 

    def display_cache(self):
        """Displays the current state of the cache."""
        print("Current Cache:", self.cache)

#---------------------------------------------------------------------------------------------------------------------

class RANDOMalgorithm:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}

    def access(self, item):
        if item in self.cache:
            print(f"Cache hit: {item}")
        else:
            if len(self.cache) >= self.capacity:
                evicted_item = random.choice(list(self.cache.keys())) 
                self.cache.pop(evicted_item)
                print(f"Cache miss: {item} | Evicted: {evicted_item}")
            else:
                print(f"Cache miss: {item}")
            self.cache[item] = True
    def get_cache(self):
        return self.cache 

    def display_cache(self):
        print("Current Cache:", list(self.cache.keys()))