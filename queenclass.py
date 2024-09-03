from piececlass import Piece
from bishopclass import Bishop
from rookclass import Rook


class Queen(Piece): # polymorphism shown here 
    # The queen piece class
    def __init__(self):
        super().__init__()  # inheritance shown here
        self.__setAttributes()

    def __setAttributes(self):
        self._value = 9

    
    # check queen valid moves
    def _check_queen(self, position, colour, white_locations, black_locations):
        piece1 = Bishop()
        moves_list = piece1._check_bishop(position, colour, white_locations, black_locations)
        piece2 = Rook()
        second_list = piece2._check_rook(position, colour, white_locations, black_locations)
        for i in range(len(second_list)):
            moves_list.append(second_list[i])
        return moves_list
