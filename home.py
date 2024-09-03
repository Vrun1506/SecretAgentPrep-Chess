import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import warnings
import pygame
import time
from bigbangchessapp import *
import sqlite3
from stack import *



class ColourError(Exception): #Exception class to catch any exceptions that happen when the background colour is being selected. 
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value




############################################################### - Two player chess game - #########################################################
def draw_board(hex_colour1, hex_colour2):
    # This function is responsible for drawing the board out. 
    #The two parameters that are inputted into the function are the two colours in hex form which are selected by the user from the getSquareColour() function.

    row_count, rank_count = 8, 8  # The number of rows and ranks on a chess board
    cell_size = 100

    board_colour1 = pygame.Color(hex_colour1)  #Initialise the first colour selected by the user. 
    board_colour2 = pygame.Color(hex_colour2)  # initialise the second colour selected by the user
    border_colour = pygame.Color('gold') # Border colour

    # Precompute rectangles for the entire board
    board_rects = [[pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size) for col in range(rank_count)] for row in range(row_count)]  # Initialising a rectangle for each square. 

    #Through using the rectangle to represent a square, we can in turn avoid creating a separate Square class. 

    # Draw the entire board with alternating colours using a single draw.rect call
    pygame.draw.rect(screen, border_colour, pygame.Rect(0, 0, cell_size * rank_count, cell_size * row_count), 5)
    for row in range(row_count):
        for col in range(rank_count):
            if (row + col) % 2 == 0:  # A simple algorithm which has binary results and so this can be used to draw the alternating colour pattern on the squares. 
                colour = board_colour1
            else:
                colour = board_colour2
            pygame.draw.rect(screen, colour, board_rects[row][col])


    # Draw the "FORFEIT" text
    screen.blit(medium_font.render('Resign', True, 'black'), (810, 830))   # Resign button
    if white_promote or black_promote:
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH - 200, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH - 200, 100], 5)
        screen.blit(big_font.render('Select Piece to Promote Pawn', True, 'black'), (20, 820))


def getSquareColour(colours_picked=None, count=0):
    #This is a customisable feature. This function gets two square colours of the user's choice and then returns them as a list. 
    if colours_picked is None:
        colours_picked = []

    colour_dict = {
        "cream": "#FFFACD",
        "orange": "#FFA500",      # The square colours are all stored in hex form so that they can be directly utilised to initialise the colours in the draw_board function. 
        "yellow": "#FFFF00",      # The key value for this dictionary is the colour that the user will input and the pair value is the corresponding hex code for that colour. 
        "green": "#008000",
        "light green": "#90EE90",
        "dark green": "#006400",
        "light blue": "#ADD8E6",
        "pink": "#FFC0CB",
        "purple": "#800080",
        "brown": "#A52A2A",
        "grey": "#808080",
        "white": "#FFFFFF"
    }

    if count < 2:   # The running condition that stops the function running more than twice. 
        valid = False 
        if count == 0:
            print("Please select a colour for the squares.\n")
        else:
            print("Please select a second colour for the squares")
        while not valid:
            sqcol = input(">").lower()
            if sqcol in colour_dict and sqcol not in colours_picked:    # two checks: the colour is present in the dictionary and that the colour hasn't already been picked. 
                valid = True
                colours_picked.append(sqcol)
            elif sqcol in colours_picked:
                print("You have already selected that colour. Please choose a different one.")
            
            elif sqcol == "black":
                print("You can't select that colour because you won't be able to see the black pieces on the board.")
            else:
                print("That colour is not available. Please choose from the available colours.")

        return getSquareColour(colours_picked, count + 1)  
    else: # base case - if the number of times that the function has been executed is greater than or equal to 3. After the function has been executed twice, we have satisfied the stopping condition
        hex_codes = [colour_dict[colour] for colour in colours_picked]   # The hex codes which are picked up are stored in a list and then returned.
        return hex_codes                    

def work_out_offset(pieceset):
    # When drawing the pieces on the board, the images are coming in different sizes so when drawing them, we need to offset them so that they fit on each square.
    # This offsetting process is done for every pieceset. 
    if pieceset == "basic":            # When each pieceset is selected, the offsetting will ensure that the images are positioned as closely to the centre as possible.
        offset_x, offset_y = 5, 7
    elif pieceset == "3D":
        offset_x, offset_y = 0, -8
    elif pieceset == "anarcandy":
        offset_x, offset_y = 15, 8
    elif pieceset == "merida":
        offset_x, offset_y = 3, 3
    
    return offset_x, offset_y

def draw_pieces(pieceset):
    #This function is responsible for drawing the pieces on the board.  
    offset_x, offset_y = 0, 0

    offset_x, offset_y = work_out_offset(pieceset)   # Get the offset values for the pieceset that has been selected. 

    for i, (pieces, locations, colour) in enumerate([(white_pieces, white_locations, 'red'), (black_pieces, black_locations, 'blue')]):
        for j, piece in enumerate(pieces):
            index = piece_list.index(piece)
            pawn_offset_x, pawn_offset_y = 10, 0  # Additional offset for pawn

            if piece == 'pawn':
                screen.blit(white_pawn if colour == 'red' else black_pawn, (locations[j][0] * 100 + pawn_offset_x, locations[j][1] * 100 + pawn_offset_y))    # Drawing the pawns. The red legal move highlights are associated with white which is why I have used the string 'red' to mean white. 
            else:
                screen.blit(white_images[index] if colour == 'red' else black_images[index], (locations[j][0] * 100 + offset_x, locations[j][1] * 100 + offset_y))  # Drawing the pieces. 

            # Draw selection rectangle
            if (turn_step < 2 and i == 0) or (turn_step >= 2 and i == 1):
                if selection == j:
                    pygame.draw.rect(screen, colour, [locations[j][0] * 100 + 1, locations[j][1] * 100 + 1, 100, 100], 2)


def check_options(pieces, locations, turn, castling_moves, check):
    #This function is responsible for fetching all of the legal moves in a given position. 
    # Initially there were global variables incorporated in the design, which came from the tutorial but I removed them and edited the functionality accordingly so as to incorporate better coding design. 
    all_moves_list = []
    new_castling_moves = castling_moves.copy()

    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]

        if piece == 'pawn':
            moves_list = check_pawn(location, turn)  # get the legal pawn moves. 
        elif piece == 'rook':
            moves_list = check_rook(location, turn) # get the legal rook moves.
        elif piece == 'knight':
            moves_list = check_knight(location, turn) # get the legal knight moves.
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn) # get the legal bishop moves.
        elif piece == 'queen':
            moves_list = check_queen(location, turn) # get the legal queen moves.
        elif piece == 'king':
            moves_list, new_castling_moves = check_king(location, turn, check) # get the legal king moves. store the castling moves as a separate list 

        all_moves_list.append(moves_list) # combine all of the moves 
    return all_moves_list, new_castling_moves


