from piececlass import Piece


class Serpent(Piece): # polymorphism shown here
    # serpent piece class. This is the second new piece I created as part of my variant. 
    def __init__(self):
        super().__init__()  # inheritance shown here
        self.__setAttributes()

    def __setAttributes(self):
        self._value = 6

    def __getTargets(self, colour):
        if colour == 'white':
            targets = [(0, 3)]
        else:
            targets = [(0, -3)]

        return targets  

    def _check_serpent(self, position, colour, white_locations, black_locations):
        # Get all of the legal moves that can be played by the serpent
        moves_list = []  # regular moves
        poisoned_list = [] # squares where enemy pieces are present.

        enemies_list, friends_list = self._get_friends_and_enemies(colour, white_locations, black_locations)

        targets = self.__getTargets(colour)


        for x, y in targets:
            target_x, target_y = position[0] + x, position[1] + y

            if 0 <= target_x <= 7 and 0 <= target_y <= 7 and (target_x, target_y) not in friends_list:
                moves_list.append((target_x, target_y))
                if (target_x, target_y) in enemies_list:
                    poisoned_list.append((target_x, target_y))

        return moves_list, poisoned_list