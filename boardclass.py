import pygame
import warnings
from pawnclass import Pawn
from bishopclass import Bishop
from serpentclass import Serpent
from kingclass import King
from queenclass import Queen
from empressclass import GrandEmpress


class Board(object):
    def __init__(self):
        self._turn_step = 0
        self._selection = 100
        self._white_promote = False
        self._black_promote = False
        self._black_promotions = ['bishop', 'serpent', 'empress', 'queen']
        self._white_promotions = ['bishop', 'serpent', 'empress', 'queen']
        self._promo_index = 100
        # check variables/ flashing counter
        self._counter = 0
        self._white_pieces = ['empress', 'serpent', 'bishop', 'king', 'queen', 'bishop', 'serpent', 'empress',
                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        
        self._black_pieces = ['empress', 'serpent', 'bishop', 'king', 'queen', 'bishop', 'serpent', 'empress',
                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        
        self._piece_list = ['pawn', 'queen', 'king', 'serpent', 'empress', 'bishop']
        
        self._black_queen = None
        self._black_queen_small = None
        self._black_king = None
        self._black_king_small = None
        self._black_empress = None
        self._black_empress_small = None
        self._black_bishop = None
        self._black_bishop_small = None
        self._black_serpent = None
        self._black_serpent_small = None
        self._black_pawn = None
        self._black_pawn_small = None
        
        self._white_queen = None
        self._white_queen_small = None
        self._white_king = None
        self._white_king_small = None
        self._white_empress = None
        self._white_empress_small = None
        self._white_bishop = None
        self._white_bishop_small = None
        self._white_serpent = None
        self._white_serpent_small = None
        self._white_pawn = None
        self._white_pawn_small = None
        
        self._white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        self._black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                        (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        
        self._font = pygame.font.Font('freesansbold.ttf', 40)


        self._white_material_count = 0

        self._black_material_count = 0

    

    def _initialise_game_variables(self):
        self._white_pieces = ['empress', 'serpent', 'bishop', 'king', 'queen', 'bishop', 'serpent', 'empress',
                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self._white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)]
        self._black_pieces = ['empress', 'serpent', 'bishop', 'king', 'queen', 'bishop', 'serpent', 'empress',
                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self._black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                        (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6)]
        self._turn_step = 0
        self._selection = 100

    def _draw_board(self, screen, hex_colour1, hex_colour2):
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
                    pygame.draw.rect(screen, board_colour1, pygame.Rect(x, y, cell_size, cell_size))
                else:
                    pygame.draw.rect(screen, board_colour2, pygame.Rect(x, y, cell_size, cell_size))

        # Draw the border around the board
        pygame.draw.rect(screen, border_colour, pygame.Rect(0, 0, cell_size * col_count, cell_size * row_count), 5)





    def _work_out_offset(self, pieceset):
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


    def _draw_pieces(self, screen, pieceset):
        #This function is responsible for drawing the pieces on the board.  
        offset_x, offset_y = 0, 0

        offset_x, offset_y = self._work_out_offset(pieceset)

        for i, (pieces, locations, colour) in enumerate([(self._white_pieces, self._white_locations, 'red'), (self._black_pieces, self._black_locations, 'blue')]):
            for j, piece in enumerate(pieces):
                index = self._piece_list.index(piece)
                pawn_offset_x, pawn_offset_y = 10, 0  # Additional offset for pawn

                if piece == 'pawn':
                    screen.blit(self._white_pawn if colour == 'red' else self._black_pawn, (locations[j][0] * 100 + pawn_offset_x, locations[j][1] * 100 + pawn_offset_y))
                else:
                    screen.blit(self._white_images[index] if colour == 'red' else self._black_images[index], (locations[j][0] * 100 + offset_x, locations[j][1] * 100 + offset_y))

                # Draw selection rectangle
                if (self._turn_step < 2 and i == 0) or (self._turn_step >= 2 and i == 1):
                    if self._selection == j:
                        pygame.draw.rect(screen, colour, [locations[j][0] * 100 + 1, locations[j][1] * 100 + 1, 100, 100], 2)


    def _check_options(self, pieces, locations, turn):
        moves_list = []
        all_moves_list = []
        poisoned_list = []  # Initialize poisoned_list outside the loop
        for i in range(len(pieces)):
            location = locations[i]
            piece = pieces[i]
            if piece == 'pawn':
                pieceselect = Pawn()
                moves_list = pieceselect._check_pawn(location, turn, self._white_locations, self._black_locations)
            elif piece == 'empress':
                pieceselect = GrandEmpress()
                moves_list = pieceselect._check_empress(location, turn, self._white_locations, self._black_locations)
            elif piece == 'serpent':
                pieceselect = Serpent()
                moves_list, poisoned_list = pieceselect._check_serpent(location, turn, self._white_locations, self._black_locations)
            elif piece == 'bishop':
                pieceselect = Bishop()
                moves_list = pieceselect._check_bishop(location, turn, self._white_locations, self._black_locations)
            elif piece == 'queen':
                pieceselect = Queen()
                moves_list = pieceselect._check_queen(location, turn, self._white_locations, self._black_locations)
            elif piece == 'king':
                pieceselect = King()
                moves_list = pieceselect._check_king(location, turn, self._white_locations, self._black_locations)
            all_moves_list.append(moves_list)
        
        return all_moves_list, poisoned_list

    def _check_valid_moves(self, white_options, black_options):
        # check for valid moves for just selected piece
        if self._turn_step < 2:
            options_list = white_options
        else:
            options_list = black_options
        valid_options = options_list[self._selection]
        return valid_options


    def _draw_valid(self, screen, moves):
        # draw valid moves on screen
        if self._turn_step < 2:
            colour = 'red'
        else:
            colour = 'blue'
        for i in range(len(moves)):
            pygame.draw.circle(screen, colour, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)
    


    def _check_promotion(self):
        # This function is responsible for checking whether a white pawn has reached the eighth rank or a black pawn has reached the first rank. 
        pawn_indexes = []
        white_promotion = False
        black_promotion = False
        promote_index = 100
        for i in range(len(self._white_pieces)):
            if self._white_pieces[i] == 'pawn':
                pawn_indexes.append(i)
        for i in range(len(pawn_indexes)):
            if self._white_locations[pawn_indexes[i]][1] == 7:
                white_promotion = True
                promote_index = pawn_indexes[i]
        pawn_indexes = []
        for i in range(len(self._black_pieces)):
            if self._black_pieces[i] == 'pawn':
                pawn_indexes.append(i)
        for i in range(len(pawn_indexes)):
            if self._black_locations[pawn_indexes[i]][1] == 0:
                black_promotion = True
                promote_index = pawn_indexes[i]
        return white_promotion, black_promotion, promote_index


    def _draw_promotion(self, screen):
        # When a pawn reaches the eighth or first rank, a menu will be drawn upon completion of the move, asking the user to select a piece to promote the pawn to.
        pygame.draw.rect(screen, 'dark gray', [800, 0, 200, 420])
        if self._white_promote:
            colour = 'white'
            for i in range(len(self._white_promotions)):
                piece = self._white_promotions[i]
                index = self._piece_list.index(piece)
                screen.blit(self._white_images[index], (860, 5 + 100 * i))

        elif self._black_promote:
            colour = 'black'
            for i in range(len(self._black_promotions)):
                piece = self._black_promotions[i]
                index = self._piece_list.index(piece)
                screen.blit(self._black_images[index], (860, 5 + 100 * i))
            pygame.draw.rect(screen, colour, [800, 0, 200, 420], 8)


    def _check_promo_select(self):
        # Work out what the user wants to promote to. 
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        x_pos = mouse_pos[0] // 100
        y_pos = mouse_pos[1] // 100

        # Check if the promotion index is not None and the mouse position is within the promotion area
        if self._promo_index is not None and y_pos < 4 and left_click and x_pos >= 8:
            # Check if it's a white promotion and the indices are within bounds
            if self._white_promote and 0 <= self._promo_index < len(self._white_pieces) and 0 <= y_pos < len(self._white_promotions):
                self._white_pieces[self._promo_index] = self._white_promotions[y_pos]
            # Check if it's a black promotion and the indices are within bounds
            elif self._black_promote and 0 <= self._promo_index < len(self._black_pieces) and 0 <= y_pos < len(self._black_promotions):
                self._black_pieces[self._promo_index] = self._black_promotions[y_pos]
    
    def _setImages(self, black_queen, black_king, black_empress, black_bishop, black_serpent, black_pawn, white_queen, white_king, white_empress, white_bishop, white_serpent, white_pawn):
        # This function is responsible for initializing the images required as part of the graphical elements to my game. 
        self._black_serpent = pygame.transform.scale(black_serpent, (95, 95))
        self._black_serpent_small = pygame.transform.scale(black_serpent, (45, 45))
        self._black_empress = pygame.transform.scale(black_empress, (100, 100))
        self._black_empress_small = pygame.transform.scale(black_empress, (45, 45))
        self._white_serpent = pygame.transform.scale(white_serpent, (100, 100))
        self._white_serpent_small = pygame.transform.scale(white_serpent, (45, 45))
        self._white_empress = pygame.transform.scale(white_empress, (100, 100))
        self._white_empress_small = pygame.transform.scale(white_empress, (45, 45))
        warnings.filterwarnings("ignore", category=RuntimeWarning)   # i kept getting a libpng error upon importing the images and saw that this was the best way to suppress it. 

        self._black_queen = pygame.transform.scale(black_queen, (100, 100))
        self._black_queen_small = pygame.transform.scale(black_queen, (45, 45))
        self._black_king = pygame.transform.scale(black_king, (100, 100))
        self._black_king_small = pygame.transform.scale(black_king, (45, 45))
        self._black_bishop = pygame.transform.scale(black_bishop, (95, 95))
        self._black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
        self._black_pawn = pygame.transform.scale(black_pawn, (100, 100))
        self._black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        
        self._white_queen = pygame.transform.scale(white_queen, (100, 100))
        self._white_queen_small = pygame.transform.scale(white_queen, (45, 45))
        self._white_king = pygame.transform.scale(white_king, (100, 100))
        self._white_king_small = pygame.transform.scale(white_king, (45, 45))
        self._white_bishop = pygame.transform.scale(white_bishop, (100, 100))
        self._white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
        self._white_pawn = pygame.transform.scale(white_pawn, (100, 100))
        self._white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        self._white_images = [self._white_pawn, self._white_queen, self._white_king, self._white_serpent, self._white_empress, self._white_bishop]
        self._small_white_images = [self._white_pawn_small, self._white_queen_small, self._white_king_small, self._white_serpent_small, self._white_empress_small, self._white_bishop_small]
        self._black_images = [self._black_pawn, self._black_queen, self._black_king, self._black_serpent, self._black_empress, self._black_bishop]
        self._small_black_images = [self._black_pawn_small, self._black_queen_small, self._black_king_small, self._black_serpent_small, self._black_empress_small, self._black_bishop_small]
