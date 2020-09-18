import numpy as np
from random import randint
import time

class TicTacToe:
    def __init__(self):
        # EMPTY BOARD
        # 0 MEANS BLANK
        #print("Board for tic tac toe game\n")
#        self.board = [[2, 0, 2, 2], [1, 0, 1, 2], [1, 2, 1, 1], [2, 1, 0, 0]]
        self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.curr_player = 1
        self.explored_nodes = 1
        self.depth = 0
    
    # TO DISPLAY CURRENT STATE POSITION
    def show_board(self):
        print("\n")
        for i in range(4):
            for j in range(4):
                print("| ", end='')
                if self.board[i][j] == 0:
                    print("  ", end='')
                elif self.board[i][j] == 1:
                    print("X ", end='')
                else:
                    print("O ", end='')
            print("|\n")
    
    # # TO CHECK GAME OVER CON
    # def gameover(self):
    #     for i in range(4):
    #         for j in range(4):
    #             if self.board[i][j] == 0:
    #                 return False
    #     return True
            
    def chance_winning(self, state, player):
        count = 0
        diag_l1 = 0
        diag_l2 = 0
        diag_r1 = 0
        diag_r2 = 0
        for i in range(4):
            row_1 = 0
            row_2 = 0
            col_1 = 0
            col_2 = 0
            for j in range(4):
                if state[i][j] == 1:
                    row_1 = row_1 + 1
                elif state[i][j] == 2:
                    row_2 = row_2 + 1
                
                if state[j][i] == 1:
                    col_1 = col_1 + 1
                elif state[j][i] == 2:
                    col_2 = col_2 + 1
            if player == 1 and row_1 > 0 and row_2 == 0:
                count = count + 1
            if player == 2 and row_2 > 0 and row_1 == 0:
                count = count + 1
            
            if player == 1 and col_1 > 0 and col_2 == 0:
                count = count + 1
            if player == 2 and col_2 > 0 and col_1 == 0:
                count = count + 1
            
            if row_1 == 0 and row_2 == 0:
                count = count + 1
            if col_1 == 0 and col_2 == 0:
                count = count + 1
            
            if state[i][i] == 1:
                diag_l1 = diag_l1 + 1
            elif state[i][i] == 2:
                diag_l2 = diag_l2 + 1
            
            if state[i][3-i] == 1:
                diag_r1 = diag_r1 + 1
            elif state[i][3-i] == 2:
                diag_r2 = diag_r2 + 1
        
        if player == 1 and diag_l1 > 0 and diag_l2 == 0:
            count = count + 1
        if player == 2 and diag_l2 > 0 and diag_l1 == 0:
            count = count + 1
        
        if diag_l1 == 0 and diag_l2 == 0:
            count = count + 1
        if diag_r1 == 0 and diag_r2 == 0:
            count = count + 1
            
        if player == 1 and diag_r1 > 0 and diag_r2 == 0:
            count = count + 1
        if player == 2 and diag_r2 > 0 and diag_r1 == 0:
            count = count + 1
        
        
        return count
            
            
    
    # CHECK WHO WIN THE GAME
    def check_win(self, board):
        for i in range(4):
            #FOR PLAYER 1
            #check for rows
            if board[i][0] == 1 and board[i][1] == 1 and board[i][2] == 1 and board[i][3] == 1:
                return 1
            #check for column
            if board[0][i] == 1 and board[1][i] == 1 and board[2][i] == 1 and board[3][i] == 1:
                return 1
            
            #FOR PLAYER 2
            #check for rows
            if board[i][0] == 2 and board[i][1] == 2 and board[i][2] == 2 and board[i][3] == 2:
                return 2
            #check for column
            if board[0][i] == 2 and board[1][i] == 2 and board[2][i] == 2 and board[3][i] == 2:
                return 2
        #FOR PLAYER 1
        #check left diagonal
        if board[0][0] == 1 and board[1][1] == 1 and board[2][2] == 1 and board[3][3] == 1:
            return 1
        #check for right diagonal
        if board[0][3] == 1 and board[1][2] == 1 and board[2][1] == 1 and board[3][0] == 1:
            return 1
        
        #FOR PLAYER 2
        #check left diagonal
        if board[0][0] == 2 and board[1][1] == 2 and board[2][2] == 2 and board[3][3] == 2:
            return 2
        #check for right diagonal
        if board[0][3] == 2 and board[1][2] == 2 and board[2][1] == 2 and board[3][0] == 2:
            return 2
        return 0
    
    # CHECK WEATHER STATE IS TERMINAL STATE OR NOT
    def check_leaf_state(self, board):
        for i in range(4):
            #FOR PLAYER 1
            #check for rows
            if board[i][0] == 1 and board[i][1] == 1 and board[i][2] == 1 and board[i][3] == 1:
                return True
            #check for column
            if board[0][i] == 1 and board[1][i] == 1 and board[2][i] == 1 and board[3][i] == 1:
                return True
            
            #FOR PLAYER 2
            #check for rows
            if board[i][0] == 2 and board[i][1] == 2 and board[i][2] == 2 and board[i][3] == 2:
                return True
            #check for column
            if board[0][i] == 2 and board[1][i] == 2 and board[2][i] == 2 and board[3][i] == 2:
                return True
        #FOR PLAYER 1
        #check left diagonal
        if board[0][0] == 1 and board[1][1] == 1 and board[2][2] == 1 and board[3][3] == 1:
            return True
        #check for right diagonal
        if board[0][3] == 1 and board[1][2] == 1 and board[2][1] == 1 and board[3][0] == 1:
            return True
        
        #FOR PLAYER 2
        #check left diagonal
        if board[0][0] == 2 and board[1][1] == 2 and board[2][2] == 2 and board[3][3] == 2:
            return True
        #check for right diagonal
        if board[0][3] == 2 and board[1][2] == 2 and board[2][1] == 2 and board[3][0] == 2:
            return True
        
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    return False
        return True
    
    # RETURN ALL POSSIBLE MOVE STATES
    def getpossiblemoves(self, state, player):
        current = []
        for i in range(4):
            for j in range(4):
                current.append(state[i][j])
        moves = []
        for i in range(16):
            if current[i] == 0:
                pre = current.copy()
                pre[i] = player
                new_state = np.reshape(pre, (4,4)).tolist()
                #print(new_state)
                moves.append(new_state)
        return moves
    
    def get_heuristic_val(self, state):
        win_chance1 = self.chance_winning(state, 1)
        win_chance2 = self.chance_winning(state, 2)
        diff = win_chance1 - win_chance2
        if diff == 0:
            return 0
        elif diff > 0:
            return 1
        else:
            return 2
    
    # RETURN BEST MOVE
    def getbestmove(self, state, player, depth):
