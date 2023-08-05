import numpy as np

class agg:
    
    # Initialize the class correctly
    def __init__(self, ls =[]):
        self.ls = ls
    
    # Return the max value in the list
    def return_max(self):
        return max(self.ls)
    
    # Return the min value in the list
    def return_min(self):
        return min(self.ls)
    
    # Return the max value squared
    def return_max_squared(self):
        return (max(self.ls))**2
    
    # Return length of the list
    def return_length(self):
        return len(self.ls)
    
    # Return the sum of all positive numbers only 
    def return_positive_sum(self):
        sum = 0
        for i in range(len(self.ls)):
            if self.ls[i] > 0:
                sum = sum + self.ls[i]
        return sum
    
    # Return the count of all negative numbers
    def return_negative_count(self):
        cnt = 0
        for i in range(len(self.ls)):
            if self.ls[i] < 0:
                cnt = cnt + 1
        return cnt
    
    # Average
    def avg(self):
        sum = 0
        for i in range(len(self.ls)):
            sum = sum + self.ls[i]
        return sum/len(self.ls)
    
    # Median
    def median(self):
        return np.median(self.ls)
        