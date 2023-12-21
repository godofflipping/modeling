from ant import Ant


class Spawnpoint:
    
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.board = board
        self.log_message = ""
     
                               
    def startSpawn(self):
        self.spawnAnt(3, 2, 0)
        self.spawnAnt(5, 1, 0)
            
    
    def spawnAnt(self, y, x, load):
        if len(self.board.ants) < self.board.max_ants:
            ant = Ant(y, x, self.board, load)
            self.board.ants.append(ant)
            self.board.ant_map[y][x] = 1
    
    
    def isFree(self):
        if self.board.ant_map[self.y][self.x] == 0:
            return True
        return False
    
    
    def run(self):
        if self.board.is_start:
            self.startSpawn()
            self.board.is_start = False
            