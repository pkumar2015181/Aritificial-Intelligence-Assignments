'''
    Import libraries according to necessity
'''

import timeit

# A* ALGORITH USING PRIORITY QUEUE
class path_finding():
    def search(start, goal):
        
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
        
    #    print("\n\nSTART ==> ", start)
    #    print("\n\nGOAL ==> ", goal)
        
        queue = {start : 0}
        visited = []
        parent = {start : None}
        list_actions = {start : None}
        path = []
        complete = 0
        final_cost = 0
        max_memory = 0
        
#        print("Queue = ", queue)
        
        while queue and complete == 0:
            # Fetch starting node of queue
            sorted_d = sorted(queue.items(), key=lambda item: item[1])
            
#            print("SORTED dict = ", sorted_d)
            
            current_node, current_node_cost = sorted_d.pop(0)
            
            del queue[current_node]
            
            visited.append(current_node)
        
#            print("\n");
            
#            print("CURRENT NODE = ", current_node, " Cost = ", current_node_cost)
            
#            print("Queue = ", queue)
            
            if current_node != start:
                current_node_cost = current_node_cost - path_finding.distance_func(current_node, goal)
            
            if current_node == goal:
                complete = 1
                final_cost = current_node_cost
#                print("\n\n==== GOAL FOUND ==== ")
                break
            
            #find all valid direction
            pos_blank = current_node.index(8)
#            print("Pos blank = ", pos_blank)
            valid_actions = path_finding.legal_direction(pos_blank)
#            print("Valid actions = ", valid_actions)
            for act in valid_actions:
#                print(act)
                next_node = path_finding.find_new_state(current_node, act)
#                print("Run loop for = ", next_node)
                if next_node not in visited:
                    #print("Not visited\n")
                    
                    estimated_cost = path_finding.distance_func(next_node, goal)
#                    print("\nEstimated cost = ", estimated_cost)
                    total_cost = estimated_cost + current_node_cost
#                    print("Total cost = ", total_cost)
                    queue[next_node] = total_cost
#                    print("Queue = ", queue)
                    
                    if len(queue) > max_memory:
                        max_memory = len(queue)
                    
                    parent.update( {next_node : current_node} )
                    list_actions.update( {next_node : act} )
                    
                    #print("Parent = ", parent)                
                    
                #else:
                    #print("Already visited\n")
            
            
            #print("\n\n")
            #print("Visited = ", visited)
            
        
    #    print(visited)
        
    #    print( len(visited) )
        
        path_actions = []    
    
        pre = goal
        while pre is not None:
            path.insert(0, pre)
            if list_actions[pre] != None:
                path_actions.insert(0, list_actions[pre] )
            pre = parent[pre]
        
        
        stop_time = timeit.default_timer()
        running_time = (stop_time - start_time)*1000000
        
        print("\n\n--------------------------------  OUTPUT -----------------------\n")
        
        print("\nSTART ==> ", start)
        print("\nGOAL ==> ", goal)
        print("\nPATH ==> ", path)
        print("\nPATH length = ", len(path)-1)
        print("\nList of Actions = ", path_actions)
        print("\nTotal Actions = ", len(path_actions))
        print("\nTotal Expanded nodes = ", len(visited))
        print('\nRunning Time: ', running_time, " microsecs")
        print("\nIf each node is taking 1KB memory then maximum memory used by priority queue is", max_memory, "KB")
        
        print("\n--------------------------------  OUTPUT -----------------------\n\n")
        
        return path_actions
    
    
    def distance_func(point1, point2):
        
        diff = tuple(abs(i-j) for i,j in zip(point1, point2))
        total = 0
        for x in diff:
            total = total + x
        return total
    
            
    def legal_direction(pos_blank):
        legal = []
        if pos_blank not in [0, 3, 6]:
            legal.append(0)     # left
        if pos_blank not in [2, 5, 8]:
            legal.append(1)     # right
        if pos_blank not in [0, 1, 2]:
            legal.append(2)     # up
        if pos_blank not in [6, 7, 8]:
            legal.append(3)     # down
        return legal
        
    def find_new_state(current_state, action):
        pos_blank = current_state.index(8)
        new_state = list(current_state)
        if action == 0:
            if pos_blank not in [0, 3, 6]:
                new_state[pos_blank], new_state[pos_blank-1] = current_state[pos_blank-1], current_state[pos_blank]
        if action == 1:
            if pos_blank not in [2, 5, 8]:
                new_state[pos_blank], new_state[pos_blank+1] = current_state[pos_blank+1], current_state[pos_blank]
        if action == 2:
            if pos_blank not in [0, 1, 2]:
                new_state[pos_blank], new_state[pos_blank-3] = current_state[pos_blank-3], current_state[pos_blank]
        if action == 3:
            if pos_blank not in [6, 7, 8]:
                new_state[pos_blank], new_state[pos_blank+3] = current_state[pos_blank+3], current_state[pos_blank]
        new_state = tuple(new_state)
        return new_state
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    












