import pygame
import warnings
from pawnclass import Pawn
from bishopclass import Bishop
from serpentclass import Serpent
from kingclass import King
from queenclass import Queen
from empressclass import GrandEmpress
from boardclass import Board


class BBApp(object):
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((1000, 900))
        pygame.display.set_caption("Chess Game")
        self.__board = Board()


    def main(self, bgcol, colours, pieceset):
        # main function
        pygame.init()
        pygame.display.set_caption('Two-Player Pygame Chess!')
        timer = pygame.time.Clock()
        fps = 60

        # 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected

        valid_moves = []
        

        warnings.filterwarnings("ignore", category=RuntimeWarning)
        black_queen = pygame.image.load('Assets/'+str(pieceset)+'/queen_black.png').convert_alpha()
        black_king = pygame.image.load('Assets/'+str(pieceset)+'/king_black.png').convert_alpha()
        black_empress = pygame.image.load('Assets/GrandEmpressBlack.png').convert_alpha()
        black_bishop = pygame.image.load('Assets/'+str(pieceset)+'/bishop_black.png').convert_alpha()
        black_serpent = pygame.image.load('Assets/BlackSerpent.png').convert_alpha()
        black_pawn = pygame.image.load('Assets/'+str(pieceset)+'/pawn_black.png').convert_alpha()
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        white_queen = pygame.image.load('Assets/'+str(pieceset)+'/queen_white.png').convert_alpha()
        white_king = pygame.image.load('Assets/'+str(pieceset)+'/king_white.png').convert_alpha()
        white_empress = pygame.image.load('Assets/GrandEmpressWhite.png').convert_alpha()
        white_bishop = pygame.image.load('Assets/'+str(pieceset)+'/bishop_white.png').convert_alpha()
        white_serpent = pygame.image.load('Assets/WhiteSerpent.png').convert_alpha()
        white_pawn = pygame.image.load('Assets/'+str(pieceset)+'/pawn_white.png').convert_alpha()
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        
        self.__board._setImages(black_queen, black_king, black_empress, black_bishop, black_serpent, black_pawn, white_queen, white_king, white_empress, white_bishop, white_serpent, white_pawn)
        game_over = False
        # main game loop
        black_options, black_poison_options = self.__board._check_options(self.__board._black_pieces, self.__board._black_locations, 'black') # Fetches the legal moves for black
        white_options, white_poison_options = self.__board._check_options(self.__board._white_pieces, self.__board._white_locations, 'white') # Fetches the legal moves for white
        

        run = True # Start of the game loop. Setting this to False will end the game loop
        serpent_selected = False
        while run:
            timer.tick(fps)
            if self.__board._counter < 30:
                self.__board._counter += 1
            else:
                self.__board._counter = 0
            self.__screen.fill(bgcol) # fill the screen
            self.__board._draw_board(self.__screen, colours[0], colours[1]) # draw the board
            self.__board._draw_pieces(self.__screen, pieceset) # draw the pieces
            if not game_over:
                self.__board._white_promote, self.__board._black_promote, self.__board._promo_index = self.__board._check_promotion() #Check if a pawn has reach the final ranks for black or white at the start of each loop. 
                if self.__board._white_promote or self.__board._black_promote: # If there is a pawn that has reach the final ranks
                    self.__board._draw_promotion(self.__screen) # Draw the promotion
                    self.__board._check_promo_select() # Select the piece that the pawn should promote to. 
                    
            if self.__board._selection != 100: # If the game is not over
                valid_moves = self.__board._check_valid_moves(white_options, black_options) # Check all of the legal moves
                self.__board._draw_valid(self.__screen, valid_moves) # Draw the valid moves that are returned from the list. 

            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False # Cross in the top right corner of the screen has been clicked indicating that the user no longer wants to play. 
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over: # Checks for the piece selected. 
                    x_coord = event.pos[0] // 100 # x coordinate of mouse press
                    y_coord = event.pos[1] // 100 # y coordinate of mouse press
                    
                    click_coords = (x_coord, y_coord) # coordinates of mouse click
                    
                    if self.__board._turn_step <= 1: # White's turn

                            
                        if click_coords in self.__board._white_locations: #If a white piece has been selected. 
                            self.__board._selection = self.__board._white_locations.index(click_coords) #Find the piece.
                            if self.__board._turn_step == 0: 
                                self.__board._turn_step = 1 # Change state from select piece to select location for the piece. 

                        if click_coords in valid_moves and self.__board._selection != 100: # If the move is legal
                            self.__board._white_locations[self.__board._selection] = click_coords # Make the move.
                            
                            
                            if click_coords in self.__board._black_locations: # If the second mouse click is legal and the square it is being moved to has a black piece on it.
                                white_piece = self.__board._white_locations.index(click_coords)   # work out what the white piece is
                                
                                if self.__board._white_pieces[white_piece] == "serpent": # has the serpent piece been selected? 
                                    serpent_selected = True  # flag variable to indicate that the serpent has been selected. 
                                    if serpent_selected == True:
                                        if click_coords in white_poison_options:  # There is an enemy piece on 
                                            neighbouring_squares = []
                                        
                                        # All of these different shifts are from black's perspective. If it is from white's perspective, it would be the complete opposite as I have chosen to implement the board from the black perspective
                                        # So you are looking at the board from the perspective of the person playing with the black pieces.
                                        
                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1] <= 7 and (click_coords[0]+1, click_coords[1]) in self.__board._black_locations: # One square to the right of click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]))
                                                
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1] <= 7 and (click_coords[0]-1, click_coords[1]) in self.__board._black_locations: # One square to the left of click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))
                                            
                                            if 0 <= click_coords[0] <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0],click_coords[1]+1) in self.__board._black_locations:  # One square up from click_coords
                                                neighbouring_squares.append((click_coords[0], click_coords[1]+1))
                                                
                                            if 0 <= click_coords[0] <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0], click_coords[1]-1) in self.__board._black_locations:  # One square down from click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))
                                            
                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0]+1, click_coords[1]+1) in self.__board._black_locations : #Diagonal top right from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]+1))
                                            
                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0]+1, click_coords[1]-1) in self.__board._black_locations: # Diagonal bottom right from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]-1))
                                            
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0]-1, click_coords[1]+1) in self.__board._black_locations: # Diagonal top left from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]))
                                                
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0]-1, click_coords[1]-1) in self.__board._black_locations: #Diagonal bottom left from click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))
                                        


                                            empress_nearby = False
                                            for square in neighbouring_squares:
                                                if square in self.__board._black_locations:
                                                    piece_index = self.__board._black_locations.index(square)
                                                    if self.__board._black_pieces[piece_index] == "empress":
                                                        empress_nearby = True
                                                        break
                                            
                                            if empress_nearby:
                                            # Remove white serpent and empress, update lists
                                                white_piece = self.__board._white_locations.index(self.__board._white_locations[self.__board._selection])
                                                empress_index = self.__board._black_locations.index(square)

                                                self.__board._white_pieces.pop(white_piece)
                                                self.__board._white_locations.pop(white_piece)

                                                self.__board._black_pieces.pop(empress_index)
                                                self.__board._black_locations.pop(empress_index)
                                            else:
                                                self.__board._black_pieces.pop(black_piece) # remove the piece from the board
                                                self.__board._black_locations.pop(black_piece) # Remove the location that the piece was on from the list of locations that black currently has pieces on.


                                else:
                                    black_piece = self.__board._black_locations.index(click_coords)

                                    if self.__board._black_pieces[black_piece] == 'king':  # If the piece is the king,
                                        piece_captured = King()
                                        self.__board._white_material_count += piece_captured._value

                                    elif self.__board._black_pieces[black_piece] == 'queen':  # If the piece is a queen,
                                        piece_captured = Queen()
                                        self.__board._white_material_count += piece_captured._value
                                    
                                    elif self.__board._black_pieces[black_piece] == 'bishop':  # If the piece is a queen,
                                        piece_captured = Bishop()
                                        self.__board._white_material_count += piece_captured._value
                                    
                                    elif self.__board._black_pieces[black_piece] == 'serpent':  # If the piece is a queen,
                                        piece_captured = Serpent()
                                        self.__board._white_material_count += piece_captured._value
                                    
                                    elif self.__board._black_pieces[black_piece] == 'empress':  # If the piece is a queen,
                                        piece_captured = GrandEmpress()
                                        self.__board._white_material_count += piece_captured._value
                                    
                                    else:
                                        piece_captured = Pawn()
                                        self.__board._white_material_count += piece_captured._value


                                    self.__board._black_pieces.pop(black_piece)  # remove the piece from the board
                                    self.__board._black_locations.pop(black_piece) # remove the piece from the list of black locations
                                

                            # Check the next set of legal moves in the new position.     
                            black_options, black_poison_options = self.__board._check_options(self.__board._black_pieces, self.__board._black_locations, 'black')
                            white_options , white_poison_options= self.__board._check_options(self.__board._white_pieces, self.__board._white_locations, 'white')
                            self.__board._turn_step = 2 # Black's turn now. 
                            self.__board._selection = 100
                            valid_moves = []

                    if self.__board._turn_step > 1:


                        if click_coords in self.__board._black_locations:
                            self.__board._selection = self.__board._black_locations.index(click_coords) #Find the piece.
                            if self.__board._turn_step == 2:
                                self.__board._turn_step = 3
                        
                        if click_coords in valid_moves and self.__board._selection != 100: # If the move is legal
                            self.__board._black_locations[self.__board._selection] = click_coords # Make the move.

                            if click_coords in self.__board._white_locations: # If the second mouse click is legal and the square it is being moved to has a black piece on it.
                                black_piece = self.__board._black_locations.index(click_coords)

                                if self.__board._black_pieces[black_piece] == "serpent":
                                    serpent_selected = True
                                    if serpent_selected == True:
                                        if click_coords in black_poison_options:
                                            neighbouring_squares = []

                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1] <= 7 and (click_coords[0]+1, click_coords[1]) in self.__board._white_locations: # One square to the right of click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]))
                                            
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1] <= 7 and (click_coords[0]-1, click_coords[1]) in self.__board._white_locations: # One square to the left of click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))
                                            
                                            if 0 <= click_coords[0] <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0],click_coords[1]+1) in self.__board._white_locations:  # One square up from click_coords
                                                neighbouring_squares.append((click_coords[0], click_coords[1]+1))
                                                
                                            if 0 <= click_coords[0] <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0], click_coords[1]-1) in self.__board._white_locations:  # One square down from click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))
                                            
                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0]+1, click_coords[1]+1) in self.__board._white_locations : #Diagonal top right from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]+1))
                                            
                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0]+1, click_coords[1]-1) in self.__board._white_locations: # Diagonal bottom right from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]-1))
                                            
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0]-1, click_coords[1]+1) in self.__board._white_locations: # Diagonal top left from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]))
                                                
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0]-1, click_coords[1]-1) in self.__board._white_locations: #Diagonal bottom left from click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))

                                            empress_nearby = False
                                            for square in neighbouring_squares:
                                                if square in self.__board._white_locations:
                                                    piece_index = self.__board._white_locations.index(square)
                                                    if self.__board._white_pieces[piece_index] == "empress":
                                                        empress_nearby = True
                                                        break
                                            
                                            if empress_nearby:
                                            # Remove black serpent and empress, update lists
                                                black_piece = self.__board._black_locations.index(self.__board._black_locations[self.__board._selection])
                                                empress_index = self.__board._white_locations.index(square)

                                                self.__board._black_pieces.pop(black_piece)
                                                self.__board._black_locations.pop(black_piece)

                                                self.__board._white_pieces.pop(empress_index)
                                                self.__board._white_locations.pop(empress_index)

                                            else:
                                                self.__board._white_pieces.pop(white_piece) # remove the piece from the board
                                                self.__board._white_locations.pop(white_piece) # Remove the location that the piece was on from the list of locations that black currently has pieces on.


                                else:
                                    white_piece = self.__board._white_locations.index(click_coords)

                                    if self.__board._white_pieces[white_piece] == 'king':  # If the piece is the king,
                                        piece_captured = King()
                                        self.__board._black_material_count += piece_captured._value

                                    elif self.__board._white_pieces[white_piece] == 'queen':  # If the piece is a queen,
                                        piece_captured = Queen()
                                        self.__board._black_material_count += piece_captured._value
                                    
                                    elif self.__board._black_pieces[black_piece] == 'bishop':  # If the piece is a bishop,
                                        piece_captured = Bishop()
                                        self.__board._black_material_count += piece_captured._value
                                    
                                    elif self.__board._black_pieces[black_piece] == 'serpent':  # If the piece is a serpent,
                                        piece_captured = Serpent()
                                        self.__board._black_material_count += piece_captured._value
                                    
                                    elif self.__board._black_pieces[black_piece] == 'empress':  # If the piece is an empress,
                                        piece_captured = GrandEmpress()
                                        self.__board._black_material_count += piece_captured._value
                                    
                                    else:                                                # The only other possible piece is a pawn 
                                        piece_captured = Pawn()
                                        self.__board._black_material_count += piece_captured._value


                                    self.__board._white_pieces.pop(white_piece)  # remove the piece from the board
                                    self.__board._white_locations.pop(white_piece) # remove the piece from the list of black locations                                              

                            black_options, black_poison_options = self.__board._check_options(self.__board._black_pieces, self.__board._black_locations, 'black')
                            white_options, white_posion_options = self.__board._check_options(self.__board._white_pieces, self.__board._white_locations, 'white')
                            self.__board._turn_step = 0
                            self.__board._selection = 100
                            valid_moves = []
                            
                if event.type == pygame.KEYDOWN and game_over: # If the user wants to play again after the game is over, they can press enter and the game will restart. 
                    if event.key == pygame.K_RETURN:
                        game_over = False
                        self.__board._initialise_game_variables()
                        valid_moves = []
                        black_options , black_poison_options = self.__board._check_options(self.__board._black_pieces, self.__board._black_locations, 'black')
                        white_options , white_poison_options = self.__board._check_options(self.__board._white_pieces, self.__board._white_locations, 'white')

        
            pygame.display.flip()
        pygame.quit()


        

        




