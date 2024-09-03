from piececlass import Piece

class Rook(Piece): # Polymorphism shown here
    # The rook piece class
    def __init__(self):
        super().__init__() # Inheritance shown here
        self.__setAttributes()

    def __setAttributes(self):
        self._value = 5
    
    
    
    def _check_rook(self, position, colour, white_locations, black_locations):
    #This function is responsible for fetching all of the legal rook moves in a given position. 
    #The rook works in a very similar way to the bishop except that the rook moves horizontally or vertically. 

        moves_list = []

        enemies_list, friends_list = self._get_friends_and_enemies(colour, white_locations, black_locations)

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # down, up, right, left

        for x_pos, y_pos in directions:
            start_x, start_y = position
            chain = 1
            continue_checking = True

            while continue_checking and 0 <= start_x + chain * x_pos <= 7 and 0 <= start_y + chain * y_pos <= 7:
                new_position = (start_x + chain * x_pos, start_y + chain * y_pos)

                if new_position not in friends_list:
                    moves_list.append(new_position)

                    if new_position in enemies_list:
                        continue_checking = False

                    chain += 1
                else:
                    continue_checking = False

        return moves_list