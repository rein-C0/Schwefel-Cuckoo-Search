import math
import numpy as np
import random

def schwefel(position):
    sol = 418.982887
    fitness = 0
    for i in range(len(position)):
            fitness -= position[i]*math.sin(math.sqrt(math.fabs(position[i])))
    return float(fitness) + sol*len(position)

def levy_flight(Lambda,lenpos):
    #generate step from levy distribution
    sigma1 = np.power((math.gamma(1 + Lambda) * np.sin((np.pi * Lambda) / 2)) \
                      / (math.gamma((1 + Lambda) / 2) * np.power(2, (Lambda - 1) / 2)), 1 / Lambda)
    sigma2 = 1
    u = np.random.normal(0, sigma1, size=lenpos)
    v = np.random.normal(0, sigma2, size=lenpos)
    step = u / np.power(np.fabs(v), 1 / Lambda)
    return step

class Nest:
    def __init__(self,alpha,pa,max,min,dim):
        # initialize generation 0
        self.__alpha = alpha
        self.__pa = pa
        self.__max_domain = max
        self.__min_domain = min
        self.__position = np.random.rand(dim) * (max - min) + min
        self.__fitness = schwefel(self.__position) # iteration = 0
    
    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def get_fitness(self):
        return self.__fitness

    def set_fitness(self):
        self.__fitness = schwefel(self.__position)
            
    def abandonHeaviside(self,NestA,NestB):
        cek=np.random.rand(len(self.__position)) < self.__pa
        step_size = self.__alpha * np.random.rand(len(self.__position)) * (NestA - NestB)
        step_size = cek * step_size
        self.__position = self.__position + step_size
        for i in range(len(self.__position)):
            if self.__position[i] > self.__max_domain:
                self.__position[i] = self.__max_domain
            if self.__position[i] < self.__min_domain:
                self.__position[i] = self.__min_domain

    def get_cuckoo(self,BestNest):
        step_size=self.__alpha * levy_flight(1.5,len(self.__position))
        # Update position
        self.__position = self.__position + ((self.__position - BestNest) * step_size)
        # Simple Boundary Rule
        for i in range(len(self.__position)):
            if self.__position[i] > self.__max_domain:
                self.__position[i] = self.__max_domain
            if self.__position[i] < self.__min_domain:
                self.__position[i] = self.__min_domain