from piececlass import Piece

class Pawn(Piece): # Polymorphism shown here
    def __init__(self):
        super().__init__() # Inheritance shown here
        self.__setAttributes()

    def __setAttributes(self):
        # This function sets the value of the pieces.
        self._value = 1

    
    def _check_pawn(self, position, colour, white_locations, black_locations):
        # This function is responsible for fetching all of the legal pawn moves.
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
                
        return moves_list