from piececlass import Piece

class King(Piece): # polymorphism shown here
    # the king piece class
    def __init__(self):
        super().__init__() # inheritance shown here
        self.__setAttributes()

    def __setAttributes(self):
        self._value = 1000  # In the game of chess, the king doesn't actually carry a value. Capturing the king or putting the king in checkmate signifies the game is over and by no means affects the material count.
        # By giving the king an extremely large value (relative to the other pieces), we can work out whether the game is over by working out the overall material count for a given side. 

    
    # check king valid moves
    def _check_king(self, position, colour, white_locations, black_locations):
        moves_list = [] #Stores all of the legal king moves. 

        enemies_list, friends_list = self._get_friends_and_enemies(colour, white_locations, black_locations)


        for x_pos in [-1, 0, 1]:              # A king can move one square in any direction. This for loop focusses on the x position. 
            for y_pos in [-1, 0, 1]:          # This nested for loops looks at the y position
                if x_pos == y_pos == 0:       #If they are both equal to 0, the king makes no moves.
                    pass

                target = (position[0] + x_pos, position[1] + y_pos)
                if 0 <= target[0] <= 7 and 0 <= target[1] <= 7 and target not in friends_list:  #Here, we make sure that the final end position the king ends up on is on the board (i.e. on a square with coordinates between 1 and 7 for both the x and y coordinates).
                    moves_list.append(target)

        return moves_list