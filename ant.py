import random as rnd

class Ant:
    counter = 0   
    base_prob = 10
    
    def __init__(self, y, x, board, load):
        Ant.counter += 1
        self.x = x
        self.y = y
        self.board = board
        self.load = load
        self.pheromone_per_run = 500
        self.id = Ant.counter
        self.log_message = ""
        
        self.path = []
    
    
    def pheromoneTrace(self):
        for i in self.path:
            self.board[i[0]][i[1]] += self.pheromone_per_run/len(self.path)
     
    
    def move(self):
        if self.board.checkBox(self.y, self.x, self.load):
            self.pheromoneTrace()
            self.board.event_happend = True
            self.log_message = str(self.id) + " SEND" + str(self.load) + " " + \
                               str(self.x) + " " + str(self.y)
            self.load = 0
        
        if self.board.checkEmptyLoad(self.y, self.x, self):
            self.board.event_happend = True
            self.load = self.board.getLoad()
            self.log_message = str(self.id) + " GET" + str(self.load) + " " + \
                               str(self.x) + " " + str(self.y)
        
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