def get_colour_lists(colour):   # To determine in a certain turn, which colour is your own pieces and which side is your opponent's pieces. 
    # For example, if you have the white pieces, your own pieces will be white and the enemy pieces will be black. 

    if colour == 'white':
        return black_locations, white_locations
    else:
        return white_locations, black_locations


def check_king(position, colour, check):
    #This function is responsible for fetching all of the legal moves that a king piece can make. 
    #The tutorial I followed had global variables here but in order to demonstrate better coding style, I removed them from the code.
    moves_list = [] #Stores all of the legal king moves. 
    castle_moves, check = check_castling(check) #Gets all of the castling moves that a king piece can make


    enemies_list, friends_list = get_colour_lists(colour)

    for x_pos in [-1, 0, 1]:              # A king can move one square in any direction. This for loop focusses on the x position. 
        for y_pos in [-1, 0, 1]:          # This nested for loops looks at the y position
            if x_pos == y_pos == 0:       #If they are both equal to 0, the king makes no moves.
                pass

            target = (position[0] + x_pos, position[1] + y_pos)
            if 0 <= target[0] <= 7 and 0 <= target[1] <= 7 and target not in friends_list:  #Here, we make sure that the final end position the king ends up on is on the board (i.e. on a square with coordinates between 1 and 7 for both the x and y coordinates).
                moves_list.append(target)

    return moves_list, castle_moves 


def check_queen(position, colour):
    # This function is responsble for fetching the legal moves that can be made by a queen in a given position.
    # A queen simply combines the functionalities of a rook and a bishop so we can simply reuse those functions. 
    moves_list = check_bishop(position, colour)
    second_list = check_rook(position, colour)
    for i in range(len(second_list)):
        moves_list.append(second_list[i]) # Additing the legal rook moves into one list. 
    return moves_list


def check_bishop(position, colour):
    #This function is responsible for fetching the legal moves that can be made by a bishop in a given position. 
    #The bishop is able to move along the diagonals through as many squares as desired until there is a blockade in the diagonal that is being pursued. 

    moves_list = []
    directions = [(1, -1), (-1, -1), (1, 1), (-1, 1)]  #These are the basic direction vectors of the movement without any chain. 

    enemies_list, friends_list = get_colour_lists(colour)

    for x_pos, y_pos in directions:
        current_x, current_y = position  #Keeps track of starting position. 
        chain = 1
        keep_checking = True

        while keep_checking and 0 <= current_x + chain * x_pos <= 7 and 0 <= current_y + chain * y_pos <= 7: #Ensures that the chain stays on the board. 
            new_position = (current_x + chain * x_pos, current_y + chain * y_pos)  #The new position from moving in a certain direction. 

            if new_position not in friends_list: #Ensuring that our own pieces aren't already on that speciifc square. 
                moves_list.append(new_position)

                if new_position in enemies_list:
                    keep_checking = False # We have reached a 'blockade' position so we simply append the move. 

                chain += 1
            else:
                keep_checking = False

    return moves_list




def check_rook(position, colour):
    #This function is responsible for fetching all of the legal rook moves in a given position. 
    #The rook works in a very similar way to the bishop except that the rook moves horizontally or vertically. 

    moves_list = []

    enemies_list, friends_list = get_colour_lists(colour)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # down, up, right, left

    for x_pos, y_pos in directions:
        start_x, start_y = position
        chain = 1
        continue_checking = True

        while continue_checking and 0 <= start_x + chain * x_pos <= 7 and 0 <= start_y + chain * y_pos <= 7:  # The loop will continue to add the basc vectors in the direction list until one of the positions isn't present on the board. 
            new_position = (start_x + chain * x_pos, start_y + chain * y_pos)

            if new_position not in friends_list:
                moves_list.append(new_position)

                if new_position in enemies_list:
                    continue_checking = False  # We can stop checking for new positions as the file has been blockaded. 

                chain += 1
            else:
                continue_checking = False   # our own pieces are blocking our path. 

    return moves_list


def is_valid_square(x, y):
    # returns a Boolean value to indicate whether the square is valid
    return 0 <= x <= 7 and 0 <= y <= 7

def check_pawn(position, colour):
    moves_list = []
    if colour == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        # add en passant move checker
        if (position[0] + 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))

        # add en passant move checker
        if (position[0] + 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list



def check_knight(position, colour):
    # This function is responsible for fetching every legal move that can be made by a knight in a given position. 
    moves_list = []

    enemies_list, friends_list = get_colour_lists(colour)

    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for move in targets:
        target = (position[0] + move[0], position[1] + move[1])

        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)

    return moves_list



def get_options_list(white_options, black_options, turn_step):
    # Works out whose turn it is so that we don't have to work out the legal moves of both the black and the white pieces for a given turn. 
    return white_options if turn_step < 2 else black_options


def check_valid_moves(white_options, black_options, turn_step, selection):
    # check for valid moves for just selected piece
    options_list = get_options_list(white_options, black_options, turn_step)
    valid_options = options_list[selection]
    return valid_options


def determineColour(turn_step):
    # This is a simple function that works out the colour of the squares highlighter based off whose turn it is, which is signified by the turn_step variable. 
    colour = 'red' if turn_step < 2 else 'blue'

    return colour


def draw_valid(moves, turn_step):
    # After checking legality, we draw the moves on the board using this function. 
    colour = determineColour(turn_step)
    for i in range(len(moves)):
        pygame.draw.circle(screen, colour, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)


def determineCheckColour(turn_step):
    # We work out which king is in check. If it is the white king, it will have a red piece highlight. If it is the black king, it will have a blue piece highlight.
    # The highlights will flash to indicate that you are in check because I had problems with implementing an algorithm to draw the moves that either got out of the check, blocked the check or had the potential to capture the offending piece. 
    if turn_step < 2:  # White's king is in check
        colour = 'dark red'
    else:
        colour = 'dark blue' # Black's king is in check
    
    return colour



def draw_check(turn_step, counter):
    # This function will draw a flashing highlight around the king that is in check when appropriate. 
    king_index, king_location = None, None

    if turn_step < 2:  # If it's white's turn 
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            opponent_options = black_options
        else:       
            return False     # the king isn't in check so we just return back to the game. 
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            opponent_options = white_options
        else:
            return False

    for i in range(len(opponent_options)):
        if king_location in opponent_options[i]:
            if counter < 15:

                colour = determineCheckColour(turn_step)

                pygame.draw.rect(screen, colour, [king_location[0] * 100 + 1, king_location[1] * 100 + 1, 100, 100], 5)  
            return True

    return False   # We return False as a default if none of the other conditions are met. 


