#!/usr/bin/env python3
from SearchProblem2 import *
from Pieces import *
import sys
import copy
import ast
import json
import time

#tracks whos turn it is


class Board(SearchProblem):

    depth = 0

    def __init__( self, state=None, turn=None ):
        self.state = state
        self.turn = turn

        #print("Input board:")
        #print_board(state)
        #print("Turn: ", turn)


    def isCheckmate(pieces):
        #checks if king has been captured on either side        
        for p in pieces:
            if p.piece == 'K':
                #king still exists
                return False
        return True
         
    
    
    def edges(self):
        #print("Possible boards (edges):")
        new_boards = []

        #OG grid dict
        grid_dict = {
            'a1': (0,0),
            'a2': (0,1),
            'a3': (0,2),
            'a4': (0,3),
            'a5': (0,4),
            'a6': (0,5),
            'a7': (0,6),
            'a8': (0,7),
            'b1': (1,0),
            'b2': (1,1),
            'b3': (1,2),
            'b4': (1,3),
            'b5': (1,4),
            'b6': (1,5),
            'b7': (1,6),
            'b8': (1,7),
            'c1': (2,0),
            'c2': (2,1),
            'c3': (2,2),
            'c4': (2,3),
            'c5': (2,4),
            'c6': (2,5),
            'c7': (2,6),
            'c8': (2,7),
            'd1': (3,0),
            'd2': (3,1),
            'd3': (3,2),
            'd4': (3,3),
            'd5': (3,4),
            'd6': (3,5),
            'd7': (3,6),
            'd8': (3,7),
            'e1': (4,0),
            'e2': (4,1),
            'e3': (4,2),
            'e4': (4,3),
            'e5': (4,4),
            'e6': (4,5),
            'e7': (4,6),
            'e8': (4,7),
            'f1': (5,0),
            'f2': (5,1),
            'f3': (5,2),
            'f4': (5,3),
            'f5': (5,4),
            'f6': (5,5),
            'f7': (5,6),
            'f8': (5,7),
            'g1': (6,0),
            'g2': (6,1),
            'g3': (6,2),
            'g4': (6,3),
            'g5': (6,4),
            'g6': (6,5),
            'g7': (6,6),
            'g8': (6,7),
            'h1': (7,0),
            'h2': (7,1),
            'h3': (7,2),
            'h4': (7,3),
            'h5': (7,4),
            'h6': (7,5),
            'h7': (7,6),
            'h8': (7,7)
        }


        #reverse dictionary for getting the position of a piece
        reverse_grid_dict = {v: k for k, v in grid_dict.items()}

        all_white_pieces = []
        all_black_pieces = []

        
        #og grid positions:
        a8=(0,7); b8=(1,7); c8=(2,7); d8=(3,7); e8=(4,7); f8=(5,7); g8=(6,7); h8=(7,7);
        a7=(0,6); b7=(1,6); c7=(2,6); d7=(3,6); e7=(4,6); f7=(5,6); g7=(6,6); h7=(7,6);
        a6=(0,5); b6=(1,5); c6=(2,5); d6=(3,5); e6=(4,5); f6=(5,5); g6=(6,5); h6=(7,5);
        a5=(0,4); b5=(1,4); c5=(2,4); d5=(3,4); e5=(4,4); f5=(5,4); g5=(6,4); h5=(7,4);
        a4=(0,3); b4=(1,3); c4=(2,3); d4=(3,3); e4=(4,3); f4=(5,3); g4=(6,3); h4=(7,3);
        a3=(0,2); b3=(1,2); c3=(2,2); d3=(3,2); e3=(4,2); f3=(5,2); g3=(6,2); h3=(7,2);
        a2=(0,1); b2=(1,1); c2=(2,1); d2=(3,1); e2=(4,1); f2=(5,1); g2=(6,1); h2=(7,1);
        a1=(0,0); b1=(1,0); c1=(2,0); d1=(3,0); e1=(4,0); f1=(5,0); g1=(6,0); h1=(7,0);

        # if self.turn == "w":
        #     #print("White's turn")
        
        #get and store all pieces on the board
        #to see which need to be checked for edges
        for key in self.state:
            #print(self.state[key])
            if self.state[key] == ' ':
                continue

            else:
                piece = ChezzPiece(self.state[key][0], self.state[key][1], key, self.state, reverse_grid_dict)
                if self.state[key][0] == 'w':
                    all_white_pieces.append(piece)
                elif self.state[key][0] == 'b':
                    all_black_pieces.append(piece)
               

        all_possible_moves = []
     

        if self.turn == 'w':
            #print("White's turn")
            for piece in all_white_pieces:
                #print(piece)
                if piece.moves() != None:
                    all_possible_moves.extend(piece.moves())
        else:
            #print("Black's turn")
            for piece in all_black_pieces:
                #print(piece)
                if piece.moves() != None:
                    all_possible_moves.extend(piece.moves())

              
        
        # for move in all_possible_moves:
        #     print(move)

        #element in all_possible_moves is a list:
        #['OLD POSITION', 'PIECE', 'NEW POSITION']


        

        #format of move is ['OLD POSITION', 'PIECE', 'NEW POSITION']
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
        #print("Making new boards:")



        counter = 0
        edges = [] #returned back to alg
        for move in all_possible_moves:
            #print("MOVE:::: ", move)
         
            if move[2] != "Y" and move[2] != "Z":
                new_board = copy.deepcopy(self.state)
            
            new_board[grid_dict[move[0]]] = ' '
            if move[2] != "X" and move[2] != "Y" and move[2] != "Z" and move[2] != "XZ":
                new_board[grid_dict[move[2]]] = move[1]


            #contangion rule
            #print("Checking Contangion")
            zombied_pieces = []
            if self.turn == 'b':
                for piece in all_white_pieces:
                    if piece.piece == 'Z':
                        #print("POSITION OF ZOMBIE?: ", piece.coord)
                        
                        if move[1] != ' ' and move[1][1] == 'Z':
                            if move[2] != "X" and move[2] != "Y" and move[2] != "Z" and move[2] != "XZ":
                                zombied_pieces = piece.contangion(self.turn, grid_dict[move[2]])
                        else:
                            zombied_pieces = piece.contangion(self.turn, piece.coord)
                #[pos]
                for piece in zombied_pieces:
                   
                    position = grid_dict[piece]
                

                    #turn piece into zombie
                    new_board[position] = 'wZ'
            else:
                for piece in all_black_pieces:
                    if piece.piece == 'Z':
                        if move[1] != ' ' and move[1][1] == 'Z':
                            if move[2] != "X" and move[2] != "Y" and move[2] != "Z" and move[2] != "XZ":
                                zombied_pieces = piece.contangion(self.turn, grid_dict[move[2]])
                        else:
                            zombied_pieces = piece.contangion(self.turn, piece.coord)

                for piece in zombied_pieces:
               
                    position = grid_dict[piece]
                   

                    #turn piece into zombie
                    new_board[position] = 'bZ'
            


            #PROMOTION OF PEON
            #print("Checking Promotion")
            #print(move)
            if move[1] != ' ' and move[1][1] == 'P':
                if move[2] != 'X' and move[2] != 'Y' and move[2] != 'Z' and move[2] != 'XZ':
     
                    #print(move)

                    #check if reached end board
                    if move[1][0] == 'w' and move[2][1] == '8':
                        #promote to zombie
                    
                        new_board[grid_dict[move[2]]] = 'wZ'
                        #print("white PROMOTED!!!")
                    elif move[1][0] =='b' and move[2][1] == '1':
                        new_board[grid_dict[move[2]]] = 'bZ'
                        #print("black PROMOTED!!!")




            

            if move[2] != "X" and move[2] != "Y":
        
                #print("_________________________________________________")
                #print_board(new_board)
                #print("_________________________________________________")

                #turning board into file format
                new_board_file = f"{self.turn} {i1} {i2} {i3}\n"
                new_board_file += "{\n"

                for key in new_board:
                
                    if new_board[key] != ' ':
                        new_board_file += f"'{reverse_grid_dict[key]}': '{new_board[key]}'"
                        #add comma if not last element
                        if key != list(new_board.keys())[-1]:
                            new_board_file += ",\n"
                        else:
                            new_board_file += "\n"
                new_board_file += "}"
                #new_file = open(f"board.{counter:03}", "w")
                #new_file.write(new_board_file)
                #new_file.close()

                counter += 1
                edges.append(new_board)
        return edges
                

        
        # print(new_board_file)
        
    
    def is_target( self ):
        pass

    def print_board(board):
        for col_counter in range(7,-1,-1):
            row = ""
            for row_counter in range(8):
                row += f"| {board[(row_counter, col_counter)]:^3} "
            row += "|"
            print(row)
            print("_________________________________________________")

    def h1(self, board, turn, reverse_grid_dict, i1, i2):
        #print("NEW BOARD_______________")
        #print_board(board)


        if int(int(i2)-int(i1)) <= 1000:
            return 0


        #heurisitc score values:
        K = 1000000
        Q = 900
        P = 100
        N = 300
        B = 350
        R = 500
        Z = 400
        F = 600
        C = 550

        #stores pos of all players pieces
        piece_pos = []

        #heurisitc score of board
        h_score = 0
        #print("hscore before: ", h_score)
        
        #print("H turn: ", turn)
        #board = self.state
        for tile in board:
            #print(tile, ": ", board[tile])

            #1) store the position of all my pieces

            if board[tile] != " " and board[tile][0] == turn:
                piece_captured = board[tile][1]
                h_score += locals()[piece_captured]
            # elif board[tile] == " " and self.state[tile] != " ":
            #     if self.state[tile][0] == turn:
            #         piece_captured = self.state[tile][1]
            #         h_score -= locals()[piece_captured]

       
          


            #2) for each piece, 
                #check if i can capture
                #add to score
        #print(len(piece_pos))

        for coord in piece_pos:
            #print(coord)
            piece = ChezzPiece(turn, board[coord][1], coord, board, reverse_grid_dict)
                

                
            #print("Old value: ", self.state[coord])
            #CHECK EACH PIECE IF WE CAPTURED FROM LAST BOARD
            #if old pos is not blank or the same piece (didnt move)
            if self.state[coord] != " " and self.state[coord] != board[coord]:
                piece_captured = self.state[coord][1]
                
                h_score += locals()[piece_captured]
                # sys.stdout = open("/dev/tty", "w")
                # print("Piece captured1: ", piece_captured, f"({h_score})")

                #if piece is king we can break because we dont need to check more moves
                if piece_captured == 'K':
                    break
            
        
           

        #get edges
        new_board = Board(board,turn)
        edges = new_board.edges()

        # print("NEW EDGES:")

        #check if we put ourselves in a position to capture
       
        for edge in edges:
            edge_player_pieces = []
            edge_opp_pieces = []
            for tile in edge:
                if edge[tile] != " ":
                    if edge[tile][0] == turn:
                        edge_player_pieces.append(tile)
                    else:
                        edge_opp_pieces.append(tile)

        
           
            #now that we have the location of each piece, check captures
            #player potential captures
            for coord in edge_player_pieces:
               
                piece = ChezzPiece(turn, edge[coord][1], coord, edge, reverse_grid_dict)

                if new_board.state[coord] != " " and new_board.state[coord] != edge[coord]:
                    # print("Coord: ", coord)
                    # print("NB: ", new_board.state[coord])
                    # print("EDGE: ", edge[coord])
                    piece_captured = new_board.state[coord][1]
                
                    h_score += locals()[piece_captured]
                    # sys.stdout = open("/dev/tty", "w")
                    # print("Piece captured2: ", piece_captured, f"({h_score})")



        #opponent potential captures
        #print("oppp")
        if turn == 'w':
            opp_turn = 'b'
        else:
            opp_turn = 'w'

      
        opp_board = Board(board,opp_turn)
        edges = opp_board.edges()

        for edge in edges:
           
            edge_opp_pieces = []
            for tile in edge:
                if edge[tile] != " ":
                    if edge[tile][0] == opp_turn:
                        edge_opp_pieces.append(tile)

            for coord in edge_opp_pieces:
                    
                piece = ChezzPiece(opp_turn, edge[coord][1], coord, edge, reverse_grid_dict)

                if opp_board.state[coord] != " " and opp_board.state[coord] != edge[coord]:
                    piece_captured = opp_board.state[coord][1]
                    
                    h_score -= locals()[piece_captured]
                    #print("Piece captured: ", piece_captured, f"(-{h_score})")


        #print(h_score)

        # sys.stdout = open("/dev/tty", "w")
        # print("H: ", h_score)
        # print_board(board)
        # print("_____________________________")

        return h_score
    

    def move(self, turn, reverse_grid_dict, i1, i2, queue=None):
        #print("Turn: ", turn)
        
        queue = self.edges()
        #print("LEN OF QUEUE: ", len(queue))
        
        queue.sort(key=lambda board: self.h1(board, turn, reverse_grid_dict, i1, i2), reverse=True)
        #print("queue sorted")
        #do stuff
        best_move = queue.pop(0)
        # sys.stdout = open("/dev/tty", "w")
        # print_board(best_move)
      
        return best_move


