import tkinter as tk
from collections import OrderedDict

class LRUalghorithm:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def access(self, item):
        """Simulates accessing an item in the cache."""
        if item in self.cache:
            # Move the accessed item to the end (most recently used)
            self.cache.move_to_end(item)
            print(f"Cache hit: {item}")
        else:
            # Add the item to the cache
            if len(self.cache) >= self.capacity:
                # Evict the least recently used item
                evicted = self.cache.popitem(last=False)
                print(f"Cache miss: {item} | Evicted: {evicted[0]}")
            else:
                print(f"Cache miss: {item}")
            self.cache[item] = True 

    def display_cache(self):
        """Displays the current state of the cache."""
        print("Current Cache:", list(self.cache.keys()))

class FIFOalgorithm:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []  # Use a list to track the cache entries

    def access(self, item):
        """Simulates accessing an item in the cache."""
        if item in self.cache:
            # Cache hit
            print(f"Cache hit: {item}")
        else:
            # Cache miss
            if len(self.cache) >= self.capacity:
                # Evict the first item added to the cache
                evicted = self.cache.pop(0)
                print(f"Cache miss: {item} | Evicted: {evicted}")
            else:
                print(f"Cache miss: {item}")
            # Add the new item to the cache
            self.cache.append(item)

    def display_cache(self):
        """Displays the current state of the cache."""
        print("Current Cache:", self.cache)

import random

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

    def display_cache(self):
        print("Current Cache:", list(self.cache.keys()))
