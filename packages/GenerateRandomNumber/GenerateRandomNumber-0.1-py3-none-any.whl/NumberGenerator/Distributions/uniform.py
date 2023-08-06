import numpy as np

class Uniform():
    def __init__(self):
        self.lst = np.array([])
        self.mean = 0
        self.var = 0
        
    def generate(self, lower, upper, n):
        self.lst = np.random.uniform(lower, upper, n)
        print("Generated number: ", self.lst)
        
    def get_mean(self):
        self.mean = np.mean(self.lst)
        return self.mean
        
    def get_var(self):
        self.var = np.var(self.lst)
        return self.var