import pygame
import time
import warnings
from piececlass import Piece
from pawnclass import Pawn
from bishopclass import Bishop
from queenclass import Queen
from kingclass import King
from empressclass import GrandEmpress
from serpentclass import Serpent

class ColourError(Exception): #Exception class to catch any exceptions that happen when the background colour is being selected. 
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class BBApp(object):
    # Main app
    def __init__(self):
        pygame.init()
        self.__WIDTH = 1000
        self.__HEIGHT = 900
        self.__screen = pygame.display.set_mode([self.__WIDTH, self.__HEIGHT])
        self.__font = pygame.font.Font('freesansbold.ttf', 20)
        self.__mediumfont = pygame.font.Font('freesansbold.ttf', 40)
        self.__bigfont = pygame.font.Font('freesansbold.ttf', 50)
        self.__turn_step = 0
        self.__selection = 100
        self.__white_promote = False
        self.__black_promote = False
        self.__black_promotions = ['bishop', 'serpent', 'empress', 'queen']
        self.__white_promotions = ['bishop', 'serpent', 'empress', 'queen']
        self.__promo_index = 100
        # check variables/ flashing counter
        self.__counter = 0
        self.__white_pieces = ['empress', 'serpent', 'bishop', 'king', 'queen', 'bishop', 'serpent', 'empress',
                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        
        self.__black_pieces = ['empress', 'serpent', 'bishop', 'king', 'queen', 'bishop', 'serpent', 'empress',
                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        
        self.__piece_list = ['pawn', 'queen', 'king', 'serpent', 'empress', 'bishop']
        
        self.__black_queen = None
        self.__black_queen_small = None
        self.__black_king = None
        self.__black_king_small = None
        self.__black_empress = None
        self.__black_empress_small = None
        self.__black_bishop = None
        self.__black_bishop_small = None
        self.__black_serpent = None
        self.__black_serpent_small = None
        self.__black_pawn = None
        self.__black_pawn_small = None
        
        self.__white_queen = None
        self.__white_queen_small = None
        self.__white_king = None
        self.__white_king_small = None
        self.__white_empress = None
        self.__white_empress_small = None
        self.__white_bishop = None
        self.__white_bishop_small = None
        self.__white_serpent = None
        self.__white_serpent_small = None
        self.__white_pawn = None
        self.__white_pawn_small = None
        
        self.__white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        self.__black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                        (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        
        self.__white_material_count = 0

        self.__black_material_count = 0
                
    
    def __setImages(self, black_queen, black_king, black_empress, black_bishop, black_serpent, black_pawn, white_queen, white_king, white_empress, white_bishop, white_serpent, white_pawn):
        # This function is responsible for initializing the images required as part of the graphical elements to my game. 
        self.__black_serpent = pygame.transform.scale(black_serpent, (95, 95))
        self.__black_serpent_small = pygame.transform.scale(black_serpent, (45, 45))
        self.__black_empress = pygame.transform.scale(black_empress, (100, 100))
        self.__black_empress_small = pygame.transform.scale(black_empress, (45, 45))
        self.__white_serpent = pygame.transform.scale(white_serpent, (100, 100))
        self.__white_serpent_small = pygame.transform.scale(white_serpent, (45, 45))
        self.__white_empress = pygame.transform.scale(white_empress, (100, 100))
        self.__white_empress_small = pygame.transform.scale(white_empress, (45, 45))
        warnings.filterwarnings("ignore", category=RuntimeWarning)   # i kept getting a libpng error upon importing the images and saw that this was the best way to suppress it. 

        self.__black_queen = pygame.transform.scale(black_queen, (100, 100))
        self.__black_queen_small = pygame.transform.scale(black_queen, (45, 45))
        self.__black_king = pygame.transform.scale(black_king, (100, 100))
        self.__black_king_small = pygame.transform.scale(black_king, (45, 45))
        self.__black_bishop = pygame.transform.scale(black_bishop, (95, 95))
        self.__black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
        self.__black_pawn = pygame.transform.scale(black_pawn, (100, 100))
        self.__black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        
        self.__white_queen = pygame.transform.scale(white_queen, (100, 100))
        self.__white_queen_small = pygame.transform.scale(white_queen, (45, 45))
        self.__white_king = pygame.transform.scale(white_king, (100, 100))
        self.__white_king_small = pygame.transform.scale(white_king, (45, 45))
        self.__white_bishop = pygame.transform.scale(white_bishop, (100, 100))
        self.__white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
        self.__white_pawn = pygame.transform.scale(white_pawn, (100, 100))
        self.__white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        self.__white_images = [self.__white_pawn, self.__white_queen, self.__white_king, self.__white_serpent, self.__white_empress, self.__white_bishop]
        self.__small_white_images = [self.__white_pawn_small, self.__white_queen_small, self.__white_king_small, self.__white_serpent_small, self.__white_empress_small, self.__white_bishop_small]
        self.__black_images = [self.__black_pawn, self.__black_queen, self.__black_king, self.__black_serpent, self.__black_empress, self.__black_bishop]
        self.__small_black_images = [self.__black_pawn_small, self.__black_queen_small, self.__black_king_small, self.__black_serpent_small, self.__black_empress_small, self.__black_bishop_small]
        
            
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
        
        self.__setImages(black_queen, black_king, black_empress, black_bishop, black_serpent, black_pawn, white_queen, white_king, white_empress, white_bishop, white_serpent, white_pawn)
        winner = ''
        game_over = False
        # main game loop
        black_options, black_poison_options = self.__check_options(self.__black_pieces, self.__black_locations, 'black') # Fetches the legal moves for black
        white_options, white_poison_options = self.__check_options(self.__white_pieces, self.__white_locations, 'white') # Fetches the legal moves for white
        
        run = True # Start of the game loop. Setting this to False will end the game loop
        serpent_selected = False
        while run:
            timer.tick(fps)
            if self.__counter < 30:
                self.__counter += 1
            else:
                self.__counter = 0
            self.__screen.fill(bgcol) # fill the screen
            self.__draw_board(colours[0], colours[1]) # draw the board
            self.__draw_pieces(pieceset) # draw the pieces
            self.__draw_check(white_options, black_options) # draw the king in check if it is in check
            if not game_over:
                self.__white_promote, self.__black_promote, self.__promo_index = self.__check_promotion() #Check if a pawn has reach the final ranks for black or white at the start of each loop. 
                if self.__white_promote or self.__black_promote: # If there is a pawn that has reach the final ranks
                    self.__draw_promotion() # Draw the promotion
                    self.__check_promo_select() # Select the piece that the pawn should promote to. 
                    
            if self.__selection != 100: # If the game is not over
                valid_moves = self.__check_valid_moves(white_options, black_options) # Check all of the legal moves
                self.__draw_valid(valid_moves) # Draw the valid moves that are returned from the list. 
            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False # Cross in the top right corner of the screen has been clicked indicating that the user no longer wants to play. 
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over: # Checks for the piece selected. 
                    x_coord = event.pos[0] // 100 # x coordinate of mouse press
                    y_coord = event.pos[1] // 100 # y coordinate of mouse press
                    
                    click_coords = (x_coord, y_coord) # coordinates of mouse click
                    
                    if self.__turn_step <= 1: # White's turn
                        if click_coords == (8, 8) or click_coords == (9, 8): #Clicks on the forfeit button
                            winner = 'black'
                            
                        if click_coords in self.__white_locations: #If a white piece has been selected. 
                            self.__selection = self.__white_locations.index(click_coords) #Find the piece.
                            if self.__turn_step == 0: 
                                self.__turn_step = 1 # Change state from select piece to select location for the piece. 

                        if click_coords in valid_moves and self.__selection != 100: # If the move is legal
                            self.__white_locations[self.__selection] = click_coords # Make the move.
                            
                            
                            if click_coords in self.__black_locations: # If the second mouse click is legal and the square it is being moved to has a black piece on it.
                                white_piece = self.__white_locations.index(click_coords)   # work out what the white piece is
                                
                                if self.__white_pieces[white_piece] == "serpent": # has the serpent piece been selected? 
                                    serpent_selected = True  # flag variable to indicate that the serpent has been selected. 
                                    if serpent_selected == True:
                                        if click_coords in white_poison_options:  # There is an enemy piece on 
                                            neighbouring_squares = []
                                        
                                        # All of these different shifts are from black's perspective. If it is from white's perspective, it would be the complete opposite as I have chosen to implement the board from the black perspective
                                        # So you are looking at the board from the perspective of the person playing with the black pieces.
                                        
                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1] <= 7 and (click_coords[0]+1, click_coords[1]) in self.__black_locations: # One square to the right of click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]))
                                                
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1] <= 7 and (click_coords[0]-1, click_coords[1]) in self.__black_locations: # One square to the left of click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))
                                            
                                            if 0 <= click_coords[0] <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0],click_coords[1]+1) in self.__black_locations:  # One square up from click_coords
                                                neighbouring_squares.append((click_coords[0], click_coords[1]+1))
                                                
                                            if 0 <= click_coords[0] <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0], click_coords[1]-1) in self.__black_locations:  # One square down from click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))
                                            
                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0]+1, click_coords[1]+1) in self.__black_locations : #Diagonal top right from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]+1))
                                            
                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0]+1, click_coords[1]-1) in self.__black_locations: # Diagonal bottom right from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]-1))
                                            
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0]-1, click_coords[1]+1) in self.__black_locations: # Diagonal top left from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]))
                                                
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0]-1, click_coords[1]-1) in self.__black_locations: #Diagonal bottom left from click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))
                                        


                                            empress_nearby = False
                                            for square in neighbouring_squares:
                                                if square in self.__black_locations:
                                                    piece_index = self.__black_locations.index(square)
                                                    if self.__black_pieces[piece_index] == "empress":
                                                        empress_nearby = True
                                                        break
                                            
                                            if empress_nearby:
                                            # Remove white serpent and empress, update lists
                                                white_piece = self.__white_locations.index(self.__white_locations[self.__selection])
                                                empress_index = self.__black_locations.index(square)

                                                self.__white_pieces.pop(white_piece)
                                                self.__white_locations.pop(white_piece)

                                                self.__black_pieces.pop(empress_index)
                                                self.__black_locations.pop(empress_index)
                                            else:
                                                self.__black_pieces.pop(black_piece) # remove the piece from the board
                                                self.__black_locations.pop(black_piece) # Remove the location that the piece was on from the list of locations that black currently has pieces on.

                                                if self.__black_pieces[black_piece] == 'king': # If it is the king that has been captured, 
                                                    winner = 'white' 
                                else:
                                    black_piece = self.__black_locations.index(click_coords)

                                    if self.__black_pieces[black_piece] == 'king':  # If the piece is the king,
                                        piece_captured = King()
                                        self.__white_material_count += piece_captured._value

                                    elif self.__black_pieces[black_piece] == 'queen':  # If the piece is a queen,
                                        piece_captured = Queen()
                                        self.__white_material_count += piece_captured._value
                                    
                                    elif self.__black_pieces[black_piece] == 'bishop':  # If the piece is a queen,
                                        piece_captured = Bishop()
                                        self.__white_material_count += piece_captured._value
                                    
                                    elif self.__black_pieces[black_piece] == 'serpent':  # If the piece is a queen,
                                        piece_captured = Serpent()
                                        self.__white_material_count += piece_captured._value
                                    
                                    elif self.__black_pieces[black_piece] == 'empress':  # If the piece is a queen,
                                        piece_captured = GrandEmpress()
                                        self.__white_material_count += piece_captured._value
                                    
                                    else:
                                        piece_captured = Pawn()
                                        self.__white_material_count += piece_captured._value


                                    self.__black_pieces.pop(black_piece)  # remove the piece from the board
                                    self.__black_locations.pop(black_piece) # remove the piece from the list of black locations
                                

                            # Check the next set of legal moves in the new position.     
                            black_options, black_poison_options = self.__check_options(self.__black_pieces, self.__black_locations, 'black')
                            white_options , white_poison_options= self.__check_options(self.__white_pieces, self.__white_locations, 'white')
                            self.__turn_step = 2 # Black's turn now. 
                            self.__selection = 100
                            valid_moves = []

                    if self.__turn_step > 1:
                        if click_coords == (8,8) or click_coords == (9,8):
                            winner = 'white'

                        if click_coords in self.__black_locations:
                            self.__selection = self.__black_locations.index(click_coords) #Find the piece.
                            if self.__turn_step == 2:
                                self.__turn_step = 3
                        
                        if click_coords in valid_moves and self.__selection != 100: # If the move is legal
                            self.__black_locations[self.__selection] = click_coords # Make the move.

                            if click_coords in self.__white_locations: # If the second mouse click is legal and the square it is being moved to has a black piece on it.
                                black_piece = self.__black_locations.index(click_coords)

                                if self.__black_pieces[black_piece] == "serpent":
                                    serpent_selected = True
                                    if serpent_selected == True:
                                        if click_coords in black_poison_options:
                                            neighbouring_squares = []

                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1] <= 7 and (click_coords[0]+1, click_coords[1]) in self.__white_locations: # One square to the right of click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]))
                                            
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1] <= 7 and (click_coords[0]-1, click_coords[1]) in self.__white_locations: # One square to the left of click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))
                                            
                                            if 0 <= click_coords[0] <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0],click_coords[1]+1) in self.__white_locations:  # One square up from click_coords
                                                neighbouring_squares.append((click_coords[0], click_coords[1]+1))
                                                
                                            if 0 <= click_coords[0] <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0], click_coords[1]-1) in self.__white_locations:  # One square down from click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))
                                            
                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0]+1, click_coords[1]+1) in self.__white_locations : #Diagonal top right from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]+1))
                                            
                                            if 0 <= click_coords[0]+1 <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0]+1, click_coords[1]-1) in self.__white_locations: # Diagonal bottom right from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]-1))
                                            
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1]+1 <= 7 and (click_coords[0]-1, click_coords[1]+1) in self.__white_locations: # Diagonal top left from click_coords
                                                neighbouring_squares.append((click_coords[0]+1, click_coords[1]))
                                                
                                            if 0 <= click_coords[0]-1 <=7 and 0 <= click_coords[1]-1 <= 7 and (click_coords[0]-1, click_coords[1]-1) in self.__white_locations: #Diagonal bottom left from click_coords
                                                neighbouring_squares.append((click_coords[0]-1, click_coords[1]))

                                            empress_nearby = False
                                            for square in neighbouring_squares:
                                                if square in self.__white_locations:
                                                    piece_index = self.__white_locations.index(square)
                                                    if self.__white_pieces[piece_index] == "empress":
                                                        empress_nearby = True
                                                        break
                                            
                                            if empress_nearby:
                                            # Remove black serpent and empress, update lists
                                                black_piece = self.__black_locations.index(self.__black_locations[self.__selection])
                                                empress_index = self.__white_locations.index(square)

                                                self.__black_pieces.pop(black_piece)
                                                self.__black_locations.pop(black_piece)

                                                self.__white_pieces.pop(empress_index)
                                                self.__white_locations.pop(empress_index)

                                            else:
                                                self.__white_pieces.pop(white_piece) # remove the piece from the board
                                                self.__white_locations.pop(white_piece) # Remove the location that the piece was on from the list of locations that black currently has pieces on.

                                                if self.__white_pieces[white_piece] == 'king': # If it is the king that has been captured, 
                                                    winner = 'black' 
                                else:
                                    white_piece = self.__white_locations.index(click_coords)

                                    if self.__white_pieces[white_piece] == 'king':  # If the piece is the king,
                                        piece_captured = King()
                                        self.__black_material_count += piece_captured._value

                                    elif self.__white_pieces[white_piece] == 'queen':  # If the piece is a queen,
                                        piece_captured = Queen()
                                        self.__black_material_count += piece_captured._value
                                    
                                    elif self.__black_pieces[black_piece] == 'bishop':  # If the piece is a bishop,
                                        piece_captured = Bishop()
                                        self.__black_material_count += piece_captured._value
                                    
                                    elif self.__black_pieces[black_piece] == 'serpent':  # If the piece is a serpent,
                                        piece_captured = Serpent()
                                        self.__black_material_count += piece_captured._value
                                    
                                    elif self.__black_pieces[black_piece] == 'empress':  # If the piece is an empress,
                                        piece_captured = GrandEmpress()
                                        self.__black_material_count += piece_captured._value
                                    
                                    else:                                                # The only other possible piece is a pawn 
                                        piece_captured = Pawn()
                                        self.__black_material_count += piece_captured._value


                                    self.__white_pieces.pop(white_piece)  # remove the piece from the board
                                    self.__white_locations.pop(white_piece) # remove the piece from the list of black locations                                              

                            black_options, black_poison_options = self.__check_options(self.__black_pieces, self.__black_locations, 'black')
                            white_options, white_posion_options = self.__check_options(self.__white_pieces, self.__white_locations, 'white')
                            self.__turn_step = 0
                            self.__selection = 100
                            valid_moves = []
                            
                if event.type == pygame.KEYDOWN and game_over: # If the user wants to play again after the game is over, they can press enter and the game will restart. 
                    if event.key == pygame.K_RETURN:
                        game_over = False
                        winner = ''
                        self.__initialise_game_variables()
                        valid_moves = []
                        black_options , black_poison_options = self.check_options(self.__black_pieces, self.__black_locations, 'black')
                        white_options, white_poison_options = self.check_options(self.__white_pieces, self.__white_locations, 'white')

            if winner != '':
                game_over = True
                self.__draw_game_over(winner)
                print("White captured "+str(self.__white_material_count)+" points of material")
                print("Black captured "+str(self.__black_material_count)+" points of material")
            # The above three lines works out whether there is a winner for a given game state. If it is true, a message will display on the screen saying who the winner is and how you can go about restarting the game. 
            # Add here the return to the MainMenuScreen in the main.py file
            pygame.display.flip()
        pygame.quit()
    
    def __initialise_game_variables(self):
        self.__white_pieces = ['empress', 'serpent', 'bishop', 'king', 'queen', 'bishop', 'serpent', 'empress',
                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.__white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)]
        self.__black_pieces = ['empress', 'serpent', 'bishop', 'king', 'queen', 'bishop', 'serpent', 'empress',
                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.__black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                        (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6)]
        self.__turn_step = 0
        self.__selection = 100

    def __draw_board(self, hex_colour1, hex_colour2):
        row_count, col_count = 8,8
        cell_size = 100

        board_colour1 = pygame.Color(hex_colour1)
        board_colour2 = pygame.Color(hex_colour2)
        border_colour = pygame.Color('gold')

        for row in range(row_count):
            for col in range(col_count):
                x = col * cell_size
                y = row * cell_size

                # Alternate between two board colours
                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.__screen, board_colour1, pygame.Rect(x, y, cell_size, cell_size))
                else:
                    pygame.draw.rect(self.__screen, board_colour2, pygame.Rect(x, y, cell_size, cell_size))

        # Draw the border around the board
        pygame.draw.rect(self.__screen, border_colour, pygame.Rect(0, 0, cell_size * col_count, cell_size * row_count), 5)

        # Draw the status text based on self.__turn_step
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                    'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        self.__screen.blit(self.__bigfont.render(status_text[self.__turn_step], True, 'black'), (20, 820))


        # Draw the "FORFEIT" text
        self.__screen.blit(self.__mediumfont.render('FORFEIT', True, 'black'), (810, 830))



    def __work_out_offset(self, pieceset):
        # When drawing the pieces on the board, the images are coming in different sizes so when drawing them, we need to offset them so that they fit on each square.
        # This offsetting process is done for every pieceset. 
        if pieceset == "basic":
            offset_x, offset_y = 5, 7
        elif pieceset == "3D":
            offset_x, offset_y = 0, -8
        elif pieceset == "anarcandy":
            offset_x, offset_y = 15, 8
        elif pieceset == "merida":
            offset_x, offset_y = 3, 3
        
        return offset_x, offset_y

    def __draw_pieces(self, pieceset):
        #This function is responsible for drawing the pieces on the board.  
        offset_x, offset_y = 0, 0

        offset_x, offset_y = self.__work_out_offset(pieceset)

        for i, (pieces, locations, colour) in enumerate([(self.__white_pieces, self.__white_locations, 'red'), (self.__black_pieces, self.__black_locations, 'blue')]):
            for j, piece in enumerate(pieces):
                index = self.__piece_list.index(piece)
                pawn_offset_x, pawn_offset_y = 10, 0  # Additional offset for pawn

                if piece == 'pawn':
                    self.__screen.blit(self.__white_pawn if colour == 'red' else self.__black_pawn, (locations[j][0] * 100 + pawn_offset_x, locations[j][1] * 100 + pawn_offset_y))
                else:
                    self.__screen.blit(self.__white_images[index] if colour == 'red' else self.__black_images[index], (locations[j][0] * 100 + offset_x, locations[j][1] * 100 + offset_y))

                # Draw selection rectangle
                if (self.__turn_step < 2 and i == 0) or (self.__turn_step >= 2 and i == 1):
                    if self.__selection == j:
                        pygame.draw.rect(self.__screen, colour, [locations[j][0] * 100 + 1, locations[j][1] * 100 + 1, 100, 100], 2)



    # function to check all pieces valid options on the board
    def __check_options(self, pieces, locations, turn):
        moves_list = []
        all_moves_list = []
        poisoned_list = []  # Initialize poisoned_list outside the loop
        for i in range(len(pieces)):
            location = locations[i]
            piece = pieces[i]
            if piece == 'pawn':
                pieceselect = Pawn()
                moves_list = pieceselect._check_pawn(location, turn, self.__white_locations, self.__black_locations)
            elif piece == 'empress':
                pieceselect = GrandEmpress()
                moves_list = pieceselect._check_empress(location, turn, self.__white_locations, self.__black_locations)
            elif piece == 'serpent':
                pieceselect = Serpent()
                moves_list, poisoned_list = pieceselect._check_serpent(location, turn, self.__white_locations, self.__black_locations)
            elif piece == 'bishop':
                pieceselect = Bishop()
                moves_list = pieceselect._check_bishop(location, turn, self.__white_locations, self.__black_locations)
            elif piece == 'queen':
                pieceselect = Queen()
                moves_list = pieceselect._check_queen(location, turn, self.__white_locations, self.__black_locations)
            elif piece == 'king':
                pieceselect = King()
                moves_list = pieceselect._check_king(location, turn, self.__white_locations, self.__black_locations)
            all_moves_list.append(moves_list)
        
        return all_moves_list, poisoned_list



    
    def __check_valid_moves(self, white_options, black_options):
        # check for valid moves for just selected piece
        if self.__turn_step < 2:
            options_list = white_options
        else:
            options_list = black_options
        valid_options = options_list[self.__selection]
        return valid_options


    
    def __draw_valid(self, moves):
        # draw valid moves on screen
        if self.__turn_step < 2:
            colour = 'red'
        else:
            colour = 'blue'
        for i in range(len(moves)):
            pygame.draw.circle(self.__screen, colour, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)


    # draw a flashing square around king if in check
    def __draw_check(self, white_options, black_options):
        if self.__turn_step < 2:    # It's white's turn. 
            if 'king' in self.__white_pieces:  
                king_index = self.__white_pieces.index('king')
                king_location = self.__white_locations[king_index]   # We get the position of the king and see whether it is under attack
                for i in range(0, len(black_options)):      # We check whether the king is in one the squares that a black piece can move to. 
                    if king_location == black_options[i]:  # If the king is under attack. 
                        if self.__counter < 15:
                            pygame.draw.rect(self.__screen, 'dark red', [self.__white_locations[king_index][0] * 100 + 1, self.__white_locations[king_index][1] * 100 + 1, 100, 100], 5)  # Draw the flashing check around the king. 
        
        else:
            # Same algorithm as above albeit the pieces have swapped round i.e. we are checking for checks against the black king made by the white pieces. 
            if 'king' in self.__black_pieces:  
                king_index = self.__black_pieces.index('king')
                king_location = self.__black_locations[king_index]
                for i in range(len(white_options)):
                    if king_location in white_options[i]:
                        if self.__counter < 15:
                            pygame.draw.rect(self.__screen, 'dark blue', [self.__black_locations[king_index][0] * 100 + 1, self.__black_locations[king_index][1] * 100 + 1, 100, 100], 5)


    def __draw_game_over(self, winner):
    # When the game is over, this function will output the message saying who won and will also give the option to restart the game.
        pygame.draw.rect(self.__screen, 'black', [200, 200, 400, 70])
        if winner == "white" or winner == "black":
            self.__screen.blit(self.__mediumfont.render(f'{winner} won the game!', True, 'white'), (210, 210))
        else:
            self.__screen.blit(self.__mediumfont.render("Draw by stalemate!", True, 'white'), (210, 210))
        self.__screen.blit(self.__mediumfont.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))
    

    def __check_promotion(self):
        # This function is responsible for checking whether a white pawn has reached the eighth rank or a black pawn has reached the first rank. 
        pawn_indexes = []
        white_promotion = False
        black_promotion = False
        promote_index = 100
        for i in range(len(self.__white_pieces)):
            if self.__white_pieces[i] == 'pawn':
                pawn_indexes.append(i)
        for i in range(len(pawn_indexes)):
            if self.__white_locations[pawn_indexes[i]][1] == 7:
                white_promotion = True
                promote_index = pawn_indexes[i]
        pawn_indexes = []
        for i in range(len(self.__black_pieces)):
            if self.__black_pieces[i] == 'pawn':
                pawn_indexes.append(i)
        for i in range(len(pawn_indexes)):
            if self.__black_locations[pawn_indexes[i]][1] == 0:
                black_promotion = True
                promote_index = pawn_indexes[i]
        return white_promotion, black_promotion, promote_index


    def __draw_promotion(self):
        # When a pawn reaches the eighth or first rank, a menu will be drawn upon completion of the move, asking the user to select a piece to promote the pawn to.
        pygame.draw.rect(self.__screen, 'dark gray', [800, 0, 200, 420])
        if self.__white_promote:
            colour = 'white'
            for i in range(len(self.__white_promotions)):
                piece = self.__white_promotions[i]
                index = self.__piece_list.index(piece)
                self.__screen.blit(self.__white_images[index], (860, 5 + 100 * i))
        elif self.__black_promote:
            colour = 'black'
            for i in range(len(self.__black_promotions)):
                piece = self.__black_promotions[i]
                index = self.__piece_list.index(piece)
                self.__screen.blit(self.__black_images[index], (860, 5 + 100 * i))
            pygame.draw.rect(self.__screen, colour, [800, 0, 200, 420], 8)
    
    def __check_promo_select(self):
        # Work out what the user wants to promote to. 
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        x_pos = mouse_pos[0] // 100
        y_pos = mouse_pos[1] // 100

        # Check if the promotion index is not None and the mouse position is within the promotion area
        if self.__promo_index is not None and y_pos < 4 and left_click and x_pos >= 8:
            # Check if it's a white promotion and the indices are within bounds
            if self.__white_promote and 0 <= self.__promo_index < len(self.__white_pieces) and 0 <= y_pos < len(self.__white_promotions):
                self.__white_pieces[self.__promo_index] = self.__white_promotions[y_pos]
            # Check if it's a black promotion and the indices are within bounds
            elif self.__black_promote and 0 <= self.__promo_index < len(self.__black_pieces) and 0 <= y_pos < len(self.__black_promotions):
                self.__black_pieces[self.__promo_index] = self.__black_promotions[y_pos]

