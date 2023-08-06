class RangeError(Exception):
    def __init__(self):
            pass



class num_generator:
    
    def __init__(self,name,query=1,lower_bound = 0,upper_bound = 0):
        self.lower_bound = lower_bound
        self.upper_bound= upper_bound
        self.n = 0
        if query==1:self.infinite_series()
        elif query==2:self.missing_data()
        else:self.finite_series()

    def missing_data(self):
        try:
            flag = int(input(str(self.name)+" :  Enter 1 for finite and any other key for infinite series  "))
            if flag == 1:
                self.finite_series()
            else:
                self.infinite_series()
        except ValueError as e:
            print("Value Error Occured hence considering infinte series as default")
            self.infinite_series()

            
    def display(self,name,series,n):
        print("##"*50)
        print("-----"+str(name)+" -----")
        print("n value is : ",n)
        print(name ,":","\n",series)
        if self.query==1 or self.query==3:
            self.Mean()
            self.Median()
        else:
            flag = int(input("Do you want to calculate mean[1] or median[2]? if not type [0]?  "))
            if flag==1:self.Mean()
            else:self.Median()
        print("##"*50)
    def get_range(self):
        if self.query == 1:self.upperbound=5;self.lower_bound=10;return
        if self.upper_bound ==0:
            try:
                self.lower_bound = int(input("please enter the lower bound:  "))
                self.upper_bound = int(input("please enter the upper bound:  "))
                if self.upper_bound < self.lower_bound : 
                    raise RangeError()
            except RangeError as e:
                print(" you have typed incorrect values lower  bound should be less tahn upper bound")  
                self.lower_bound = int(input("please enter the lower bound:  "))
                self.upper_bound = int(input("please enter the upper bound:  "))
              
        else:
            return
    def get_median(series):
        n = len(series)
        if n%2!=0:
            index = int(n/2)
            return series[index]
        elif n%2==0:
            median = int(n/2)
            n1 = series[median]
            n2 = series[median-1]
            median = (n1+n2)/2
            return median

    def get_mean(series):
        n = len(series)
        if n!=0:
            return round(sum(series)/n,2)
        else:
            print("The series is empty")