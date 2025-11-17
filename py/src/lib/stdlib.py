"""
Standard Library Functions
"""

import random
import time
import sys

class Stdlib:
    @staticmethod
    def malloc(size):
        """Allocate memory"""
        print(f"[STDLIB] malloc({size})")
        # In real implementation, this would interface with memory manager
        return [0] * size
    
    @staticmethod
    def free(ptr):
        """Free memory"""
        print(f"[STDLIB] free({id(ptr)})")
        # In real implementation, this would return memory to memory manager
    
    @staticmethod
    def calloc(nmemb, size):
        """Allocate and zero memory"""
        total_size = nmemb * size
        print(f"[STDLIB] calloc({nmemb}, {size}) = {total_size}")
        return [0] * total_size
    
    @staticmethod
    def realloc(ptr, size):
        """Reallocate memory"""
        print(f"[STDLIB] realloc({id(ptr)}, {size})")
        # Simplified implementation
        return [0] * size
    
    @staticmethod
    def atoi(s):
        """String to integer"""
        try:
            return int(s)
        except ValueError:
            return 0
    
    @staticmethod
    def atol(s):
        """String to long"""
        try:
            return int(s)
        except ValueError:
            return 0
    
    @staticmethod
    def rand():
        """Random number"""
        return random.randint(0, 32767)
    
    @staticmethod
    def srand(seed):
        """Seed random number generator"""
        random.seed(seed)
    
    @staticmethod
    def exit(status):
        """Exit program"""
        print(f"[STDLIB] exit({status})")
        sys.exit(status)
    
    @staticmethod
    def system(command):
        """Execute system command"""
        print(f"[STDLIB] system('{command}')")
        # In real OS, this would create a new process
        return 0
    
    @staticmethod
    def getenv(name):
        """Get environment variable"""
        # Simulated environment
        env_vars = {
            'PATH': '/bin:/usr/bin',
            'HOME': '/home/user',
            'USER': 'user',
            'SHELL': '/bin/sh'
        }
        return env_vars.get(name, "")
    
    @staticmethod
    def abs(x):
        """Absolute value"""
        return abs(x)
    
    @staticmethod
    def labs(x):
        """Long absolute value"""
        return abs(x)