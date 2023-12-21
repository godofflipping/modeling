from spawnpoint import Spawnpoint

import logging as log


class Board:    
    
    def __init__(self, filename):
        self.decrease_p = 0
        self.decrease_a = 1
        self.max_ants = 2
        self.max_pheromone = 1
        self.event_happend = False
        self.ticks = 0
        self.all_mail = 0
        self.event_id = 0
        self.is_start = True
        self.getDataFromFile(filename)
        
        log.basicConfig(level=log.INFO, filename="sim.log", \
                        filemode="w", format="%(message)s")
        
        log.info("ID T IDR EventType X Y")


    def eventHappend(self, item):
        self.event_id += 1
        log.info(str(self.event_id) + f" {self.ticks} " + item.log_message)
        self.event_happend = False

        
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
                        self.spawns.append(Spawnpoint(len_last, len_whole, self))
            
            self.mail = []
            self.ants = []
            self.ant_map = [[0 for i in range(self.x)] for j in range(self.y)]
    
    
    def getMail(self, filename):
        with open(filename, 'r') as file:
            data = file.readlines()[0]
            
            for i in data.split():
                self.all_mail += 1
                self.mail.append(int(i))
            
    
    def eventForTick(self, decreasing = True):
        self.max_pheromone = 1
        
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                
                if isinstance(self[i][j], float) or isinstance(self[i][j], int):
                    if (self[i][j] > self.max_pheromone):
                        self.max_pheromone = self[i][j]
        
        self.ticks += 1
        
        for spawnpoint in self.spawns:
            spawnpoint.run()    
        
        for ant in self.ants:
            ant.move()
            if self.event_happend:
                self.eventHappend(ant)
        
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
        answer = []
        
        for i in range(len(neighbours)):
            if 0 <= neighbours[i][0] < self.y and 0 <= neighbours[i][1] < self.x and \
                (isinstance(self[neighbours[i][0]][neighbours[i][1]], float) or \
                    isinstance(self[neighbours[i][0]][neighbours[i][1]], int)):
                
                if self.ant_map[neighbours[i][0]][neighbours[i][1]] == 0:
                    answer.append(neighbours[i])
        
        return answer

    
    def checkBox(self, y, x, load):
        neighbours = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
        
        for i in range(len(neighbours)):
            if 0 <= neighbours[i][0] < self.y and 0 <= neighbours[i][1] < self.x and \
                isinstance(self[neighbours[i][0]][neighbours[i][1]], str) and \
                    self[neighbours[i][0]][neighbours[i][1]][0] == 'B':
                
                if (self.box[int(self[neighbours[i][0]][neighbours[i][1]][1:]) - 1] == load):
                    return True
        
        return False
    
    
    def checkEmptyLoad(self, y, x, ant):
        neighbours = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
        
        for i in range(len(neighbours)):
            if 0 <= neighbours[i][0] < self.y and 0 <= neighbours[i][1] < self.x and \
                isinstance(self[neighbours[i][0]][neighbours[i][1]], str) and \
                    self[neighbours[i][0]][neighbours[i][1]] == 'S':
                
                if ant.load == 0:
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