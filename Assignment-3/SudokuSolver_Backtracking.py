import numpy as np
import copy
#from random import randint
import time

class sudoku_BT:
    # READ INPUT FROM TEXT FILE
    def __init__(self):
        input_file = open('input.txt').read()
        self.board = [list(map(int, line.split(' '))) for line in input_file.split('\n')]
        self.nodes = 0
    
    # SAVE OUTPUT IN TEXT FILE
    def save_output(self, board):
        sol_file = open("solution.txt","w") 
        for i in board:
            line = ' '.join([str(elem) for elem in i])
#            print(line)
            sol_file.write(line)
            sol_file.write("\n")
    
    # CHECK EACH CONSTRAINT IN BOARD
    def constraint_satisfication(self, board):
        arr = np.array(board)
        # CHECK FOR ALL ROWS
        for row in range(9):
            row_ele = []
            for i in range(9):
                if arr[row][i] != 0:
                    row_ele.append(arr[row][i])
            # CONTAINS DUPLICATES
            if len(row_ele) != len(set(row_ele)):
#                print("Row = ", row)
                return False
        
        # CHECK FOR ALL COLUMNS
        for col in range(9):
            col_ele = []
            for i in range(9):
                if arr[i][col] != 0:
                    col_ele.append(arr[i][col])
            # CONTAINS DUPLICATES
            if len(col_ele) != len(set(col_ele)):
#                print("Col = ", col)
                return False
        
        # CHECK FOR ALL BLOCKS
        for block_row in range(3):
            for block_col in range(3):
                block_ele = []
                for row in range(3):
                    for col in range(3):
                        ele = arr[block_row*3 + row][block_col*3 + col]
                        if ele != 0:
                            block_ele.append(ele)
                # CONTAINS DUPLICATES
                if len(block_ele) != len(set(block_ele)):
