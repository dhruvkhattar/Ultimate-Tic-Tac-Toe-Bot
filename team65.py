import sys
import random
import signal
import copy

def get_init_board_and_blockstatus():

    board = []
    for i in range(9):
        row = ['-']*9
        board.append(row)
                                    
    block_stat = ['-']*9
    return board, block_stat


class Tree_Node:
    def __init__(self, board, block, child_array, parent, current_move):
        self.board = board
        self.block = block
        self.current_move = current_move
        self.child_array = child_array
        self.parent = parent
        self.heuristic = 0
        self.alpha = -9223372036854775808
        self.beta = 9223372036854775807
        return

class Tree:

    def __init__(self):
        self.root = None
        return
    def determine_blocks_allowed(self, old_move, block_stat):
		blocks_allowed = []
		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			blocks_allowed = [1,3]
		elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
			blocks_allowed = [1,5]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
			blocks_allowed = [3,7]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
			blocks_allowed = [5,7]
		elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
			blocks_allowed = [0,2]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
			blocks_allowed = [0,6]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
			blocks_allowed = [6,8]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
			blocks_allowed = [2,8]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
			blocks_allowed = [4]
		else:
			sys.exit(1)
		final_blocks_allowed = []
        #print blocks_allowed
        #print block_stat
		for i in blocks_allowed:
			if block_stat[i] == '-':
				final_blocks_allowed.append(i)
        #print final_blocks_allowed
		return final_blocks_allowed


    def update_lists(self,game_board, block_stat, move_ret, fl):
        game_board[move_ret[0]][move_ret[1]] = fl
        block_no = (move_ret[0]/3)*3 + move_ret[1]/3
        id1 = block_no/3
        id2 = block_no%3
        mflg = 0
        flag = 0
        for i in range(id1*3,id1*3+3):
            for j in range(id2*3,id2*3+3):
                if game_board[i][j] == '-':
                    flag = 1
                    
        if block_stat[block_no] == '-':
            if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
                mflg=1
            if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
                mflg=1
                
            if mflg != 1:
                for i in range(id2*3,id2*3+3):
                    if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-' and game_board[id1*3][i] != 'D':
                        mflg = 1
                        break
                    
            if mflg != 1:
                for i in range(id1*3,id1*3+3):
                    if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-' and game_board[i][id2*3] != 'D':
                        mflg = 1
                        break
        if flag == 0:
		    block_stat[block_no] = 'D'
        if mflg == 1:
            block_stat[block_no] = fl
	
	    return mflg                
    def get_empty_out_of(self, gameb, blal,block_stat):
        cells = []  
        for idb in blal:
            id1 = idb/3
            id2 = idb%3
            for i in range(id1*3,id1*3+3):
                for j in range(id2*3,id2*3+3):
                    if gameb[i][j] == '-':
                        cells.append((i,j))

        if cells == []: 
            new_blal = []
            all_blal = [0,1,2,3,4,5,6,7,8]
            for i in all_blal:
                if block_stat[i]=='-':
                    new_blal.append(i)

            for idb in new_blal:
                id1 = idb/3
                id2 = idb%3
                for i in range(id1*3,id1*3+3):
                    for j in range(id2*3,id2*3+3):
                        if gameb[i][j] == '-':
                            cells.append((i,j))
        return cells

  
    def generate_moves(self, node, flag):
        blocks = self.determine_blocks_allowed(node.current_move, node.block)
        child_states = self.get_empty_out_of(node.board, blocks, node.block)
        t_board = node.board
        moves = []
        for child in child_states:
            new_board = copy.deepcopy(t_board)
            new_board[child[0]][child[1]] = flag
            t_block = copy.deepcopy(node.block)
            ret = self.update_lists(new_board, t_block, child, flag)
            child_node = Tree_Node(new_board, t_block, [], node, child)
            moves.append(child_node)
        return moves

    def build_tree(self, root, depth, flag):
        child_states = []
        blocks = self.determine_blocks_allowed(root.current_move, root.block)
        if not blocks:
            depth = depth - 1
        
        if self.root == None and root.current_move[0] == -1 and root.current_move[1] == -1:
            new_board = copy.deepcopy(root.board)
            t_block = copy.deepcopy(root.block)
            blocks = range(9)
            states = self.get_empty_out_of(new_board, blocks, t_block)
            x, y = states[random.randrange(len(states))]
            new_board[x][y] = flag
            self.update_lists(new_board, t_block, (x, y), flag)
            temp = Tree_Node(new_board, t_block, [], root, (x, y))
            child_states.append(temp)
            self.root = root

        if not child_states: #check
            child_states = self.generate_moves(root, flag)

        root.child_array = child_states
        parent = root

        while depth - 1 :
            new_child_nodes = []
            if flag == 'x':
                flag = 'o'
            else:
                flag = 'x'
            for node in child_states:
                if not node.child_array: #check
                    '''if flag == 'x':
                        flag = 'o'
                    else:
                        flag = 'x'''
                    new_child_states = self.generate_moves(node, flag)
                    node.child_array = new_child_states
                    new_child_nodes = new_child_nodes + new_child_states
                else: # remove redundant code
                    for child in node.child_array:
                        child.heuristic = 0
                        child.alpha = -9223372036854775808
                        child.beta = 9223372036854775807
            '''if flag == 'x':
                flag = 'o'
            else:
                flag = 'x'''
            depth = depth - 1
            child_states = new_child_nodes

        return

