from ..NumGen import num_generator
class Error(Exception):
    def __init_(self):
        print("please enter values less than 100")
        self.n = int(input("enter the number of values :"))
    def __str__(self):
        return(repr(self.n))

    

    
class Pentagon(num_generator):
    def __init__(self,query=1,lower_bound = 0,upper_bound = 0):
        self.query=query
        self.name = "Pentagon Series"
        self.series = []
        super().__init__(self.name,query,lower_bound,upper_bound)

    def finite_series(self):
        self.get_range()
        self.list_n = list(range(self.lower_bound, self.upper_bound + 1))
        self.series = [ int(3*n*(n-1)/2 + n) for n in self.list_n]
        self.n = len(self.list_n)
        self.display(self.name, self.series, len(self.list_n))

    def infinite_series(self):
        try:
            
            if self.query==1:raise ValueError
            self.n = int(input("enter the number of values :"))
            if self.n>100:
                raise Error
        except ValueError as e:
            self.n=5
        except Error:
            print("Exception raised:")
        finally:
            print('you have given value as 5')
        self.series = [int(3*i*(i-1)/2 + i) for i in range(1, self.n + 1)]
        self.display(self.name, self.series, self.n)

    def Mean(self):
        if len(self.series) != 0:
            self.avg = num_generator.get_mean(self.series)
            print("mean of series is :", self.avg)


    def Median(self):
        if len(self.series) != 0:
            self.median = num_generator.get_median(self.series)
            print("median of series:", self.median)