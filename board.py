from spawnpoint import Spawnpoint

class Board:    
    
    def __init__(self, filename):
        self.decrease_p = 0
        self.decrease_a = 1
        self.max_ants = 5
        self.max_pheromone = 1
        self.ticks = 0
        self.allMail = 0
        self.getDataFromFile(filename)
        
        
    def getDataFromFile(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            self.y = int(lines[0].split()[0])
            self.x = int(lines[0].split()[1])
            
            self.data = []
            self.box = list(map(int, lines[1].split()))
            self.spawns = []
            
            for line in lines[2:]:
                self.data.append([])
                
                for cell in line.split():
                    self.data[-1].append(cell)
                    
                    if self.data[-1][-1] == '0':
                        self.data[-1][-1] = 0
                    
                    len_whole = len(self.data) - 1
                    len_last = len(self.data[-1]) - 1
                    if isinstance(self[len_whole][len_last], str) and self[len_whole][len_last][0] == 'S':
                        self.spawns.append(Spawnpoint(len_whole, len_last, self))
            
            self.mail = []
            self.ants = []
            self.ant_map = [[0 for i in range(self.x)] for j in range(self.y)]
    
    
    def getMail(self, filename):
        with open(filename, 'r') as file:
            data = file.readlines()[0]
            
            for i in data.split():
                self.allMail += 1
                self.mail.append(int(i))
            
    
    def eventForTick(self, decreasing = True):
        
        self.max_pheromone = 1
        
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                
                if isinstance(self[i][j], float) or isinstance(self[i][j], int):
                    if (self[i][j] > self.max_pheromone):
                        self.max_pheromone = self[i][j]
        
        print(f"Ticks {self.ticks}")
        self.ticks += 1
        
        print(f'    Ants: {len(self.ants)}')
        print(f'    Max Pheromone: {"%.2f" % self.max_pheromone}')
        print(f'    Task: {self.allMail - len(self.mail) - len(self.ants)}/{self.allMail}')
        
        for spawnpoint in self.spawns:
            spawnpoint.process()
        
        for ant in self.ants:
            ant.process()
        
        if decreasing:
            self.decrease()
            
    
    def decrease(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if isinstance(self[i][j], float) or isinstance(self[i][j], int):
                    self[i][j] = max(0, self[i][j] - self.decrease_a)
                    self[i][j] *= 1 - self.decrease_p / 100
                    
    
    def getValidNeibours(self, y, x):
        neighbours = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
        ans = []
        for i in range(len(neighbours)):
            if 0 <= neighbours[i][0] < self.y and 0 <= neighbours[i][1] < self.x and \
                (isinstance(self[neighbours[i][0]][neighbours[i][1]], float) or \
                    isinstance(self[neighbours[i][0]][neighbours[i][1]], int)):
                if self.ant_map[neighbours[i][0]][neighbours[i][1]] == 0:
                    ans.append(neighbours[i])
        return ans

    
    def checkBox(self, y, x, load):
        neighbours = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
        for i in range(len(neighbours)):
            if 0 <= neighbours[i][0] < self.y and 0 <= neighbours[i][1] < self.x and \
                isinstance(self[neighbours[i][0]][neighbours[i][1]], str) and \
                    self[neighbours[i][0]][neighbours[i][1]][0] == 'B':
                if (self.box[int(self[neighbours[i][0]][neighbours[i][1]][1:])-1] == load):
                    return True
        return False
    
    
    def getLoad(self):
        return self.mail.pop(0)
                
    
    def __getitem__(self, item):
        if isinstance(item, int):
            if item < -self.y or item >= self.y:
                raise IndexError("Index of bounds")
            item =  item + self.y if item < 0 else item
            return self.data[item]
        raise TypeError("Index must be int")     