def draw_game_over(winner):
    # When the game is over, this function will output the message saying who won and will also give the option to restart the game.
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    if winner == "white" or winner == "black":
        screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    else:
        screen.blit(font.render("Draw by stalemate!", True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))



def check_en_passant(turn_step, old_coords, new_coords):
    # This function is responsible for checking whether en passant is legal or not.
    if turn_step <= 1:   # White's en passant
        index = white_locations.index(old_coords) # Get the old pawn position. 
        ep_coords = (new_coords[0], new_coords[1] - 1)  # Convert to the new pawn position after the move has been made and selected. 
        piece = white_pieces[index]
    else:
        index = black_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] + 1)
        piece = black_pieces[index]
    if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
        # if piece was pawn and moved two spaces, return EP coords as defined above
        pass
    else:
        ep_coords = (100, 100)   # Default values if none of the checks return as true (for example, when we have a piece that has been selected. )
    return ep_coords



def check_castling(check):
    # # king must not currently be in check, neither the rook nor king has moved previously, nothing between
    # and the king does not pass through or finish on an attacked piece
    # Store each valid castle move as [((king_coords), (rook_coords))]
    castle_moves = []
    rook_indexes = []
    rook_locations = []
    king_index = 0
    king_pos = (0, 0)

    # Determine if it's White's or Black's turn based on the turn step
    if turn_step > 1:   # White's turn
        # Iterate over White pieces to find rooks and the king
        for i in range(len(white_pieces)):
            if white_pieces[i] == 'rook':     # Finding whether a rook exists.
                rook_indexes.append(white_moved[i])
                rook_locations.append(white_locations[i])
            if white_pieces[i] == 'king':
                king_index = i
                king_pos = white_locations[i]
                
        # Check conditions for castling on White's side
        if not white_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]), (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    # Check if there are any pieces on the empty squares, or if the rook is moved, or if it's under attack
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in black_options or rook_indexes[i]:
                        castle = False
                # If all conditions are met, add the castle move to the list
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    else:
        # Iterate over Black pieces to find rooks and the king
        for i in range(len(black_pieces)):
            if black_pieces[i] == 'rook':
                rook_indexes.append(black_moved[i])
                rook_locations.append(black_locations[i])
            if black_pieces[i] == 'king':
                king_index = i
                king_pos = black_locations[i]

        # Check conditions for castling on Black's side
        if not black_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True

                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),(king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):

                    # Check if there are any pieces on the empty squares, or if the rook is moved, or if it's under attack
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in white_options or rook_indexes[i]:
                        castle = False
                # If all conditions are met, add the castle move to the list
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    return castle_moves, check



def draw_castling(turn_step, moves):
    # This function is responsible for drawing the castling move. 

    colour = determineColour(turn_step)

    for move in moves:
        king_x, king_y = move[0][0] * 100 + 50, move[0][1] * 100 + 70
        rook_x, rook_y = move[1][0] * 100 + 50, move[1][1] * 100 + 70

        king_center = (king_x, king_y)
        rook_center = (rook_x, rook_y)

        king_render_pos = (king_x - 20, king_y - 10)
        rook_render_pos = (rook_x - 20, rook_y - 10)

        pygame.draw.circle(screen, colour, king_center, 8)
        screen.blit(font.render('king', True, 'black'), king_render_pos)

        pygame.draw.circle(screen, colour, rook_center, 8)
        screen.blit(font.render('rook', True, 'black'), rook_render_pos)

        pygame.draw.line(screen, colour, king_center, rook_center, 2)



# add pawn promotion
def check_promotion():
    # This function is responsible for checking whether a white pawn has reached the eighth rank or a black pawn has reached the first rank. 
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = 100
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index


def draw_promotion():
    # When a pawn reaches the eighth or first rank, a menu will be drawn upon completion of the move, asking the user to select a piece to promote the pawn to. 
    pygame.draw.rect(screen, 'dark gray', [800, 0, 200, 420])
    
    colour = 'white' if white_promote else 'black'
    promotions = white_promotions if white_promote else black_promotions

    for i, piece in enumerate(promotions):
        index = piece_list.index(piece)
        piece_image = white_images[index] if colour == 'white' else black_images[index]
        screen.blit(piece_image, (860, 5 + 100 * i))

    pygame.draw.rect(screen, colour, [800, 0, 200, 420], 8)



def check_promo_select():
    # Work out what the user wants to promote to. 
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100

    # Check if the promotion index is not None and the mouse position is within the promotion area
    if promo_index is not None and y_pos < 4 and left_click and x_pos >= 8:
        # Check if it's a white promotion and the indices are within bounds
        if white_promote and 0 <= promo_index < len(white_pieces) and 0 <= y_pos < len(white_promotions):
            white_pieces[promo_index] = white_promotions[y_pos]
        # Check if it's a black promotion and the indices are within bounds
        elif black_promote and 0 <= promo_index < len(black_pieces) and 0 <= y_pos < len(black_promotions):
            black_pieces[promo_index] = black_promotions[y_pos]




def getBgCol():
    # Get the background colour that the user wants.
    # Like on lichess.org and chess.com, the background colour is customisable
    colours = ["red", "orange", "yellow", "green", "light green", "dark green", "blue", "light blue", "dark blue", "pink", "purple",  "brown", "grey", "white"]
    valid = False

    print("\nPlease select a background colour.")
    while valid == False:
        bgcol = input(">").lower()
        try:
            if bgcol not in colours:  # if a valid colour isn't entered
                raise ColourError("That colour is not available. These are the colours that are available:")
            valid = True

        except ColourError:
            print("Please enter a valid colour. You can't select black because you will not be able to see the captured pieces.")
    return bgcol

def selectPieceSet():
    # This function is responsible for getting the user to select a piece set. It is running recursively. 

    # Dictionary below deals with selecting a piece set. The key value is the number and the pair value is the folder name in which the assets are being stored. 
    piece_sets = {
    1: "basic",
    2: "merida",
    3: "3D",
    4: "anarcandy",
    }
    print("Select a piece set for your game.")
    print("These are your options:")
    for number, piece_set in piece_sets.items():
        print(f"{number}: {piece_set}")
        time.sleep(0.25) #Improved readability. 
    while True:
        try:
            selected_number = int(input(">"))
            if selected_number in piece_sets:
                selected_piece_set = piece_sets[selected_number]
                print("OK, "+str(selected_piece_set)+" has been selected.")
                return selected_piece_set
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:    #To deal with any rogue input values. 
            print("Please enter a valid integer between 1 and 4.")



