'''
    Import libraries according to necessity
'''

import timeit

# DEPTH FIRST SEARCH ALGORITH USING STACK

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
    
    
    queue = []
    queue.append(start)
    visited = []
    parent = {start : None}
    path = []
    complete = 0
    max_memory = 0
    
    #print("Queue = ", queue)
    
    while queue and complete == 0:
        # Fetch starting node of queue
        current_node = queue.pop()
        
        
        #print("\n\n\n");
        
        #print("CURRENT NODE = ", current_node)
        
        #print("Queue = ", queue)
        
        
        #find all valid path
        valid_path = maze_game.legal_directions(*current_node)
        #print("Valid path before = ", valid_path)
        
        valid_path = list(set(valid_path).difference(visited))
        #print("Valid path after = ", valid_path)
        
        for next_node in valid_path:
            #print("Run loop for = ", next_node)
            
            if next_node not in visited:
                #print("Not visited\n")
                
                queue.append(next_node)
                #print("Queue = ", queue)
                if len(queue) > max_memory:
                    max_memory = len(queue)
                
                parent.update( {next_node : current_node} )
                
                #print("Parent = ", parent)
                
                if next_node == goal:
                    complete = 1
                    #print("\n\n==== GOAL FOUND ==== ")
                
                
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
    
    print("\n\n--------------------------------  OUTPUT START -----------------------\n")
    
    print("\nSTART ==> ", start)
    print("\nGOAL ==> ", goal)
    print("\nPATH ==> ", path)
    print("\nPATH Length = ", len(path)-1)
    print("\nTotal cost = ", 2*(len(path)-1))
    print("\nTotal Expanded nodes = ", len(visited))
    print('\nRunning Time: ', running_time, " microsecs")
    print("\nIf each node is taking 1KB memory then maximum memory used by stack is", max_memory, "KB")
    
    print("\n--------------------------------  OUTPUT END -----------------------\n\n")
    
    
    return len(path),path
        































# -*- coding: utf-8 -*-

