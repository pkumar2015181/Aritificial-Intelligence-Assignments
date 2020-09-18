import numpy as np
import copy
import random
#from random import randint
import time

class sudoku_MC:
    # READ INPUT FROM TEXT FILE
    def __init__(self):
        input_file = open('input.txt').read()
        self.board = [list(map(int, line.split(' '))) for line in input_file.split('\n')]
    
    # SAVE OUTPUT IN TEXT FILE
    def save_output(self, board):
        sol_file = open("solution.txt","w") 
        for i in board:
            line = ' '.join([str(elem) for elem in i])
#            print(line)
            sol_file.write(line)
            sol_file.write("\n")
            
    # CHECK EACH CONSTRAINT
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
    
    # Total no. of conflict in board
    def board_conflict(self, board, row, col, value):
        board[row][col] = value
        count = 0
        arr = np.array(board)
        # CHECK FOR ALL ROWS
        for row in range(9):
            row_ele = []
            for i in range(9):
                if arr[row][i] != 0:
                    row_ele.append(arr[row][i])
            # CONTAINS DUPLICATES
            if len(row_ele) != len(set(row_ele)):
                count = count + 1
        
        # CHECK FOR ALL COLUMNS
        for col in range(9):
            col_ele = []
            for i in range(9):
                if arr[i][col] != 0:
                    col_ele.append(arr[i][col])
            # CONTAINS DUPLICATES
            if len(col_ele) != len(set(col_ele)):
                count = count + 1
        
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
                    count = count + 1
        return count
    
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

    # INITIALIZE ALL VARIABLE WITH RANDOM VALUE FROM ITS DOMAIN 
    def initialization(self, domain_dict):
        keys = list(domain_dict.keys())
        for key in keys:
            if key != 'board':
                row = int(key[0])
                col = int(key[1])
                domain_dict['board'][row][col] = random.choice(domain_dict[key])
        return domain_dict
           
    # FIND THE VALUE FROM ITS DOMAIN WHICH CONFLICTING LEAST
    def conflict(self, key, board, domain_dict):
        keys = list(domain_dict.keys())
        min_value = -1
        min_count = 0
        row = int(key[0])
        col = int(key[1])
        possible_values = domain_dict[key]
        for value in possible_values:
            count = []
            count.append(key)
            for i in range(9):
                # FOR ROW
                if str(row)+str(i) in keys:
                    if value == board[row][i] and str(row)+str(i) not in count:
                        count.append(str(row)+str(i))
                
                # FOR COLUMN
                if str(i)+str(col) in keys:
                    if value == board[i][col] and str(i)+str(col) not in count:
                        count.append(str(i)+str(col))
            
            # FOR BLOCK
            block_row = int(row/3)
            block_col = int(col/3)
            for i in range(3):
                for j in range(3):
                    if str(block_row*3 + i)+str(block_col*3 + j) in keys:
                        if value == board[block_row*3 + i][block_col*3 + j] and str(block_row*3 + i)+str(block_col*3 + j) not in count:
                            count.append(str(block_row*3 + i)+str(block_col*3 + j))
            
            count.remove(key)
#            print("Value = ", value, " count = ", count, " len = ", len(count))
            
            if min_value == -1:
                min_value = value
                min_count = count
            else:
                if len(count) < len(min_count):
                    min_value = value
                    min_count = count
        
#        print("key = ", key, "Min value = ", min_value, " count = ", min_count)
        return (min_value, len(min_count))
    
    # RETURN TRUE IF BOTH ARE DIFFERENT AND RETURN FALSE IF BOTH ARE SAME
    def check_diff(self, board_list, board):
        board_array = np.array(board_list)
        board_array = np.reshape(board_array, [9, 9])
        for i in range(9):
            for j in range(9):
                if board_array[i, j] != board[i][j]:
                    return True
        
        return False
    
    # MINMUM CONFLICT ALGORITHM WHICH RETURN BOARD
    def minconflict(self, domain_dict):
#        max_steps = int(input("Enter the no. of maximum steps : "))
        max_steps = 50000
        domain_dict = self.initialization(domain_dict)
        print("Puzzle after random initailization: ")
        self.print_board(domain_dict['board'])
        board = domain_dict['board']
        actual_conflict =  self.board_conflict(board, 0, 0, board[0][0]) 
        board_list = []
        for i in range(9):
            for j in range(9):
                board_list.append(board[i][j])
        del domain_dict['board']
        keys = sorted(domain_dict, key = lambda key: len(domain_dict[key]))
        random.shuffle(keys)
#        keys = domain_keys
#        print("keys = ", keys)
        key = 0
        for step in range(max_steps):
#            print("step = ", step, " Actual Conf = ", actual_conflict)
#            if step%5000 == 0:
#                print("steps = ", step, " is completed")
#            print(key, " value = ", keys[key])
            row = int(keys[key][0])
            col = int(keys[key][1])
            (value, conf) = self.conflict(keys[key], board, domain_dict)
#            self.print_board(board)
            t_conf = self.board_conflict(board, row, col, value)
            if t_conf < actual_conflict:
                print("step = ", step, " Actual Conflicts = ", actual_conflict)
                actual_conflict = t_conf
                board[row][col] = value
                if actual_conflict == 0:
                    print("step = ", step, " Actual Conflicts = 0")
                    domain_dict['board'] = board
                    return domain_dict
            
            key = (key + 1)%len(keys)
            if key == 0:
#                self.print_board(board)
                current_board = []
                for i in range(9):
                    for j in range(9):
                        current_board.append(board[i][j])
                if board_list == current_board:
#                    print("Same board")
                    for c in range(10):
                        rand_key = random.choice(keys)
                        board[int(rand_key[0])][int(rand_key[1])] = random.choice(domain_dict[rand_key])
                else:
                    board_list = current_board
        
        domain_dict['board'] = board
        return domain_dict
            

# MAIN FUNCTION
if __name__ == '__main__':
    total_start_time = time.time()
    game = sudoku_MC()
    print("Problem Puzzle: ")
    game.print_board(game.board)
#    print(game.board)
#    print(len(game.board))
#    game.save_output(game.board)    
    d_dict = game.create_domain(game.board)
    d_dict = game.reduce_domain(game.board, d_dict)
    d_dict['board'] = game.board
    conf_start_time = time.time()
    final = game.minconflict(d_dict)
    conf_end_time = time.time()
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
    print("\nTime taken by Min. conflict function =  %s seconds" % (conf_end_time - conf_start_time))
        
    