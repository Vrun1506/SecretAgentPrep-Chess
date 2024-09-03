from piececlass import Piece

class Bishop(Piece): # Polymorphism shown here
    # The Bishop piece class
    def __init__(self):
        super().__init__()  # Inheritance shown here
        self.__setAttributes()

    def __setAttributes(self):
        # Set the piece value. 
        self._value = 3

    
    def _check_bishop(self, position, colour, white_locations, black_locations):
    #This function is responsible for fetching the legal moves that can be made by a bishop in a given position. 
    #The bishop is able to move along the diagonals through as many squares as desired until there is a blockade in the diagonal that is being pursued. 

        moves_list = []
        directions = [(1, -1), (-1, -1), (1, 1), (-1, 1)]  #These are the basic direction vectors of the movement without any chain. 


        enemies_list, friends_list = self._get_friends_and_enemies(colour, white_locations, black_locations)

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