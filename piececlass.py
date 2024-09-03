class Piece(object): # Base class for all of the pieces. The pieces all inherit the methods and attributes from this class
    def __init__(self):
        self._value = None
    
    def _get_friends_and_enemies(self, colour, white_locations, black_locations):
        # This function determines which are your own pieces based on the colour. 
        # I.e. if you have the white pieces and it's your turn, the enemy pieces are the black pieces (represented by black_locations) and the friendly pieces are the white pieces (represented by white_locations) and vice versa. 
        if colour == 'white':
            return black_locations, white_locations
        else:
            return white_locations, black_locations