################################################################ - UI Functions - #################################################################
class CreateAccountScreen(tk.Frame): #Inheritance and Polymorphism from the base class. 
    # This is the first screen that will be displayed to the user upon execution of the code. 
    def __init__(self, master=None):
        super().__init__(master, bg="black") #Overriding the default. 
        self.master = master
        self.grid(sticky="nsew")
        self.__create_widgets()

    def __create_widgets(self):
        # Create the "Create account" label with a bigger font
        create_account_label = tk.Label(self, text="Create account", font=("Arial", 36), fg="orange", bg="black")
        create_account_label.grid(row=1, pady=(5, 15), padx=(125, 50), columnspan=4)

        # Create the "Username:" label
        username_label = tk.Label(self, text="Username:", font=("Arial", 14), fg="white", bg="black")
        username_label.grid(row=2, column=0, sticky='e', padx=(3, 0), pady=(0, 3))

        # Create the input box to the right of the "Username" label with red text
        self.__username_input = tk.Entry(self, font=("Arial", 14), bg="dark blue", fg="red")
        self.__username_input.grid(row=2, column=1, padx=(0, 3), pady=(0, 3))

        # Bind the focus and focus-out events to change the background colour
        self.__username_input.bind("<FocusIn>", self.__on_entry_focus_username)
        self.__username_input.bind("<FocusOut>", self.__on_entry_focus_out_username)

        self.__password_label = tk.Label(self, text="Password:", font=("Arial", 14), fg="white", bg="black")
        self.__password_label.grid(row=3, column=0, sticky='e', padx=(3, 0), pady=(0, 3))

        # Password Entry
        self.__password_input = tk.Entry(self, font=("Arial", 14), bg="dark blue", fg="red", show="*")
        self.__password_input.grid(row=3, column=1, padx=(0, 3), pady=(0, 3))
        self.__password_input.bind("<FocusIn>", self.__on_entry_focus_password)
        self.__password_input.bind("<FocusOut>", self.__on_entry_focus_out_password)


        # Create the "Submit" button with a red background to switch to the Main Menu screen
        submit_button = tk.Button(self, text="Create", command=self.__submit_details, font=("Arial", 16), bg="red", fg="blue")
        submit_button.grid(row=4, columnspan=4, pady=10)

        # Add an error label to display the error message
        self._error_label = tk.Label(self, text="", fg="red", bg="black")
        self._error_label.grid(row=6, columnspan=4)

        # Add an image 200 pixels below the "Submit" button
        logo_image = Image.open("logo.png")
        logo_image = logo_image.resize((400, 200), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        self._logo_label = tk.Label(self, image=logo_photo, bg="black")
        self._logo_label.image = logo_photo
        self._logo_label.grid(row=7, columnspan=4, pady=10)

        # Create a "Log In" button to switch to the LogInScreen
        login_button = tk.Button(self, text="Log In", command=self.__switch_to_login_screen, font=("Arial", 16), bg="red", fg="blue")
        login_button.grid(row=8, columnspan=4, pady=10)
        
        
        quit_button = tk.Button(self, text="Quit", command=self.__quit_program, font=("Arial", 16), bg="red", fg="blue")
        quit_button.grid(row=7, column=7, pady=15)


    def __on_entry_focus_password(self, event): #The password field will change colour to light blue when it is clicked. 
        event.widget.config(bg="#7ab8ff")

    def __on_entry_focus_out_password(self, event): # The password field will be dark blue when it is yet to be clicked. 
        event.widget.config(bg="dark blue")
    
    def __on_entry_focus_username(self, event): #The password field will change colour to light blue when it is clicked. 
        event.widget.config(bg="#7ab8ff")

    def __on_entry_focus_out_username(self, event): # The password field will be dark blue when it is yet to be clicked. 
        event.widget.config(bg="dark blue")

    def __submit_details(self):
        # This function is responsible for adding the details to the database. If the username already exists in the database, an error will output informing the user to create a new one. 
        connection = sqlite3.connect("LoginDetails.db")
        cursor = connection.cursor()

        # A table called PasswordDetails with the passwordID and the hah value of the password being stored. 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PasswordDetails (
                passwordID INTEGER PRIMARY KEY AUTOINCREMENT,
                hashed_password TEXT
            )
        ''')

        # A table called IDDetails which stored the userID and passwordID.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS IDDetails (
                userID INTEGER PRIMARY KEY AUTOINCREMENT,
                passwordID INTEGER,
                FOREIGN KEY(passwordID) REFERENCES PasswordDetails(passwordID)
            )
        ''')

        # A table called Users, which stores the UserID and the username. 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS UsernameDetails (
                userID INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                FOREIGN KEY(userID) REFERENCES IDDetails(userID)
            )
        ''')

        if len(self.__username_input.get()) < 6:        #Checks if the username is less than 6 characters
            messagebox.showinfo("Error","Your username needs to be at least 6 characters!")
        
        elif len(self.__username_input.get()) > 15:      # Checks whether the username is greater than 15 characters. 
            messagebox.showinfo("Error", "Your username needs to be less than or equal to 15 characters!")
        
        elif len(self.__password_input.get()) < 6:       # Added security measure of checking password length. 
            messagebox.showinfo("Error", "Your password needs to be at least 6 characters!")

        else:
            # Hash the password
            hashed_password = self.__HashPassword(self.__password_input.get())     # Password gets hashed. 

            # Check if username already exists
            cursor.execute('SELECT * FROM UsernameDetails WHERE username = ?', (self.__username_input.get(),))


            if cursor.fetchone(): # Does the username exist
                messagebox.showerror("Error", "Username already exists. Directing you to the login screen...")  #yes
                self.__switch_to_login_screen()
            else:
                # Insert data into PasswordDetails table
                cursor.execute('INSERT INTO PasswordDetails (hashed_password) VALUES (?)', (hashed_password,))  #no
                passwordID = cursor.lastrowid 

                # Insert data into IDDetails table
                cursor.execute('INSERT INTO IDDetails (userID, passwordID) VALUES (?, ?)', (cursor.lastrowid, passwordID))

                # Get the userID of the inserted row
                userID = cursor.lastrowid

                # Insert data into Users table
                cursor.execute('INSERT INTO UsernameDetails (userID, username) VALUES (?, ?)', (userID, self.__username_input.get()))

                # Commit changes and close connection
                messagebox.showinfo("Success", "Account created successfully!")
                connection.commit()
                connection.close()

                # Direct to Main Menu Screen
                self.__switch_to_main_menu_screen()

    
    def __HashPassword(self, password):
        # This function is responsible for hashing the password to improve the security of the system and for additional verification and authentication processes before allowing the user to enter the system. 
        rt = 0
        for i in range(0, len(password)-1):
            rt += ord(password[i])
        return rt

    def __switch_to_main_menu_screen(self):
        # This function is responsible for switching to the Main Menu Screen
        self.master.switch_frame(MainMenuScreen)

    def __switch_to_login_screen(self):
        # Thie function is responsible for switching to the Login Screen
        self.master.switch_frame(LogInScreen)
    
    def __quit_program(self):
        # This function will quit the program if the user clicks on the Quit button 
        self.master.destroy()

class LogInScreen(tk.Frame): #Inheritance and Polymorphism from the tk.Frame class. 
    # If an account has already been created with the system, clicking on the LogIn button will direct them to this screen where they will be able to login and see whether their account exists or not. 
    def __init__(self, master=None):
        super().__init__(master, bg="black")
        self.master = master
        self.grid(sticky="nsew")
        self.__create_widgets()

    def __create_widgets(self):
        # Create the "Log In" label with a bigger font
        login_label = tk.Label(self, text="Log In", font=("Arial", 36), fg="orange", bg="black")
        login_label.grid(row=1, pady=(100, 15), columnspan=4)

        # Create the "Username:" label
        username_label = tk.Label(self, text="Username:", font=("Arial", 14), fg="white", bg="black")
        username_label.grid(row=2, column=0, sticky='e', padx=(3, 0), pady=(0, 3))

        # Create the input box for the username
        self.__username_input = tk.Entry(self, font=("Arial", 14), bg="dark blue", fg="red")
        self.__username_input.grid(row=2, column=1, padx=(0, 3), pady=(0, 3))
        self.__username_input.bind("<FocusIn>", self.__on_entry_focus_username)
        self.__username_input.bind("<FocusOut>", self.__on_entry_focus_out_username)

        # Create the "Login" button with a red background to check the username
        login_button = tk.Button(self, text="Log In", command=self.__check_login, font=("Arial", 16), fg="blue", bg="red")
        login_button.grid(row=5, columnspan=4, pady=10)

        self.__password_label = tk.Label(self, text="Password:", font=("Arial", 14), fg="white", bg="black")
        self.__password_label.grid(row=3, column=0, sticky='e', padx=(3, 0), pady=(0, 3))
        self.__password_input = tk.Entry(self, font=("Arial", 14), bg="dark blue", fg="red", show="*")
        self.__password_input.grid(row=3, column=1, padx=(0, 3), pady=(0, 3))
        self.__password_input.bind("<FocusIn>", self.__on_entry_focus_password)
        self.__password_input.bind("<FocusOut>", self.__on_entry_focus_out_password)

        # Create an error label to display the error message
        self.__error_label = tk.Label(self, text="", fg="red", bg="black")
        self.__error_label.grid(row=4, columnspan=4)

        # Add an image below the error label
        logo_image = Image.open("logo.png")
        logo_image = logo_image.resize((300, 150), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        self.__logo_label = tk.Label(self, image=logo_photo, bg="black")
        self.__logo_label.image = logo_photo
        self.__logo_label.grid(row=6, columnspan=4, pady=10)
        

        back_button = tk.Button(self, text="Back", command=self.master.go_back, font=("Arial", 16), fg="blue", bg="red")
        back_button.grid(row=2, column=10, pady=10)


        home_button = tk.Button(self, text="Home", command=self.__switch_to_create_account, font=("Arial", 16), fg="blue", bg="red")
        home_button.grid(row=3, column=10, pady=10)
    
    def __HashPassword(self, password):
        #This is the same password hashing function as in the CreateAccountScreen class.
        rt = 0
        for i in range(0, len(password)-1):
            rt += ord(password[i])
        return rt
    

    def __switch_to_create_account(self):
        # This function switches the screen back to the CreateAccountScreen class 
        self.master.switch_frame(CreateAccountScreen)


    def __check_login(self):
        try:
            # Connect to the database
            connection = sqlite3.connect("LoginDetails.db")
            cursor = connection.cursor()

            # Check if UsernameDetails table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='UsernameDetails'")
            if cursor.fetchone():
                # Get the entered password
                entered_password = self.__password_input.get()

                # Check 1: Does the username exist in the database
                cursor.execute('SELECT * FROM UsernameDetails WHERE username = ?', (self.__username_input.get(),))
                user_data = cursor.fetchone()

                if user_data:
                    # Check 2: Compare hashed passwords in IDDetails table
                    hashed_entered_password = self.__HashPassword(entered_password)
                    cursor.execute('''
                        SELECT hashed_password
                        FROM PasswordDetails
                        WHERE passwordID = ?
                    ''', (user_data[1],))  # Assuming passwordID is in the second column of IDDetails
                    hashed_db_password = cursor.fetchone()

                    # Check 3: Check for plaintext password (existing check)
                    if entered_password == user_data[1]:  # Assuming plaintext password is stored in the second column
                        # Perform additional checks if needed

                        # Successful login
                        messagebox.showinfo("Success", "Logging In...")
                        self.__switch_to_main_menu()
                    elif hashed_db_password and hashed_entered_password == hashed_db_password[0]:
                        # Successful login
                        messagebox.showinfo("Success", "Logging In...")
                        self.__switch_to_main_menu()
                    else:
                        # Incorrect password
                        messagebox.showerror("Error", "Invalid password!")
                else:
                    # Invalid username
                    messagebox.showerror("Error", "Invalid username!")
            else:
                # UsernameDetails table doesn't exist
                messagebox.showerror("Error", "No usernames have been created!")

        except sqlite3.Error as e:
            # Handle SQLite errors
            messagebox.showerror("Error", f"SQLite error: {e}")

        finally:
            # Close the database connection
            if connection:
                connection.close()
    
    def __on_entry_focus_password(self, event):
        event.widget.config(bg="#7ab8ff")

    def __on_entry_focus_out_password(self, event):
        event.widget.config(bg="dark blue")
    
    def __on_entry_focus_username(self, event):
        event.widget.config(bg="#7ab8ff")

    def __on_entry_focus_out_username(self, event):
        event.widget.config(bg="dark blue")

    def __switch_to_main_menu(self):
        # This function is responsible for switching to the Main Menu. 
        self.master.switch_frame(MainMenuScreen)

class MainMenuScreen(tk.Frame):
    # This class displays the main menu and the options that are available for the user. 
    def __init__(self, master=None):
        super().__init__(master, bg="black")
        self.master = master
        self.grid(sticky="nsew")
        self.__create_widgets()

    def __create_widgets(self):
        main_menu_label = tk.Label(self, text="Main Menu", font=("Arial", 24), fg="orange", bg="black")
        main_menu_label.grid(row=0, column = 10, pady=(100, 20), columnspan=10)
        

        # Create a "Standard Chess" button
        standard_chess_button = tk.Button(self, text="Standard Chess", command=self.__return_standard_chess, font=("Arial", 16), fg="blue", bg="red", height = 2)  # Normal game of chess player vs player
        standard_chess_button.grid(row=1, column=12, padx=10, pady=15)

        big_bang_variant_button = tk.Button(self, text="Big Bang Variant", command=self.__return_big_bang_variant, font=("Arial", 16), fg="blue", bg="red", height = 2) # My own Big Bang variant
        big_bang_variant_button.grid(row=2, column=12, padx = 10, pady=15)

        lichess_stats__button = tk.Button(self, text="View Lichess Stats", command=self.__return_get_lichess_data, font=("Arial", 16), fg="blue", bg="red", height = 2) #Viewing lichess stats but this code is on a different file called ViewLichessStats.py
        lichess_stats__button.grid(row=4, column=12, padx=10, pady=10)

        self.__message_label = tk.Label(self, text="", font=("Arial", 16), fg="red", bg="black") #Potential for dealing with any errors, should they arise. This could also be used to display any messages like the need to go onto a different file. 
        self.__message_label.grid(row= 10, column=10, pady=10)

        back_button = tk.Button(self, text="Back", command=self.master.go_back, font=("Arial", 16), fg="blue", bg="red")  # This function will pop the last screen from the stack and then return the user to that screen.
        back_button.grid(row=5, column=8, pady=10)
        

    def __return_standard_chess(self):
        # Return a value of 1 to show that the user wants to play the standard game of chess. 
        self.__quit_program(1)

    def __return_big_bang_variant(self):
        # Return a value of 2 to show that the user wants to play the variant. 
        self.__quit_program(2)

    def __return_get_lichess_data(self):
        # Output the error message if the View Lichess Stats button is clicked
        self.__message_label.config(text="To view the data, run the code in ViewLichessStats.py")


    def __quit_program(self, value):
        self.master.return_value = value
        self.master.destroy()
  
    def __switch_to_create_account(self):
        self.master.switch_frame(CreateAccountScreen)
    
    def __switch_to_main_menu(self):
        self.master.switch_frame(MainMenuScreen)

class App(tk.Tk):
    # Basic interface is initialised before any changes are made to it. 
    def __init__(self, start_frame = CreateAccountScreen):
        super().__init__()
        self.geometry("800x700")
        self.title("Create Account")
        self.configure(bg="black")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.return_value = None
        self.current_frame = None

        self._stack = Stack(10)  # Initialize the stack. Association aggregation shown here. 
        self.is_first_switch = True
        self.switch_frame(start_frame)

    def switch_frame(self, frame_class, going_back=False):
        # This method defines how the screens switch between each other. 
        if not going_back and self.current_frame:
            self._stack.push(self.current_frame.__class__)
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def go_back(self):
        # Going back to the last accessed frame.
        if not self._stack.isEmpty(): # if the stack is not empty
            previous_frame_class = self._stack.pop()
            self.switch_frame(previous_frame_class, going_back=True)
        else:
            messagebox.showinfo("Back Navigation", "No previous screen to go back to.")



def load_and_scale_image(pieceset, colour, piece_type, size):
    # This function is responsible for loading an image and then scaling it to a smaller size. 
    image = pygame.image.load(f'Assets/{pieceset}/{piece_type}_{colour}.png').convert_alpha()
    return pygame.transform.scale(image, size)

def initialise_images(pieceset):
    # This function is responsible for initialising all of the images based off the user's requirements and selection of the pieceset. 
    sizes = {
        '3D': {'queen': (120, 120), 'king': (120, 120), 'rook': (120, 120), 'bishop': (120, 120),
               'knight': (120, 120), 'pawn': (100, 100), 'small': (45, 45)},
        'basic': {'queen': (90, 90), 'king': (90, 90), 'rook': (90, 90), 'bishop': (90, 90),
                  'knight': (90, 90), 'pawn': (80, 80), 'small': (45, 45)},
        'anarcandy': {'queen': (80, 80), 'king': (80, 80), 'rook': (80, 80), 'bishop': (60, 80),
                      'knight': (70, 70), 'pawn': (70, 70), 'small': (30, 30)},
        'merida': {'queen': (90, 90), 'king': (90, 90), 'rook': (90, 90), 'bishop': (90, 90),
                   'knight': (90, 90), 'pawn': (80, 80), 'small': (45, 45)}
    }

    warnings.filterwarnings("ignore", category=RuntimeWarning)

    white_pawn = load_and_scale_image(pieceset, 'white', 'pawn', sizes[pieceset]['pawn'])
    white_pawn_small = pygame.transform.scale(white_pawn, sizes[pieceset]['small'])

    black_pawn = load_and_scale_image(pieceset, 'black', 'pawn', sizes[pieceset]['pawn'])
    black_pawn_small = pygame.transform.scale(black_pawn, sizes[pieceset]['small'])

    white_knight = load_and_scale_image(pieceset, 'white', 'knight', sizes[pieceset]['knight'])
    white_knight_small = pygame.transform.scale(white_knight, sizes[pieceset]['small'])

    black_knight = load_and_scale_image(pieceset, 'black', 'knight', sizes[pieceset]['knight'])
    black_knight_small = pygame.transform.scale(black_knight, sizes[pieceset]['small'])

    white_bishop = load_and_scale_image(pieceset, 'white', 'bishop', sizes[pieceset]['bishop'])
    white_bishop_small = pygame.transform.scale(white_bishop, sizes[pieceset]['small'])

    black_bishop = load_and_scale_image(pieceset, 'black', 'bishop', sizes[pieceset]['bishop'])
    black_bishop_small = pygame.transform.scale(black_bishop, sizes[pieceset]['small'])

    white_rook = load_and_scale_image(pieceset, 'white', 'rook', sizes[pieceset]['rook'])
    white_rook_small = pygame.transform.scale(white_rook, sizes[pieceset]['small'])

    black_rook = load_and_scale_image(pieceset, 'black', 'rook', sizes[pieceset]['rook'])
    black_rook_small = pygame.transform.scale(black_rook, sizes[pieceset]['small'])

    white_queen = load_and_scale_image(pieceset, 'white', 'queen', sizes[pieceset]['queen'])
    white_queen_small = pygame.transform.scale(white_queen, sizes[pieceset]['small'])

    black_queen = load_and_scale_image(pieceset, 'black', 'queen', sizes[pieceset]['queen'])
    black_queen_small = pygame.transform.scale(black_queen, sizes[pieceset]['small'])

    white_king = load_and_scale_image(pieceset, 'white', 'king', sizes[pieceset]['king'])
    white_king_small = pygame.transform.scale(white_king, sizes[pieceset]['small'])

    black_king = load_and_scale_image(pieceset, 'black', 'king', sizes[pieceset]['king'])
    black_king_small = pygame.transform.scale(black_king, sizes[pieceset]['small'])


    return white_pawn, white_pawn_small, black_pawn, black_pawn_small, white_knight, white_knight_small, black_knight, black_knight_small, white_bishop, white_bishop_small, black_bishop, black_bishop_small, white_rook, white_rook_small, black_rook, black_rook_small, white_queen, white_queen_small, black_queen, black_queen_small, white_king, white_king_small, black_king, black_king_small
           

def initialise_game_variables():
    # This function is responsible for setting and resetting all of the game variables. This is called at the start of the game and at the end of the game when the user wants to play again. 
    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    
    # 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
    turn_step = 0
    selection = 100
    valid_moves = []
    white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
    white_promotions = ['bishop', 'knight', 'rook', 'queen']
    white_moved = [False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False]
    small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                        white_rook_small, white_bishop_small]
    black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
    small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                        black_rook_small, black_bishop_small]
    black_promotions = ['bishop', 'knight', 'rook', 'queen']
    black_moved = [False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False]
    piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
    # check variables/ flashing counter
    counter = 0
    winner = ''
    game_over = False
    white_ep = (100, 100)
    black_ep = (100, 100)
    white_promote = False
    black_promote = False
    promo_index = 100
    check = False
    castling_moves = []

    return white_pieces, white_locations, black_pieces, black_locations, turn_step, selection, valid_moves, white_images, white_promotions, white_moved, small_white_images, black_images, small_black_images, black_promotions, black_moved, piece_list, counter, winner, game_over, white_ep, black_ep, white_promote, black_promote, promo_index, check, castling_moves



if __name__ == "__main__":
    app = App()
    app.mainloop()

    return_value = app.return_value # The return value from clicking one of the buttons on the MainMenuScreen. 

    # Handling the return value
    if return_value == 1: # If the Standard Chess Button was clicked
        
        game_run = False
        pygame.init()
        background = getBgCol()  # Get the background colour that the user wants
        sqcols = getSquareColour() # Get the square colours that the user wants
        pieceset = selectPieceSet() # Get the pieceset that the user wants
        game_run = True
        if game_run:
            WIDTH = 1000
            HEIGHT = 900
            screen = pygame.display.set_mode([WIDTH, HEIGHT])
            pygame.display.set_caption('Two-Player Pygame Chess!')
            font = pygame.font.Font('freesansbold.ttf', 20)
            medium_font = pygame.font.Font('freesansbold.ttf', 40)
            big_font = pygame.font.Font('freesansbold.ttf', 50)
            timer = pygame.time.Clock()
            fps = 60



            white_pawn, white_pawn_small, black_pawn, black_pawn_small, white_knight, white_knight_small, black_knight, black_knight_small, white_bishop, white_bishop_small, black_bishop, black_bishop_small, white_rook, white_rook_small, black_rook, black_rook_small, white_queen, white_queen_small, black_queen, black_queen_small, white_king, white_king_small, black_king, black_king_small =initialise_images(pieceset)  # Initialise the images required to make the display
                
            white_pieces, white_locations, black_pieces, black_locations, turn_step, selection, valid_moves, white_images, white_promotions, white_moved, small_white_images, black_images, small_black_images, black_promotions, black_moved, piece_list, counter, winner, game_over, white_ep, black_ep, white_promote, black_promote, promo_index, check, castling_moves =initialise_game_variables()  # Initialise the game variables


            black_options, castling_moves = check_options(black_pieces, black_locations, 'black', castling_moves, check)  # Get black's legal moves. 
            white_options, castling_moves = check_options(white_pieces, white_locations, 'white', castling_moves, check)  # Get white's legal moves.
            run = True
            while run:
                timer.tick(fps)
                if counter < 30:
                    counter += 1
                else:
                    counter = 0

                screen.fill(background)
                draw_board(sqcols[0], sqcols[1])
                draw_pieces(pieceset)
                draw_check(turn_step, counter)
                if not game_over:
                    white_promote, black_promote, promo_index = check_promotion()
                    if white_promote or black_promote:
                        draw_promotion()
                        check_promo_select()
                if selection != 100:
                    valid_moves = check_valid_moves(white_options, black_options, turn_step, selection)
                    draw_valid(valid_moves, turn_step)
                    if selected_piece == 'king':
                        draw_castling(turn_step, castling_moves)
                # event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                        x_coord = event.pos[0] // 100  # Get the x position of the mouse click
                        y_coord = event.pos[1] // 100  # Get the y position of the mouse click

                        click_coords = (x_coord, y_coord)
                        if turn_step <= 1:  # If it's white's turn
                            if click_coords == (8, 8) or click_coords == (9, 8):  # If the resign button is clicked
                                winner = 'black' # Black wins
                            
                            elif len(white_options) == 0:  # We have a stalemate
                                winner = 'draw'


                            if click_coords in white_locations: # Check if a piece has been selected
                                selection = white_locations.index(click_coords)
                                selected_piece = white_pieces[selection]

                                if turn_step == 0:
                                    turn_step = 1  # Move onto the next game phase where you have to select a destination for that piece

                            if click_coords in valid_moves and selection != 100:
                                white_ep = check_en_passant(turn_step, white_locations[selection], click_coords)
                                white_locations[selection] = click_coords
                                white_moved[selection] = True

                                if click_coords in black_locations:  # if the second set of coordinates is in the black_locations (i.e. where the black pieces are)
                                    black_piece = black_locations.index(click_coords) # get the index of the piece that is being attacked and clicked on
                                    if black_pieces[black_piece] == 'king':  # If the piece is the king,
                                        winner = 'white'  # White wins. 
                                    black_pieces.pop(black_piece)  # remove the piece from the board
                                    black_locations.pop(black_piece) # remove the piece from the list of black locations
                                    black_moved.pop(black_piece)  # remove the piece from the list of pieces that can be moved. 
                                
                                if click_coords == black_ep:   # If it's an en passant move, remove the piece that has been captured by en passant
                                    black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
                                    black_pieces.pop(black_piece)
                                    black_locations.pop(black_piece)
                                    black_moved.pop(black_piece)

                                black_options, castling_moves = check_options(black_pieces, black_locations, 'black', castling_moves, check)  # Get the new set of legal mvoes 
                                white_options, castling_moves = check_options(white_pieces, white_locations, 'white', castling_moves, check) # Get the new set of legal moves
                                turn_step = 2  # Black's turn
                                selection = 100
                                valid_moves = []

                            # add option to castle
                            elif selection != 100 and selected_piece == 'king': # Check whether castling is legal
                                for q in range(len(castling_moves)):
                                    if click_coords == castling_moves[q][0]:
                                        white_locations[selection] = click_coords
                                        white_moved[selection] = True
                                        if click_coords == (1, 0):
                                            rook_coords = (0, 0)
                                        else:
                                            rook_coords = (7, 0)
                                        rook_index = white_locations.index(rook_coords)
                                        white_locations[rook_index] = castling_moves[q][1]

                                        black_options, castling_moves = check_options(black_pieces, black_locations, 'black', castling_moves, check)
                                        white_options, castling_moves = check_options(white_pieces, white_locations, 'white', castling_moves, check)
                                        turn_step = 2
                                        selection = 100
                                        valid_moves = []

                        if turn_step > 1: # Black's turn
                            if click_coords == (8, 8) or click_coords == (9, 8): # If the resign button is pressed
                                winner = 'white' # White wins.

                            elif len(black_options) == 0: # Stalemate
                                winner = 'draw' 


                            if click_coords in black_locations:
                                selection = black_locations.index(click_coords)
                                # check what piece is selected, so you can only draw castling moves if king is selected
                                selected_piece = black_pieces[selection]
                                if turn_step == 2:
                                    turn_step = 3 # Time to move said selected piece to a destination. 


                            if click_coords in valid_moves and selection != 100: # If the move is legal, make the move. 
                                black_ep = check_en_passant(turn_step, black_locations[selection], click_coords)
                                black_locations[selection] = click_coords
                                black_moved[selection] = True


                                if click_coords in white_locations: # If the destination has a white piece on it already. 
                                    white_piece = white_locations.index(click_coords) # Works out what is the piece on the square. 

                                    if white_pieces[white_piece] == 'king': # If the piece is the king, the king is captured and black wins. 
                                        winner = 'black' # Black wins

                                    white_pieces.pop(white_piece)
                                    white_locations.pop(white_piece)  # Remove the captured piece from the board and we no longer need to keep a track of its location due to it not being present on the board. 
                                    white_moved.pop(white_piece)

                                if click_coords == white_ep:     # Make the en passant capture if it is an en passant capture. 
                                    white_piece = white_locations.index((white_ep[0], white_ep[1] + 1))
                                    white_pieces.pop(white_piece)
                                    white_locations.pop(white_piece)
                                    white_moved.pop(white_piece)


                                black_options, castling_moves = check_options(black_pieces, black_locations, 'black', castling_moves, check) # Switch back to white's turn
                                white_options, castling_moves = check_options(white_pieces, white_locations, 'white', castling_moves, check)
                                turn_step = 0
                                selection = 100
                                valid_moves = []

                            # add option to castle
                            elif selection != 100 and selected_piece == 'king':
                                for q in range(len(castling_moves)):
                                    if click_coords == castling_moves[q][0]:
                                        black_locations[selection] = click_coords
                                        black_moved[selection] = True
                                        if click_coords == (1, 7):
                                            rook_coords = (0, 7)
                                        else:
                                            rook_coords = (7, 7)
                                        rook_index = black_locations.index(rook_coords)
                                        black_locations[rook_index] = castling_moves[q][1]
                                        black_options, castling_moves = check_options(black_pieces, black_locations, 'black', castling_moves, check)
                                        white_options, castling_moves = check_options(white_pieces, white_locations, 'white', castling_moves, check)
                                        turn_step = 0
                                        selection = 100
                                        valid_moves = []


                    if event.type == pygame.KEYDOWN and game_over: # If the game is over and a key is pressed down,
                        if event.key == pygame.K_RETURN: # If said key is the ENTER key, 
                            white_pieces, white_locations, black_pieces, black_locations, turn_step, selection, valid_moves, white_images, white_promotions, white_moved, small_white_images, black_images, small_black_images, black_promotions, black_moved, piece_list, counter, winner, game_over, white_ep, black_ep, white_promote, black_promote, promo_index, check, castling_moves =initialise_game_variables() # reinitialise the game variables
                            winner = '' # set the winner to '' as there is no winner and we have a new game on our hands
                            black_options, castling_moves = check_options(black_pieces, black_locations, 'black', castling_moves, check) # Get the legal moves of the position
                            white_options, castling_moves = check_options(white_pieces, white_locations, 'white', castling_moves, check)

                if winner != '': # If the king has been captured at any point, then we have a winner according to the code logic. 
                    game_over = True # flag variable to indicate that the game is over
                    draw_game_over(winner) # Draw the game over message to indicate the outcome of the game.
                pygame.display.update()
            pygame.quit()



    elif return_value == 2:
        running = True
        rules = False
        print("""______ _         ______                      _   _            _             _   
        | ___ (_)        | ___ \                    | | | |          (_)           | |  
        | |_/ /_  __ _   | |_/ / __ _ _ __   __ _   | | | | __ _ _ __ _  __ _ _ __ | |_ 
        | ___ \ |/ _` |  | ___ \/ _` | '_ \ / _` |  | | | |/ _` | '__| |/ _` | '_ \| __|
        | |_/ / | (_| |  | |_/ / (_| | | | | (_| |  \ \_/ / (_| | |  | | (_| | | | | |_ 
        \____/|_|\__, |  \____/ \__,_|_| |_|\__, |   \___/ \__,_|_|  |_|\__,_|_| |_|\__|
                __/  /                      __/ /                                      
                |___/                      |___/                                       """)

        print("\n\n")

        print("Welcome to my variant.")
        time.sleep(2)
        print("Would you like to learn the rules?")
        while rules == False:
            y_or_n = input(">(Y/N)").lower()
            if y_or_n == "y":
                print("1) It is the first of its kind and the rules are simple.")
                print("\n")
                time.sleep(3)
                print("2) All of the pieces move like normal chess but there are some new rules.")
                print("\n")
                time.sleep(3)
                print("3) There is no castling, no checkmate, no en passant and no check, which means that you will have to rely on your brain power and wit to capture all of the pieces.")
                print("\n")
                time.sleep(4)
                print("4) There are an additional two pieces to this game: the Grand Empress and the Serpent.")
                print("\n")
                time.sleep(3)
                print("5) The Grand Empress moves similar to a knight but can't capture pieces. It is a healer against the serpent's poison.")
                print("\n")
                time.sleep(8)
                print("6) The serpent can move forward four squares at a time but can't move in any other direction.")
                print("\n")
                time.sleep(5)
                print("You have two serpent pieces: one is able to capture pieces while the other isn't able to capture them as it is not poisonous.")
                print("\n")
                time.sleep(5)
                print("If the Grand Empress is not on a neighbouring square to the piece that is being captured by the serpent, then the piece will be removed from the board.")
                print("\n")
                time.sleep(6)
                print("Once healed, both the serpent and the Grand Empress die and are removed from the game.")
                print("\n")
                time.sleep(3)
                rules = True

            elif y_or_n == "n":
                rules = True

            else:
                print("Please only enter y or n.")

        bgcol = getBgCol()
        colours= getSquareColour()     
        pieceset = selectPieceSet()
        run = True
        if run == True:
            a = BBApp()
            game = a.main(bgcol, colours, pieceset)
            warnings.filterwarnings("ignore", category=RuntimeWarning)