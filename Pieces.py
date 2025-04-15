import copy

class ChezzPiece():
    def __init__(self, color, piece, coord, board, reverse_grid_dict):
        self.board = board
        self.coord = coord
        self.color = color
        self.piece = piece
        self.reverse_grid_dict = reverse_grid_dict
        self.position = reverse_grid_dict[coord]

    def __str__(self):
        return self.color + ' ' + self.piece + ' at ' + str(self.coord)

    def contangion(self, turn, pos):

        #print("Position: ", pos)
        #print("turn: ", turn)
        possible_directions = [(-1,0), (1,0), (0,1), (0,-1)]
        #(-1,-1), (-1,1), (1,-1), (1,1) < queen style infections 

        zombied_pieces = []

        for direction in possible_directions:
            current_row = pos[0]
            current_col = pos[1]

            while True:
                current_row += direction[0]
                current_col += direction[1]
                if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                    break
                #piece found in radius
                if self.board[current_row, current_col] != ' ':
                    #print("Piece: ", self.board[current_row, current_col])
                    if self.board[current_row, current_col][0] == 'b' and turn == 'b' and self.board[current_row, current_col][1] != 'K' and self.board[current_row, current_col][1] != 'Z':
                        #print("black piece next to zombie")
                        zombied_pieces.append(self.reverse_grid_dict[current_row, current_col])


                    elif self.board[current_row, current_col][0] == 'w' and turn == 'w' and self.board[current_row, current_col][1] != 'K' and self.board[current_row, current_col][1] != 'Z':
                        #print("white piece next to zombie: ", self.board[current_row, current_col])
                        zombied_pieces.append(self.reverse_grid_dict[current_row, current_col])
                break
        return zombied_pieces

                



        
        pass

    def moves(self):
     
        if self.piece == 'F':
            return self.flinger()
        elif self.piece == 'P':
            return self.peon()
        elif self.piece == 'N':
            return self.knight()
        elif self.piece == 'C':
            return self.cannon()
        elif self.piece == 'Q':
            return self.queen()
        elif self.piece == 'K':
            return self.king()
        elif self.piece == 'Z':
            return self.zombie()
        elif self.piece == 'B':
            return self.bishop()
        elif self.piece == 'R':
            return self.rook()
        
    #I THINK ITS DONE
    def flinger(self):
        possible_directions = [(-1,0), (1,0), (0,1), (0,-1), 
                               (-1,-1), (-1,1), (1,-1), (1,1)]

        all_possible_moves = []

        #moves based off position
        for direction in possible_directions:
            current_row = self.coord[0]
            current_col = self.coord[1]
            while True:
                current_row += direction[0]
                current_col += direction[1]
                if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                    break
                if self.board[current_row, current_col] == ' ':
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
                    break
                else:
                    #we cannot capture but we can catapult
                    piece = self.board[current_row, current_col]
                    piece_pos = (current_row, current_col)
                    #print("We can fling piece: ", piece)

                   
                    if self.color == piece[0]:
                        row_flung_direction = -(direction[0])
                        col_flung_direction = -(direction[1])

                      

                        while True:

                            current_row += row_flung_direction
                            current_col += col_flung_direction

                            # print("Direction: ", row_flung_direction, col_flung_direction)

                        
                            #print(f"Looking at: ({current_row}, {current_col}): {self.board[current_row, current_col]}")
                            if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                                #print("Out of bounds")
                                break
                            if self.board[current_row, current_col] == self.piece:
                                #print("Skip flinger")
                                break
                                

                            #flung piece lands on an empty spot
                            if self.board[current_row, current_col] == ' ':
                                all_possible_moves.append([self.reverse_grid_dict[piece_pos[0], piece_pos[1]], f"{piece[0]}{piece[1]}", self.reverse_grid_dict[current_row, current_col], None])
                                

                            #flung piece lands on an enemy piece and both get destroyed
                            elif self.color != self.board[current_row, current_col][0]:
                                all_possible_moves.append([self.reverse_grid_dict[piece_pos[0], piece_pos[1]], " ", self.reverse_grid_dict[current_row, current_col], self.board[current_row, current_col][0]])
                                
                    break
        return all_possible_moves      


      
    #DONE
    def peon(self):
        
        #can only move forward
        #can only capture diagonally forward
        all_possible_moves = []
        w_directions_move = [(0,1)]
        b_directions_move = [(0,-1)]
        w_directions_capture = [(-1,1), (1,1)]
        b_directions_capture = [(-1,-1), (1,-1)]


        if self.color == 'w':
            for direction in w_directions_move:
                current_row = self.coord[0] + direction[0]
                current_col = self.coord[1] + direction[1]


              
                if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                    break
                
                if self.board[current_row, current_col] == ' ':
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
                else:
                    break
            for direction in w_directions_capture:
           
                current_row = self.coord[0] + direction[0]
                current_col = self.coord[1] + direction[1]
                if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                    break
                if self.board[current_row, current_col] != ' ' and self.board[current_row, current_col][0] != self.color:
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], self.board[current_row, current_col]])
                
        else: # color is black
            for direction in b_directions_move:
                current_row = self.coord[0] + direction[0]
                current_col = self.coord[1] + direction[1]
                if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                    break
                if self.board[current_row, current_col] == ' ':
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
                else:
                    break
            for direction in b_directions_capture:
                current_row = self.coord[0] + direction[0]
                current_col = self.coord[1] + direction[1]
                if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                    break
                if self.board[current_row, current_col] != ' ' and self.board[current_row, current_col][0] != self.color:
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], self.board[current_row, current_col]])
                

        return all_possible_moves
        pass

    #DONE
    def knight(self):
        #print("KNIGHT - CHECKING ALL POSSIBLE MOVES")
        all_possible_moves = []
        new_board_pos = []
       
        #for each direction, check if valid move
        possible_directions = [(-1,-2), (-2, -1), (-1, 2), (-2, 1), (1, -2), (2, -1), (1, 2), (2, 1)]
        for direction in possible_directions:
            current_row = self.coord[0] + direction[0]
            current_col = self.coord[1] + direction[1]
            
            while True:
                if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                    break
                if self.board[current_row, current_col] == ' ':
                    #all_possible_moves.append(f"{self.reverse_grid_dict[current_row, current_col]}: {self.color}{self.piece}")

                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
                
                    break
                else:
                    #check if we can capture
                    if self.color != self.board[current_row, current_col][0]:
                        all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
                    break

        #print("New board pos: ", new_board_pos)
        #print("All possible moves: ", all_possible_moves)
        return all_possible_moves
        pass
    
    #DONE I THINK
    def cannon(self):
        

        possible_directions = [(-1,0), (1,0), (0,1), (0,-1)]
        all_possible_moves = []
        for direction in possible_directions:
            current_row = self.coord[0] + direction[0]
            current_col = self.coord[1] + direction[1]
            if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                continue
            if self.board[current_row, current_col] == ' ':
                all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
            #we cannot capture

        #can fire a cannonball on any diagonal
        possible_directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
        

        #store pieces that need to be removed
        #[old position, piece]
        

        for direction in possible_directions:
            piece_on_diagonal = False
            pieces_to_remove = []
           
            current_row = self.coord[0]
            current_col = self.coord[1]

            while True:
                current_row += direction[0]
                current_col += direction[1]
                if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                    break
                if self.board[current_row, current_col] != ' ':
                    piece_on_diagonal = True
                    pieces_to_remove.append([self.reverse_grid_dict[current_row, current_col], self.board[current_row, current_col]])
                    

            #'X' and 'Y' and 'Z', 'XZ' is logic used in the Chezz file
           
            if piece_on_diagonal:
                
                
                for piece in pieces_to_remove:
                    
                    #only one element
                    if len(pieces_to_remove) == 1:
                        all_possible_moves.append([piece[0], piece[1], "XZ", None])
                    #last element
                    elif piece == pieces_to_remove[-1]:
                        all_possible_moves.append([piece[0], piece[1], "Z", None])
                    #first element
                    elif piece == pieces_to_remove[0]:
                        all_possible_moves.append([piece[0], piece[1], "X", None])
                    else:                                        
                        all_possible_moves.append([piece[0], piece[1], "Y", None])
               
     
        return all_possible_moves
    
    #DONE
    def queen(self):

        #queen can move up down and diagonally in all directions
        possible_directions= [(1,1), (1,-1), (-1,1), (-1,-1), (0,1), (0,-1), (1,0), (-1,0)]
        all_possible_moves = []

        for direction in possible_directions:
            current_row = self.coord[0]
            current_col = self.coord[1]
            while True:
                current_row += direction[0]
                current_col += direction[1]
                if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                    break
                if self.board[current_row, current_col] == ' ':
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
                else:
                    #piece found, we will break from the search loop and move 
                    #to next direction unless we can capture
                    if self.color != self.board[current_row, current_col][0]:
                        all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
                    break
        return all_possible_moves
        pass
    
    #DONE
    def king(self):
        #print("KING - CHECKING ALL POSSIBLE MOVES")
        all_possible_moves = []
        #can move up, down, left, right, diagonally 1 space

        #setting bound for loop
        if self.coord[1] == 0:
            col_start = self.coord[1]
        else:
            col_start = self.coord[1] - 1

        if self.coord[1] == 7:
            col_end = self.coord[1]
        else:
            col_end = self.coord[1] + 1

        if self.coord[0] == 0:
            row_start = self.coord[0]
        else:
            row_start = self.coord[0] - 1
        
        if self.coord[0] == 7:
            row_end = self.coord[0]
        else:
            row_end = self.coord[0] + 1

        # print("Row start: ", row_start)
        # print("Row end: ", row_end)
        # print("Col start: ", col_start)
        # print("Col end: ", col_end)

        for i in range(row_start, row_end+1):
            for j in range(col_start, col_end+1):
                if self.board[i,j] == ' ':
                    #all_possible_moves.append(self.reverse_grid_dict[i,j])
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[i,j], None])
                else:
                    #check if we can capture
                    if self.color != self.board[i,j][0]:
                        all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[i,j], None])
        
        return all_possible_moves
        
        pass
    
    #DONE
    def zombie(self):
        possible_directions = [(-1,0), (1,0), (0,1), (0,-1)]
        all_possible_moves = []
        for direction in possible_directions:
            current_row = self.coord[0] + direction[0]
            current_col = self.coord[1] + direction[1]
            if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                continue
            if self.board[current_row, current_col] == ' ':
                all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
            else:
                #check if we can capture
                if self.color != self.board[current_row, current_col][0]:
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
        return all_possible_moves
        pass

    #DONE
    def bishop(self):
        #bishop can move diagonally in all directions but not up, down, left, right
        possible_directions= [(1,1), (1,-1), (-1,1), (-1,-1)]
        all_possible_moves = []
        for direction in possible_directions:
            current_row = self.coord[0]
            current_col = self.coord[1]
            while True:
                current_row += direction[0]
                current_col += direction[1]
                if current_row < 0 or current_row > 7 or current_col < 0 or current_col > 7:
                    break
                if self.board[current_row, current_col] == ' ':
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
                else:
                    #check if we can capture
                    if self.color != self.board[current_row, current_col][0]:
                        all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row, current_col], None])
                    break
        return all_possible_moves
        pass

    #DONE
    def rook(self):
        all_possible_moves = []
        #can move up, down, left, right

        #check left:
        
        if self.position[0] == 'a':
            pass
        else:
          #print("ROOK - CHECKING LEFT")
            #this will be the second tuple number that can be directly used in the board columns
            current_col = self.coord[1]
          
            counter = 1

            for i in range(current_col):
            
                if self.board[self.coord[0], current_col-counter] == ' ':
                    #print("Empty space")
                    #all_possible_moves.append(self.reverse_grid_dict[self.coord[0], current_col-counter])
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[self.coord[0], current_col-counter], None])
                else:
                  #print("Piece found - We cannot move in left anymore")
                  #check if we can capture
                    if self.color != self.board[self.coord[0], current_col-counter][0]:
                        all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[self.coord[0], current_col-counter], None])
                    break
                counter += 1
            

        #check right:
        
        if self.position[0] != 'h':
          #print("ROOK - CHECKING RIGHT")
            current_col = self.coord[1]
            counter = 1
         

            for i in range(7-current_col):               

                if self.board[self.coord[0], current_col+counter] == ' ':
                    #print("Empty space")
                    #all_possible_moves.append(self.reverse_grid_dict[self.coord[0], current_col+counter])
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[self.coord[0], current_col+counter], None])
                else:
                    #print("Piece found - We cannot move right any more")
                    #check if we can capture
                    if self.color != self.board[self.coord[0], current_col+counter][0]:
                        all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[self.coord[0], current_col+counter], None])
                    break
                counter += 1

        #check up:
        if self.position[1] != '8':
          #print("ROOK - CHECKING UP")
            current_row = self.coord[0]
            counter = 1

            for i in range(current_row-counter):
                if self.board[current_row-counter, self.coord[1]] == ' ':
                    #print("Empty space")
                    #all_possible_moves.append(self.reverse_grid_dict[current_row-counter, self.coord[1]])
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row-counter, current_col], None])
                else:
                    #check if we can capture
                    if self.color != self.board[current_row-counter, self.coord[1]][0]:
                        all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row-counter, current_col], None])
                    break
                counter += 1

        #check down:
        if self.position[1] != '1':
          #print("ROOK - CHECKING DOWN")
            current_row = self.coord[0]
            counter = 1

            for i in range(7-current_row):
                if self.board[current_row+counter, self.coord[1]] == ' ':
                    #print("Empty space")
                    #all_possible_moves.append(self.reverse_grid_dict[current_row+counter, self.coord[1]])
                    all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row+counter, current_col], None])
                    
                else:
                    #print("Piece found - We cannot move down anymore")
                    #check if we can capture
                    if self.color != self.board[current_row+counter, self.coord[1]][0]:
                        all_possible_moves.append([self.reverse_grid_dict[self.coord[0], self.coord[1]], f"{self.color}{self.piece}", self.reverse_grid_dict[current_row+counter, current_col], None])
                    break
                counter += 1

        return all_possible_moves
          