def print_board(board):
    for col_counter in range(7,-1,-1):
        row = ""
        for row_counter in range(8):
            row += f"| {board[(row_counter, col_counter)]:^3} "
        row += "|"
        print(row)
        print("_________________________________________________")

 
#reads each line in input file and passes to gather_data
def read_file():

    #Fixed grid positions
    # a1=(7,0); b1=(7,1); c1=(7,2); d1=(7,3); e1=(7,4); f1=(7,5); g1=(7,6); h1=(7,7);
    # a2=(6,0); b2=(6,1); c2=(6,2); d2=(6,3); e2=(6,4); f2=(6,5); g2=(6,6); h2=(6,7);
    # a3=(5,0); b3=(5,1); c3=(5,2); d3=(5,3); e3=(5,4); f3=(5,5); g3=(5,6); h3=(5,7);
    # a4=(4,0); b4=(4,1); c4=(4,2); d4=(4,3); e4=(4,4); f4=(4,5); g4=(4,6); h4=(4,7);
    # a5=(3,0); b5=(3,1); c5=(3,2); d5=(3,3); e5=(3,4); f5=(3,5); g5=(3,6); h5=(3,7);
    # a6=(2,0); b6=(2,1); c6=(2,2); d6=(2,3); e6=(2,4); f6=(2,5); g6=(2,6); h6=(2,7);
    # a7=(1,0); b7=(1,1); c7=(1,2); d7=(1,3); e7=(1,4); f7=(1,5); g7=(1,6); h7=(1,7);
    # a8=(0,0); b8=(0,1); c8=(0,2); d8=(0,3); e8=(0,4); f8=(0,5); g8=(0,6); h8=(0,7);

    #OG grid positions:
    a8=(0,7); b8=(1,7); c8=(2,7); d8=(3,7); e8=(4,7); f8=(5,7); g8=(6,7); h8=(7,7);
    a7=(0,6); b7=(1,6); c7=(2,6); d7=(3,6); e7=(4,6); f7=(5,6); g7=(6,6); h7=(7,6);
    a6=(0,5); b6=(1,5); c6=(2,5); d6=(3,5); e6=(4,5); f6=(5,5); g6=(6,5); h6=(7,5);
    a5=(0,4); b5=(1,4); c5=(2,4); d5=(3,4); e5=(4,4); f5=(5,4); g5=(6,4); h5=(7,4);
    a4=(0,3); b4=(1,3); c4=(2,3); d4=(3,3); e4=(4,3); f4=(5,3); g4=(6,3); h4=(7,3);
    a3=(0,2); b3=(1,2); c3=(2,2); d3=(3,2); e3=(4,2); f3=(5,2); g3=(6,2); h3=(7,2);
    a2=(0,1); b2=(1,1); c2=(2,1); d2=(3,1); e2=(4,1); f2=(5,1); g2=(6,1); h2=(7,1);
    a1=(0,0); b1=(1,0); c1=(2,0); d1=(3,0); e1=(4,0); f1=(5,0); g1=(6,0); h1=(7,0);


    #read first line (get turn + ints)
    turn, i1, i2, i3 = sys.stdin.readline().split()


    #init board to be blank
    board = { (i,j): ' ' for i in range(0,8) for j in range(0,8) }


  


    #new_moves = ""
    new_moves_array = []

    new_moves_text = ""
    new_moves_dict = {}


    #gets the moves from the board file
    moves = sys.stdin.readlines()

    for line in moves:
        
        new_moves_array.append(line.strip())
        new_moves_text += line.strip()
        #print(line.strip()[0:2], line.strip()[4:8])            

        if line.strip() == "}":
            break

    #print("new_moves_text: ", new_moves_text)

    #new_moves is an array that holds each piece position of board
    new_moves = new_moves_text[1:-1].split(",")
        


    board.update( eval( new_moves_text ) )


    return board, turn, i1, i2, i3, new_moves

        


