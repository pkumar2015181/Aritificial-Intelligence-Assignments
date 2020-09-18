"""
IMPORT REQUIRED LIBRARIES
"""

def hill_climbing(problem):
    # To return comma sepated tuple of positions on queens
    #Example: for 4 queens your algorithm returns (2,0,1,3)
    """
    YOUR CODE HERE
    """
    j = 5
    while j > 0:
        j = j-1
        start = problem.initial()
        val_start = problem.value(start)
        print("Iteration = ",5-j)
        print("Initial position = ", start, " with value = ", val_start)
        
        goal_found = False
        max_state = start
        max_val = val_start
        flag = 1
        while flag:
            flag = 0
    #        print("\nState = ", max_state)
    #        print("State val = ", max_val)
            ch = problem.children(max_state)
    #        print("\nchildren = ", ch)
            for i in ch:
                val_i = problem.value(i)
    #            print("state = ", i, ", val = ", val_i)
                if val_i > max_val:
                    max_val = val_i
                    max_state = i
                    flag = 1
                    if problem.goal_test(max_state) == True:
                        goal_found = True
                        
        
        print("Max. state = ", max_state, " with value = ", max_val)
        if goal_found == True:
            print("GOAL IS FOUND")
        else:
            print("GOAL IS NOT FOUND")
        if j > 1:
            print("\n")
#    print("children = ",ch)
#    val = problem.value(start)
#    print("Value = ", val)
#    goal = problem.goal_test(start)
#    print("goal = ", goal)
#    rc = problem.random_child(start)
#    print("RC = ", rc)
    
    return max_state