#                    print("BR = ", block_row, " BC = ", block_col)
                    return False
        return True
    
    # CREATE DOMAIN FOR EACH VARIABLE
    def create_domain(self, board):
        arr = np.array(board)
        domain_dict = {}
        for row in range(9):
            for col in range(9):
                if arr[row][col] == 0:
                    domain_dict[str(row)+str(col)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
#        print(domain_dict)
        return domain_dict
    
    # REDUCE DOMAIN FOR EACH VARIABLE AND RETURNED REDUCED DOMAIN
    def reduce_domain(self, board, domain_dict):
        arr = np.array(board)
#        print(domain_dict)
        keys = list(domain_dict.keys())
        for key in keys:
            row = int(key[0])
            col = int(key[1])
            present = []
            for i in range(9):
                # FOR ROW
                if arr[row][i] != 0 and arr[row][i] not in present:
                    present.append(arr[row][i])
                
                # FOR COLUMN
                if arr[i][col] != 0 and arr[i][col] not in present:
                    present.append(arr[i][col])
            
            # FOR BLOCK
            block_row = int(row/3)
            block_col = int(col/3)
            for i in range(3):
                for j in range(3):
                    ele = arr[block_row*3 + i][block_col*3 + j]
                    if ele != 0 and ele not in present:
                        present.append(ele)
            
            for ele in present:
                domain_dict[key].remove(ele)
            
#            print("Key = ", key, " Domain = ", domain_dict[key])
        
        return domain_dict
    
    # CHECK FOR DOMAINS WHICH CONTAIN ONLY SINGLE VALUE
    def check_single_value_domain(self, domain_dict):
        single_value_list = []
        keys = list(domain_dict.keys())
        for key in keys:
            if len(domain_dict[key]) == 1:
                single_value_list.append(key)
        
        if len(single_value_list) > 0:
            return single_value_list
        else:
            return -1
    
    # CHECK FOR DOMAINS WHICH CONTAIN NO VALUE
    def check_no_value_domain(self, domain_dict):
        keys = list(domain_dict.keys())
        for key in keys:
            if len(domain_dict[key]) == 0:
                return True
        
        return False
    
    # PRINT BOARD
    def print_board(self, board):
#        print("\nCurrent Board = ")
        for i in range(9):
            if i == 0:
                print("    0 1 2 3 4 5 6 7 8")
                print("    _ _ _ _ _ _ _ _ _")
            for j in range(9):
                if j == 0:
                    print(i, "|", end = " ")
                print(board[i][j], end = " ")
            print("\n")
    
    # REDUCE DOMAIN OF CORRESPONDING ROW, COLUMN AND BLOCK OF A VARIABLE
    def reduce_domain_value(self, key, value, domain_dict):
        keys = list(domain_dict.keys())
        row = int(key[0])
        col = int(key[1])
        for i in range(9):
            # FOR ROW
            if str(row)+str(i) in keys:
                if value in domain_dict[str(row)+str(i)]:
                    domain_dict[str(row)+str(i)].remove(value)
            
            # FOR COLUMN
            if str(i)+str(col) in keys:
                if value in domain_dict[str(i)+str(col)]:
                    domain_dict[str(i)+str(col)].remove(value)
        
        # FOR BLOCK
        block_row = int(row/3)
        block_col = int(col/3)
        for i in range(3):
            for j in range(3):
                if str(block_row*3 + i)+str(block_col*3 + j) in keys:
                    if value in domain_dict[str(block_row*3 + i)+str(block_col*3 + j)]:
                        domain_dict[str(block_row*3 + i)+str(block_col*3 + j)].remove(value)
        
#        print("New Domain = ")
#        for k in domain_dict.keys():
#            print("Key = ", k, " Domain = ", domain_dict[k])
        return domain_dict
        
    # BACKTRACK FUNCTION RETURN BOARD IF SUCCESSFUL OTHERWISE FALSE
    def backtracking(self, domain_dict):
        self.nodes = self.nodes + 1
#        print("\nBACKTRCKING\n")
        board = domain_dict['board']
#        self.print_board(board)
        del domain_dict['board']
        if self.check_no_value_domain(domain_dict) == True:
            return False
        
        sorted_keys = sorted(domain_dict, key = lambda key: len(domain_dict[key]))
#        print("Sorted keys = ", sorted_keys)
        for key in sorted_keys:
            if len(domain_dict[key]) == 1:
#                print("Key = ", key, " value = ", domain_dict[key][0])
#                print("Domain size = ", len(domain_dict[key]))
                board[int(key[0])][int(key[1])] = domain_dict[key][0]
                if self.constraint_satisfication(board):
                    new_domain = self.reduce_domain_value(key, domain_dict[key][0], domain_dict)
                    if len(domain_dict[key]) == 0:
                        del domain_dict[key]
                    if self.check_no_value_domain(new_domain) == True:
                        return False
                    new_domain['board'] = board
                    if len(new_domain) == 1:
#                        print("New domain is empty")
                        return new_domain
                    result = self.backtracking(new_domain)
#                    if result == False:
#                        print("FALSE for key = ", key)
                    return result
                else:
#                    print("Constraint Unsatisfied")
                    return False
            else:
                total = len(domain_dict[key])
                flag = True
                domain_dict_copy = {}
                domain_dict_copy = copy.deepcopy(domain_dict)
                board_list = []
                for i in range(9):
                    for j in range(9):
                        board_list.append(board[i][j])
                while total > 0 and flag == True:
                    ele = len(domain_dict[key]) - total
                    total = total - 1
#                    print("Key = ", key, " value = ", domain_dict[key][ele])
#                    print("Domain size = ", len(domain_dict[key]))
#                    print("Domain Dict = ", domain_dict)
#                    print("Board = ", board)
                    board[int(key[0])][int(key[1])] = domain_dict[key][ele]
                    if self.constraint_satisfication(board):
                        new_domain = self.reduce_domain_value(key, domain_dict[key][ele], domain_dict)
                        curr_domain = new_domain[key]
                        del new_domain[key]
                        if self.check_no_value_domain(new_domain) == True:
                            return False
                        new_domain['board'] = board
                        if len(new_domain) == 1:
#                            print("New domain is empty")
                            return new_domain
                        result = self.backtracking(new_domain)
                        if result != False:
                            flag = False
                        else:
#                            print("FALSE for key = ", key)
#                            print("Check for next value in domain")
                            domain_dict.clear()
#                            domain_dict = copy.deepcopy(domain_dict_copy)
#                            print("Board list = ", board_list)
#                            print(type(board_list))
                            board_array = np.array(board_list)
#                            print("Board array = ", board_array)
#                            print(type(board_array))
                            board_array = np.reshape(board_array, [9, 9])
#                            print("Board array = ", board_array)
                            board = board_array.tolist()
#                            print("Board = ", board)
                            k_list = list(domain_dict_copy.keys())
                            for k in k_list:
                                domain_dict[k] = domain_dict_copy[k]
#                            print("Domain = ", domain_dict)
                    else:
#                        print("Constraint Unsatisfied")
                        return False
                return result

# MAIN FUNCTION
if __name__ == '__main__':
    total_start_time = time.time()
    game = sudoku_BT()
    print("Problem Puzzle: ")
    game.print_board(game.board)
#    print(game.board)
#    print(len(game.board))
#    game.save_output(game.board)    
    d_dict = game.create_domain(game.board)
    d_dict = game.reduce_domain(game.board, d_dict)
    d_dict['board'] = game.board
    back_start_time = time.time()
    final = game.backtracking(d_dict)
    back_end_time = time.time()
    if final == False:
        print("Solution is not exist")
    else:
        print("Solved Puzzle:")
        game.print_board(final['board'])
        game.save_output(final['board'])
        if game.constraint_satisfication(final['board']):
            print("Constraint Satisfied")
        else:
            print("Constraint Unsatisfied")
    print("\nTotal time taken by code =  %s seconds" % (time.time() - total_start_time)) 
    print("\nTime taken by Backtrack function =  %s seconds" % (back_end_time - back_start_time))
    print("\nNo. of explored nodes = ", game.nodes)
        
    