if __name__ == "__main__":
    #TODO: add check to see if board has been passed in command line
    #if no board passed, dont run
    state, turn, i1, i2, i3, new_moves = read_file()
    #print("Numbers: ", i1, i2, i3)

#OG grid dict
    grid_dict = {
            'a1': (0,0),
            'a2': (0,1),
            'a3': (0,2),
            'a4': (0,3),
            'a5': (0,4),
            'a6': (0,5),
            'a7': (0,6),
            'a8': (0,7),
            'b1': (1,0),
            'b2': (1,1),
            'b3': (1,2),
            'b4': (1,3),
            'b5': (1,4),
            'b6': (1,5),
            'b7': (1,6),
            'b8': (1,7),
            'c1': (2,0),
            'c2': (2,1),
            'c3': (2,2),
            'c4': (2,3),
            'c5': (2,4),
            'c6': (2,5),
            'c7': (2,6),
            'c8': (2,7),
            'd1': (3,0),
            'd2': (3,1),
            'd3': (3,2),
            'd4': (3,3),
            'd5': (3,4),
            'd6': (3,5),
            'd7': (3,6),
            'd8': (3,7),
            'e1': (4,0),
            'e2': (4,1),
            'e3': (4,2),
            'e4': (4,3),
            'e5': (4,4),
            'e6': (4,5),
            'e7': (4,6),
            'e8': (4,7),
            'f1': (5,0),
            'f2': (5,1),
            'f3': (5,2),
            'f4': (5,3),
            'f5': (5,4),
            'f6': (5,5),
            'f7': (5,6),
            'f8': (5,7),
            'g1': (6,0),
            'g2': (6,1),
            'g3': (6,2),
            'g4': (6,3),
            'g5': (6,4),
            'g6': (6,5),
            'g7': (6,6),
            'g8': (6,7),
            'h1': (7,0),
            'h2': (7,1),
            'h3': (7,2),
            'h4': (7,3),
            'h5': (7,4),
            'h6': (7,5),
            'h7': (7,6),
            'h8': (7,7)
    }


    #reverse dictionary for getting the position of a piece
    reverse_grid_dict = {v: k for k, v in grid_dict.items()}

    
    board = Board(state, turn)
    # sys.stdout = open("/dev/tty", "w")
    # print("STARTING BOARD:")
    # print_board(state)
    # print("______________________________________________")
    # print("______________________________________________")
    #print("Input board")
    #print_board(state)
    
    #board.edges()
    start = time.time()
    best_move = board.move(turn, reverse_grid_dict, i1, i2)
    end = time.time()

    # sys.stdout = open("/dev/tty", "w")
    
    total_time = int((end - start)*1000)

 
    #print("i1: ", int((float(i1) + total_time)*1000))


    i1 = int(i1) + total_time
    i3 = int(i3) + 1 #move played, so increment

  
    
    if turn == 'w':
        turn = 'b'
    elif turn == 'b':
        turn = 'w'

    # sys.stdout = open("/dev/tty", "w")
    # print_board(best_move)
  

    #output best_move to stdout in board format
    # sys.stdout = sys.__stdout__
    print(f"{turn} {i1} {i2} {i3}")
    print("{")

    for key in best_move:
        if best_move[key] != ' ':
            # Print the key without quotes and the value with single quotes
            print(f"  {reverse_grid_dict[key]}: '{best_move[key]}'", end="")
            # Add a comma if it's not the last element
            if key != list(best_move.keys())[-1]:
                print(",")
            else:
                print()

    print("}")



    

   






    