

class Board:
  
  flower_space = "X"
  none_space = "--"
  column_space = " | "
  empty_space = "O"

  tiles = [[]]

  def __init__(self, h,w):
    self.tiles = [["O" for x in range(w)] for y in range(h)] 
    self.tiles[0][0] = self.flower_space
    self.tiles[0][2] = self.flower_space
    self.tiles[4][0] = self.none_space
    self.tiles[5][0] = self.none_space
    self.tiles[4][2] = self.none_space
    self.tiles[5][2] = self.none_space
    self.tiles[3][1] = self.flower_space
    self.tiles[6][0] = self.flower_space
    self.tiles[6][2] = self.flower_space

  def to_text(self):
    display = ""
    for i in range(0, len(self.tiles)):
      for j in range(0, len(self.tiles[i])):
        if j != 0:
          display = display + self.column_space
        display = display + self.tiles[i][j]
      display = display + "\n"
    print (display)
    return display

  def place_token(self, token, location):
    # TODO fix this logic so it is not dependent on player 1 and 2
    if token.owner == "Player 1":
      row_column = {
        1 : [3,0],
        2 : [2,0],
        3 : [1,0],
        4 : [0,0], 
        5 : [0,1],
        6 : [1,1],
        7 : [2,1],
        8 : [3,1],
        9 : [4,1],
        10 : [5,1],
        11 : [6,1],
        12 : [7,1],
        13 : [7,0],
        14 : [6,0]
      }

    elif token.owner == "Player 2":
      row_column = {
        1 : [3,2],
        2 : [2,2],
        3 : [1,2],
        4 : [0,2], 
        5 : [0,1],
        6 : [1,1],
        7 : [2,1],
        8 : [3,1],
        9 : [4,1],
        10 : [5,1],
        11 : [6,1],
        12 : [7,1],
        13 : [7,2],
        14 : [6,2]
      }

    if len(row_column) < location : 
        raise Exception("place_token error. self: {0} token: {1} location{2}".format(self, token, location))
      
    self.tiles[row_column[location][0]][row_column[location][1]] = token.owner_symbol