dummy_board, dummy_block = get_init_board_and_blockstatus()
tree = Tree()
old_node = Tree_Node(dummy_board, dummy_block, [], None, (-1, -1))

class Player65:

    def __init__(self):
		    pass

    def heuristic(self, temp_board, block_stat, flag):
        h_values = []
        h_values.append(self.heuristic_small([temp_board[0][0], temp_board[0][1], temp_board[0][2], temp_board[1][0], temp_board[1][1], temp_board[1][2], temp_board[2][0], temp_board[2][1], temp_board[2][2] ], flag, 0))
        h_values.append(self.heuristic_small([temp_board[0][3], temp_board[0][4], temp_board[0][5], temp_board[1][3], temp_board[1][4], temp_board[1][5], temp_board[2][3], temp_board[2][4], temp_board[2][5] ], flag, 0))
        h_values.append(self.heuristic_small([temp_board[0][6], temp_board[0][7], temp_board[0][8], temp_board[1][6], temp_board[1][7], temp_board[1][8], temp_board[2][6], temp_board[2][7], temp_board[2][8] ], flag, 0))
        h_values.append(self.heuristic_small([temp_board[3][0], temp_board[3][1], temp_board[3][2], temp_board[4][0], temp_board[4][1], temp_board[4][2], temp_board[5][0], temp_board[5][1], temp_board[5][2] ], flag, 0))
        h_values.append(self.heuristic_small([temp_board[3][3], temp_board[3][4], temp_board[3][5], temp_board[4][3], temp_board[4][4], temp_board[4][5], temp_board[5][3], temp_board[5][4], temp_board[5][5] ], flag, 0))
        h_values.append(self.heuristic_small([temp_board[3][6], temp_board[3][7], temp_board[3][8], temp_board[4][6], temp_board[4][7], temp_board[4][8], temp_board[5][6], temp_board[5][7], temp_board[5][8] ], flag, 0))
        h_values.append(self.heuristic_small([temp_board[6][0], temp_board[6][1], temp_board[6][2], temp_board[7][0], temp_board[7][1], temp_board[7][2], temp_board[8][0], temp_board[8][1], temp_board[8][2] ], flag, 0))
        h_values.append(self.heuristic_small([temp_board[6][3], temp_board[6][4], temp_board[6][5], temp_board[7][3], temp_board[7][4], temp_board[7][5], temp_board[8][3], temp_board[8][4], temp_board[8][5] ], flag, 0))
        h_values.append(self.heuristic_small([temp_board[6][6], temp_board[6][7], temp_board[6][8], temp_board[7][6], temp_board[7][7], temp_board[7][8], temp_board[8][6], temp_board[8][7], temp_board[8][8] ], flag, 0))
        h_sum = 0

        for i in h_values:
            h_sum = h_sum + i
        h_sum2 = self.heuristic_small(block_stat, flag, 1)
        
        return h_sum + h_sum2

    def heuristic_small(self, block, flag, choice):
        h_sum = 0
        lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        if flag == 'x':
            nflag = 'o'
        else:
            nflag = 'x'

        if choice == 0:
            for line in lines:
                if block[line[0]] == flag and block[line[1]] == flag and block[line[2]] == flag:
                    h_sum += 10
                elif (block[line[0]] == flag and block[line[1]] == flag and block[line[2]] == '-') or (block[line[0]] == flag and block[line[2]] == flag and block[line[1]] == '-') or (block[line[2]] == flag and block[line[1]] == flag and block[line[0]] == '-'):
                    h_sum += 5
                elif (block[line[0]] == flag and block[line[1]] == '-' and block[line[2]] == '-') or (block[line[0]] == '-' and block[line[2]] == flag and block[line[1]] == '-') or (block[line[2]] == '-' and block[line[1]] == flag and block[line[0]] == '-'):
                    h_sum += 1
                elif block[line[0]] == nflag and block[line[1]] == nflag and block[line[2]] == nflag:
                    h_sum -= 10
                elif (block[line[0]] == nflag and block[line[1]] == nflag and block[line[2]] == '-') or (block[line[0]] == nflag and block[line[2]] == nflag and block[line[1]] == '-') or (block[line[2]] == nflag and block[line[1]] == nflag and block[line[0]] == '-'):
                    h_sum -= 5
                elif (block[line[0]] == nflag and block[line[1]] == '-' and block[line[2]] == '-') or (block[line[0]] == '-' and block[line[2]] == nflag and block[line[1]] == '-') or (block[line[2]] == '-' and block[line[1]] == nflag and block[line[0]] == '-'):
                    h_sum -= 1
                else:
                    pass
        else:
            for line in lines:
                if block[line[0]] == flag and block[line[1]] == flag and block[line[2]] == flag:
                    h_sum += 1000
                elif (block[line[0]] == flag and block[line[1]] == flag and block[line[2]] == '-') or (block[line[0]] == flag and block[line[2]] == flag and block[line[1]] == '-') or (block[line[2]] == flag and block[line[1]] == flag and block[line[0]] == '-'):
                    h_sum += 500
                elif (block[line[0]] == flag and block[line[1]] == '-' and block[line[2]] == '-') or (block[line[0]] == '-' and block[line[2]] == flag and block[line[1]] == '-') or (block[line[2]] == '-' and block[line[1]] == flag and block[line[0]] == '-'):
                    h_sum += 100
                elif block[line[0]] == nflag and block[line[1]] == nflag and block[line[2]] == nflag:
                    h_sum -= 1000
                elif (block[line[0]] == nflag and block[line[1]] == nflag and block[line[2]] == '-') or (block[line[0]] == nflag and block[line[2]] == nflag and block[line[1]] == '-') or (block[line[2]] == nflag and block[line[1]] == nflag and block[line[0]] == '-'):
                    h_sum -= 500
                elif (block[line[0]] == nflag and block[line[1]] == '-' and block[line[2]] == '-') or (block[line[0]] == '-' and block[line[2]] == nflag and block[line[1]] == '-') or (block[line[2]] == '-' and block[line[1]] == nflag and block[line[0]] == '-'):
                    h_sum -= 100
                else:
                    pass
        return h_sum
            
    
    def alpha_beta_prune(self, branch, depth, alpha, beta, flag):
        if len(branch.child_array) == 0:
            if ((depth) % 2 == 1):
                branch.beta = self.heuristic(branch.board, branch.block, flag)
            else:
                branch.alpha = self.heuristic(branch.board, branch.block, flag)

        for child_object in branch.child_array:
            self.alpha_beta_prune(child_object, depth + 1, branch.alpha, branch.beta, flag)

            # this is where the pruning takes place

            if ((depth)%2 == 1):
                if(branch.beta < alpha ):
                    break
            else:
                if(branch.alpha > beta):
                    break

            if((depth)%2 == 1):
                branch.beta = child_object.alpha if branch.beta > child_object.alpha else branch.beta

            else:
                branch.alpha = child_object.beta if branch.alpha < child_object.beta else branch.alpha

        return


    def update_lists(self,game_board, block_stat, move_ret, fl):
        game_board[move_ret[0]][move_ret[1]] = fl
        block_no = (move_ret[0]/3)*3 + move_ret[1]/3
        id1 = block_no/3
        id2 = block_no%3
        mflg = 0
        flag = 0
        for i in range(id1*3,id1*3+3):
            for j in range(id2*3,id2*3+3):
                if game_board[i][j] == '-':
                    flag = 1
                    
        if block_stat[block_no] == '-':
            if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
                mflg=1
            if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
                mflg=1
                
            if mflg != 1:
                for i in range(id2*3,id2*3+3):
                    if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-' and game_board[id1*3][i] != 'D':
                        mflg = 1
                        break
                    
            if mflg != 1:
                for i in range(id1*3,id1*3+3):
                    if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-' and game_board[i][id2*3] != 'D':
                        mflg = 1
                        break
        if flag == 0:
		    block_stat[block_no] = 'D'
        if mflg == 1:
            block_stat[block_no] = fl
	
	    return mflg                

    def move(self,temp_board,temp_block,old_move,flag):

        global old_node
        global tree

        new_board = copy.deepcopy(temp_board)
        t_block = copy.deepcopy(temp_block)
        #ret = self.update_lists(new_board, t_block, old_move, flag)
        #print ret
        new_node = Tree_Node(new_board, t_block, [], old_node, old_move)
        old_node = new_node
        tree.build_tree(old_node, 3, flag)
        self.alpha_beta_prune(old_node, 0, -10000, 10000, flag)
        temp = old_node.alpha
        for child in old_node.child_array:
            for child in old_node.child_array:
                if temp == child.beta:
                    old_node = child
                    return child.current_move
                else:
                    pass
