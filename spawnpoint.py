from ant import Ant

class Spawnpoint:
    def __init__(self, y, x, board):
        self.x = x
        self.y = y
        self.board = board
        
    
    def process(self):
        if self.isFree() and len(self.board.mail) > 0:
            self.spawnAnt(self.y, self.x)
            
    
    def isFree(self):
        if self.board.ant_map[self.y][self.x] == 0:
            return True
        return False
    
    
    def spawnAnt(self, y, x):
        if len(self.board.ants) < self.board.max_ants:
            self.board.ants.append(Ant(y, x, self.board, self.board.getLoad()))
            self.board.ant_map[y][x] = 1