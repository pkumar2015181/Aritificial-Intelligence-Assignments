"""
IMPORT REQUIRED LIBRARIES
"""
from random import randint
#from itertools import combinations
import operator
import numpy as np

def reproduce(x,y):
#    print("Reproduce: x = ", x, " and y = ", y)
    size = len(x)
#    print("size = ", size)
    random_point = randint(0, size-1)
#    print("RP = ", random_point)
    new = []
    for i in range(size):
        if i < random_point:
            new.append(x[i])
        else:
            new.append(y[i])
#    print("NEW = ", tuple(new))
    return tuple(new) 

def GA(problem):
    # To return comma sepated tuple of positions on queens
    #Example: for 4 queens your algorithm returns (2,0,1,3)
    """
    YOUR CODE HERE
    """
    
    N = int(input("Enter population size: "))
    crossover_prob = float(input("Enter crossover probability: "))
    mutation_prob = float(input("Enter mutation probability: "))
    population = []
    max_state = None
    max_value = float('-Inf')
    # GENERATE UNIQUE POPULATION
    while len(population) < N:
        state = problem.initial()
        if state not in population:
            population.append(state)
            if problem.goal_test(state) == True:
                goal_found = True
                max_state = state
                max_value = problem.value(state)
    
#    print("Population = ", population)
    
    goal_found = False
    #time = 5**(problem.N - 1)
    time = 2**problem.N
    
    while goal_found == False and time > 0:
        #print("\n\nTime = ", time)
        time = time-1
        population_fitness = {}
        for state in population:
            population_fitness[state] = problem.value(state)
        #print("Befor sort: ",population_fitness)
        
        sorted_population = sorted(population_fitness.items(), key=operator.itemgetter(1), reverse=True)
        #print("After sort: ",sorted_population)
        
        sorted_states = []
        for i in sorted_population:
            sorted_states.append(i[0])
        #print("SS = ", sorted_states)
        
        if max_state == None:
            max_state = sorted_states[0]
            max_value = problem.value(max_state)
            if problem.goal_test(max_state) == True:
                goal_found = True
        else:
            if problem.value(max_state) < problem.value(sorted_states[0]):
                max_state = sorted_states[0]
                max_value = problem.value(max_state)
                if problem.goal_test(max_state) == True:
                    goal_found = True
        
        co_size = round(crossover_prob*N)
        if co_size > len(sorted_states):
            co_size = len(sorted_states)
        #print(co_size)
        co_population = []
        for j in range(co_size):
            co_population.append(sorted_states[j])
        
        #print("co population: ",co_population)
        
        new_population = []
        for _ in range(N):
            x = randint(0, co_size-1)
            y = randint(0, co_size-1)
            new = reproduce(co_population[x], co_population[y])
            random_prob = np.random.random()
            if random_prob < mutation_prob:
                new = problem.random_child(new)
            if problem.goal_test(new) == True:
                goal_found = True
                max_state = new
                max_value = problem.value(new)
                break
            new_population.append(new)
            if max_state == None:
                max_state = new
                max_value = problem.value(max_state)
            else:
                if problem.value(max_state) < problem.value(new):
                    max_state = new
                    max_value = problem.value(max_state)
        
        #print("NP = ", new_population)
        population = new_population
        #print("\n max state = ", max_state, " with value = ", max_value)
    
    if goal_found == True:
        print("GOAL IS FOUND")
    else:
        print("GOAL IS NOT FOUND")
        
    return max_state
