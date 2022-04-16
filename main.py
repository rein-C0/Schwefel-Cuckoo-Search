import numpy as np
import random
import CuckooSearch

if __name__ == '__main__':
    dimension=5
    max_domain=500
    min_domain=-500
    alpha=0.1
    generation=500
    population=50
    Pa=0.25
    Cuckoo=[CuckooSearch.Nest(alpha,Pa,max_domain,min_domain,dimension) for i in range(population)]
    Cuckoo = sorted(Cuckoo, key=lambda ID: ID.get_fitness())
    BestPosition = np.copy(Cuckoo[0].get_position())
    BestFitness = CuckooSearch.schwefel(BestPosition)
    for n in range(generation):
        #Update Egg Position using Levy Flight
        for i in range(len(Cuckoo)):
            Cuckoo[i].get_cuckoo(BestPosition)
            Cuckoo[i].set_fitness()
        Cuckoo = sorted(Cuckoo, key=lambda ID: ID.get_fitness())
        #Abandon Cuckoo
        for i in range(len(Cuckoo)):
            randA=random.randint(0,population)
            randB=random.randint(0,population)
            while randA==randB:
                randB=random.randint(0,population)
            Cuckoo[i].abandonHeaviside(randA,randB)
            Cuckoo[i].set_fitness()
        Cuckoo = sorted(Cuckoo, key=lambda ID: ID.get_fitness())
        if Cuckoo[0].get_fitness() < BestFitness:
            BestPosition = np.copy(Cuckoo[0].get_position())
            BestFitness = CuckooSearch.schwefel(BestPosition)
        print("Generation ",n+1)
        print("Nest :",BestPosition)
        print("Fitness :",BestFitness)