#        print("\n\nstate = ", state, " ply = ", player)
#        print("depth = ", depth)
        
        # FOR TERMINAL STATE
        if self.check_leaf_state(state) == True:
#            print("Terminal state")
            # CHANGE STATE TO TUPLE
            current = []
            for i in range(4):
                for j in range(4):
                    current.append(state[i][j])
            best_moves = {}
            win_player = self.check_win(state)
#            print("Winner player = ", win_player)
            if win_player == 0:
                best_moves[tuple(current)] = 0
            elif win_player == 1:
                if self.curr_player == 1:
#                    print("C1")
                    best_moves[tuple(current)] = 1
                else:
#                    print("C2")
                    best_moves[tuple(current)] = -1
            elif win_player == 2:
                if self.curr_player == 1:
#                    print("C3")
                    best_moves[tuple(current)] = -1
                else:
#                    print("C4")
                    best_moves[tuple(current)] = 1
#            print("Best move = ", best_moves)
            return best_moves
        # FOR NON-TERMINAL STATE
        else:
            if depth <= 0:
#                print("Depth over -- Middle state")
                # CHANGE STATE TO TUPLE
                current = []
                for i in range(4):
                    for j in range(4):
                        current.append(state[i][j])
                best_moves = {}
                win_player = self.get_heuristic_val(state)
#                print("Winner player = ", win_player)
                if win_player == 0:
                    best_moves[tuple(current)] = 0
                elif win_player == 1:
                    if self.curr_player == 1:
#                        print("C1")
                        best_moves[tuple(current)] = 1
                    else:
#                        print("C2")
                        best_moves[tuple(current)] = -1
                elif win_player == 2:
                    if self.curr_player == 1:
#                        print("C3")
                        best_moves[tuple(current)] = -1
                    else:
#                        print("C4")
                        best_moves[tuple(current)] = 1
#                print("Best move = ", best_moves)
                return best_moves
                
            else:
                possible_moves = self.getpossiblemoves(state, player)
