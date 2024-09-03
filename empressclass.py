from piececlass import Piece

class GrandEmpress(Piece): # polymorphism shown here
    # grand empress piece class
    # This is the first new piece I have created as part of my variant. 
    def __init__(self):
        super().__init__() # inheritance shown here
        self.__setAttributes()

    def __setAttributes(self):
        self._value = 7  # In the game of chess, the king doesn't actually carry a value. Capturing the king or putting the king in checkmate signifies the game is over and by no means affects the material count.
        # By giving the king an extremely large value (relative to the other pieces), we can work out whether the game is over by working out the overall material count for a given side.
    

    def _check_empress(self, position, colour, white_locations, black_locations):
        moves_list = []

        enemies_list, friends_list = self._get_friends_and_enemies(colour, white_locations, black_locations)

        targets = [(2,1), (2,-1), (1,2), (1,-2), (-1,2), (-1,-2), (-2,1), (-2,-1)]
        for i in range(len(targets)):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if target not in friends_list and target not in enemies_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list 
