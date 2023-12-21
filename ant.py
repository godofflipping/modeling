import random as rnd

class Ant:
    
    base_prob = 10
    
    def __init__(self, y, x, board, load):
        self.x = x
        self.y = y
        self.board = board
        self.load = load
        self.fer_per_run = 300
        
        self.path = []
        
    
    def process(self):
        if self.board.checkBox(self.y, self.x, self.load):
            self.leavePheromone()
            self.board.ant_map[self.y][self.x] = 0
            self.board.ants.remove(self)
            return
        
        neighbours = self.board.getValidNeibours(self.y, self.x)
        if len(neighbours) == 0:
            return
        
        weights = [10 + self.board[neighbour[0]][neighbour[1]] for neighbour in neighbours]
        decicion = rnd.random() * sum(weights)
        ind = 0
        
        while decicion > sum(weights[0 : ind + 1]):
            ind += 1
        
        self.path.append((neighbours[ind][0], neighbours[ind][1]))
        self.board.ant_map[self.y][self.x] = 0
        self.y, self.x = neighbours[ind][0], neighbours[ind][1]
        self.board.ant_map[self.y][self.x] = 1
        
    
    def leavePheromone(self):
        for i in self.path:
            self.board[i[0]][i[1]] += self.fer_per_run/len(self.path)
