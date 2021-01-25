class Board:

    flower_space = "X"
    none_space = "--"
    column_space = " | "
    empty_space = "O"

    tiles = [[]]

    player_path_row_column = {}
    player_path_row_column[1] = {
        1: [3, 0],
        2: [2, 0],
        3: [1, 0],
        4: [0, 0],
        5: [0, 1],
        6: [1, 1],
        7: [2, 1],
        8: [3, 1],
        9: [4, 1],
        10: [5, 1],
        11: [6, 1],
        12: [7, 1],
        13: [7, 0],
        14: [6, 0],
        15: [5,0]
    }

    player_path_row_column[2] = {
        1: [3, 2],
        2: [2, 2],
        3: [1, 2],
        4: [0, 2],
        5: [0, 1],
        6: [1, 1],
        7: [2, 1],
        8: [3, 1],
        9: [4, 1],
        10: [5, 1],
        11: [6, 1],
        12: [7, 1],
        13: [7, 2],
        14: [6, 2],
        15: [5,2]
    }

    def __init__(self, h, w):
        self.tiles = [[self.empty_space for x in range(w)] for y in range(h)]
        self.tiles[0][0] = self.flower_space
        self.tiles[0][2] = self.flower_space
        self.tiles[4][0] = self.none_space
        self.tiles[5][0] = self.none_space
        self.tiles[4][2] = self.none_space
        self.tiles[5][2] = self.none_space
        self.tiles[3][1] = self.flower_space
        self.tiles[6][0] = self.flower_space
        self.tiles[6][2] = self.flower_space

        self.last_tile_location = len(self.player_path_row_column[1])

    def to_text(self):
        display = ""
        for i in range(0, len(self.tiles)):
            for j in range(0, len(self.tiles[i])):
                if j != 0:
                    display = display + self.column_space
                display = display + self.tiles[i][j]
            display = display + "\n"
        return display

    def place_token(self, token, location):
        row_column = {}
        row_column = self.get_player_path(token)

        
        if location not in row_column:
            raise Exception(
                "place_token error. self: {0} token: {1} location{2}".format(
                    self, token, location
                )
            )

        if location == self.last_tile_location :
            return # we can pretend that we move it by not updating that board peice
            
        row_index = row_column[location][0]
        column_index = row_column[location][1]
        self.tiles[row_index][column_index] = token.owner_symbol

    def get_player_path(self, token):
        if token.owner == "Player 1":
            return self.player_path_row_column[1]
        elif token.owner == "Player 2":
            return self.player_path_row_column[2]
        else :
            raise Exception("get_player_path error {0}".format(token))

    """
        Returns the place on the board that a players tokens are e.g. 1-14
    """
    def find_all_player_locations(self, token):
        location_list = []
        player_path = self.get_player_path(token)
        for k,v in player_path.items():
            row = v[0]
            col = v[1]
            if self.tiles[row][col] == token.owner_symbol:
                location_list.append(self.find_location_from_coord(token, row, col))

        return location_list

    def find_location_from_coord(self,token, i, j):

        if token.owner == "Player 1":
            for k,v in self.player_path_row_column[1].items():
                if v[0] == i and v[1]==j:
                    return k
        elif token.owner == "Player 2":
            for k,v in self.player_path_row_column[2].items():
                if v[0] == i and v[1]==j:
                    return k
        else : 
            raise Exception("find_location_from_coord error finding owner {0} for coord {1}:{2}".format(token, i, j))

    def place_token_is_valid(self, token, location):
        if location == 0: 
            return False
        
        row_column = {}
        row_column = self.get_player_path(token)

        if location not in row_column:
            return False
        
        row = row_column[location][0]
        column = row_column[location][1]
        if self.tiles[row][column] in [token.owner_symbol]:
            return False

        return True

    def reset_tile(self, token, location):
        player_path = self.get_player_path(token)

        if location not in player_path:
            raise Exception("reset_tile error {0} - {1}".format(token, location))

        coordinate_to_reset = player_path[location]
        row = coordinate_to_reset[0]
        col = coordinate_to_reset[1]
        
        flower_spaces = [
            [0,0],
            [0,2],
            [3,1],
            [6,2]
        ]
        if coordinate_to_reset in flower_spaces :
            self.tiles[row][col] = self.flower_space
            return
        else :
            self.tiles[row][col] = self.empty_space
        

