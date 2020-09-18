"""
IMPORT REQUIRED LIBRARIES
"""
import math
import numpy as np



# You've got to tune these parameters carefully before you can make it work
def exp_schedule(k=50, lam=0.5, limit=15):
    # Parameters must be tuned according to the size of the input
	# k decides the time span of random walk
	# lambda decides how steep does the probability converges to zero
	# limit decides the number of iterations
    #return lambda t:
    """
    YOUR CODE HERE
    """ 

def simulated_annealing(problem, schedule=exp_schedule()):
    # To return comma sepated tuple of positions on queens
    #Example: for 4 queens your algorithm returns (2,0,1,3)
    """
    YOUR CODE HERE
    """
    goal_found = False
    no_down_moves = 0
    max_state = problem.initial()
#    max_state = (4, 4, 1, 1, 7, 0, 1, 7)
    max_val = problem.value(max_state)
    print("\nInitial position = ", max_state, " with value = ", max_val)
    if problem.goal_test(max_state) == True:
        goal_found = True
        print("GOAL is Found at state: ", max_state)
        return max_state
    itr = 4**(problem.N+2)
#    itr = 200000
    print("Scheduled Temperature = ", itr)
    while itr>0 and goal_found == False:        
        temp = itr
        next_child = problem.random_child(max_state)
        next_val = problem.value(next_child)
        if problem.goal_test(next_child) == True:
            goal_found = True
            max_state = next_child
            max_val = next_val
            break
        if (next_val - max_val) > 0:
            max_state = next_child
            max_val = next_val
            if itr == 1:
                itr = 2
        else:
            #Generate a random probability between 0 and 1  
            random_prob = np.random.random()
            curr_prob = math.exp((next_val - max_val)/temp)
            if random_prob < curr_prob:
                max_state = next_child
                max_val = next_val
                no_down_moves += 1
            
        itr = itr-1
    print("Max state = ", max_state, " with value = ", max_val)
    if goal_found == True:
        print("GOAL is Found")
    else:
        print("Goal is not found")
    return max_state
