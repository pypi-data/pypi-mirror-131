import numpy as np

class Normal():
    def __init__(self):
        self.lst = np.array([])
        self.mean = 0
        self.var = 0
        
    def generate(self, mu, sigma, n):
        self.lst = np.random.normal(mu, sigma, n)
        print("Generated number: ", self.lst)
        
    def get_mean(self):
        self.mean = np.mean(self.lst)
        return self.mean
        
    def get_var(self):
        self.var = np.var(self.lst)
        return self.var