#                print("Possible moves = ", possible_moves)
#                print("No. of moves = ", len(possible_moves))
                best_moves = {}
                pos_best_val = float('-Inf')
                neg_best_val = float('Inf')
                for next_state in possible_moves:
                    self.explored_nodes = self.explored_nodes + 1
                    curr = []
                    for i in range(4):
                        for j in range(4):
                            curr.append(state[i][j])
                    if player == 1:
                        down_move = self.getbestmove(next_state, 2, depth-1)
                    else:
                        down_move = self.getbestmove(next_state, 1, depth-1)
                    for m in down_move:
                        val = down_move[m]
                        # CHOOSE MAXIMUM VALUE STATE
                        if player == self.curr_player:
                            if val > pos_best_val:
                                best_moves.clear()
                                pos_best_val = val
                                board = []
                                for i in range(4):
                                    for j in range(4):
                                        board.append(self.board[i][j])
                                if curr == board:
#                                    print("========")
                                    best_moves[m] = val
                                else:
                                    best_moves[tuple(curr)] = val
                                
                            elif val == pos_best_val:
                                board = []
                                for i in range(4):
                                    for j in range(4):
                                        board.append(self.board[i][j])
                                if curr == board:
#                                    print("========")
                                    best_moves[m] = val
                                else:
                                    best_moves[tuple(curr)] = val
                        # CHOOSE MINIMUM VALUE STATE
                        else:
                            if val < neg_best_val:
                                best_moves.clear()
                                neg_best_val = val
                                board = []
                                for i in range(4):
                                    for j in range(4):
                                        board.append(self.board[i][j])
                                if curr == board:
#                                    print("========")
                                    best_moves[m] = val
                                else:
                                    best_moves[tuple(curr)] = val
                                
                            elif val == neg_best_val:
                                board = []
                                for i in range(4):
                                    for j in range(4):
                                        board.append(self.board[i][j])
                                if curr == board:
#                                    print("========")
                                    best_moves[m] = val
                                else:
                                    best_moves[tuple(curr)] = val
                
#                print("\nstate = ", state, " ply = ", player)
#                print("Non-terminal state")
#                print("Best moves = ", best_moves)
                
                # CHOOSE RANDOM MOVE FROM ALL BEST MOVES
                total_moves = len(best_moves)
                if total_moves == 1:
                    return best_moves
                else:
                    rand_move = {}
                    states = []
                    s = 0
                    for m in best_moves:
                        s = s+1
                        states.append(m)
                    
                    
                    
                    # print("\n========================\n")
                    # next_sta = None
                    # ch = float('Inf')
                    # for st in states:
                    #     mat = np.reshape(st, (4,4)).tolist()
                    #     print("mat = ", mat)
                    #     if player == 1:
                    #         print("C1")
                    #         if ch > self.chance_winning(mat, 2):
                    #             print("C2")
                    #             next_sta = st
                    #     if player == 2:
                    #         print("C3");
                    #         if ch > self.chance_winning(mat, 1):
                    #             print("C4")
                    #             next_sta = st
                    
                    # rand_move[next_sta] = best_moves[next_sta]
                    # print("Rand move = ", rand_move)
                    
                    # print("\n========================\n")
                    # return rand_move
                    
                    rand_no = randint(0, s-1)
#                    print("states = ", states)
#                    print("s = ", s)
#                    print("rand no = ", rand_no)
                    rand_move[states[rand_no]] = best_moves[states[rand_no]]
#                    print("Rand move = ", rand_move)
                    return rand_move
  

# MAIN FUNCTION
if __name__ == '__main__':
    game = TicTacToe()
    player = 1
    depth = int(input("Enter depth of search: "))
    game.depth = depth
    
    # CHECK GAME IS OVER OR NOT
    while game.check_leaf_state(game.board) == False:
        game.show_board()
        if player == 1:
            print("Player - 1")
            game.curr_player = 1
            start_time = time.time()
            down_move = game.getbestmove(game.board, 1, depth)
#            print(down_move)
            for m in down_move:
                game.board = np.reshape(m, (4,4)).tolist()
            print("\nTime taken for 1 move =  %s seconds" % (time.time() - start_time)) 
            print("No. of explored nodes = ", game.explored_nodes)
            game.explored_nodes = 0
            game.depth = depth
            player = 2
        else:
            print("Player - 2")
            game.curr_player = 2
            flag = 1
            while flag == 1:
                move = int(input("You are O: Choose blank tile from board between 1-16 (left to right and top to bottom): "))
                move = move - 1
                if game.board[int(move/4)][move%4] == 0:
                    game.board[int(move/4)][move%4] = 2
                    flag = 0
                else:
                    print("Invalid Position! Choosen tile is not blank. Choose another tile")
            
            player = 1
    
    game.show_board()
    win_player = game.check_win(game.board)
    if win_player == 0:
        print("Match is draw")
    elif win_player == 1:
        print("Player 1 wins")
    else:
        print("Player 2 wins")