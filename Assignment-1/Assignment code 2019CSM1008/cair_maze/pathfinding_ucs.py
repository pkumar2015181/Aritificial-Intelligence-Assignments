'''
    Import libraries according to necessity
'''

import timeit

# UNIFORM COST SEARCH ALGORITH USING PRIORITY QUEUE

def search(maze_game, start, goal):
    """
    ***************************************
    YOUR CODE HERE
    **************************************
    search-algorithm
     :param maze_game: the GameMaze instance
    :param start: tuple (x,y) of start position
    :param goal: tuple (x,y) of the goal position
    :A sequential loop to take 1 step then again check for environment legal actions 
     and then take 2 step or backtrack if no options possible
    :return: list containing the path [number of coordinates, sequence of coordinates from source to destination, comma separated] if possible

    """
    
    start_time = timeit.default_timer()
    
    #print(maze_game)
    #print("\n\nSTART ==> ", start)
    #print("\n\nGOAL ==> ", goal)
    
    queue = {start : 0}
    visited = []
    parent = {start : None}
    path = []
    complete = 0
    final_cost = 0
    max_memory = 0
    
    #print("Queue = ", queue)
    
    while queue and complete == 0:
        # Fetch starting node of queue
        sorted_d = sorted(queue.items(), key=lambda item: item[1])
        
        #print("SORTED dict = ", sorted_d)
        
        current_node, current_node_cost = sorted_d.pop(0)
        
        del queue[current_node]
    
        #print("\n");
        
        #print("CURRENT NODE = ", current_node, " Cost = ", current_node_cost)
        
        #print("Queue = ", queue)
        
        if current_node == goal:
            complete = 1
            #print("\n\n==== GOAL FOUND ==== ")
            final_cost = current_node_cost
            break
        
        
        #find all valid path
        valid_path = maze_game.legal_directions(*current_node)
        #print("Valid path before = ", valid_path)
        
        valid_path = list(set(valid_path).difference(visited))
        #print("Valid path after = ", valid_path)
        
        for next_node in valid_path:
            #print("Run loop for = ", next_node)
            
            if next_node not in visited:
                #print("Not visited\n")
                
                step_cost = cost_of_step(current_node, next_node)
                
                queue[next_node] = current_node_cost + step_cost
                #print("Queue = ", queue)
                
                if len(queue) > max_memory:
                    max_memory = len(queue)
                
                parent.update( {next_node : current_node} )
                
                #print("Parent = ", parent)
                
                
            #else:
                #print("Already visited\n")
        
        visited.append(current_node)
        #print("\n\n")
        #print("Visited = ", visited)
        
    
    #print(visited)
    
    #print( len(visited) )
    
    pre = goal
    while pre is not None:
        path.insert(0, pre)
        pre = parent[pre]
    
    stop_time = timeit.default_timer()
    running_time = (stop_time - start_time)*1000000
    
    print("\n\n--------------------------------  OUTPUT -----------------------\n")
    
    print("\nSTART ==> ", start)
    print("\nGOAL ==> ", goal)
    print("\nPATH ==> ", path)
    print("\nPATH length = ", len(path)-1)
    print("\nTotal cost = ", final_cost)
    print("\nTotal Expanded nodes = ", len(visited))
    print('\nRunning Time: ', running_time, " microsecs")
    print("\nIf each node is taking 1KB memory then maximum memory used by priority queue is", max_memory, "KB")
    
    print("\n--------------------------------  OUTPUT -----------------------\n\n")
    
    return len(path),path
        

def cost_of_step(tuple1,tuple2):
    x1, y1 = tuple1
    x2, y2 = tuple2
    if x1 == x2:
        return 1
    else:
        return 2
    































