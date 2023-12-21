from board import Board
from ant import Ant
from color import fadeColor

import time
import pygame


class Window:
    
    def __init__(self, map, mail, scale, console = False):
        self.delay = 0
        self.console = console
        self.scale = scale
        
        self.board = Board(map)
        self.board.getMail(mail)
    
    
    def setRegFieldColor(self, i, j):
        color = fadeColor(mix = (self.board[i][j] + Ant.base_prob) / (self.board.max_pheromone + Ant.base_prob))
        pygame.draw.rect(self.surface, color, (j * self.scale + 2, i * self.scale + 2, self.scale - 2, self.scale - 2))
        
    
    def setSendFieldColor(self, i, j):
        color = '#FF0000'
        pygame.draw.rect(self.surface, color, (j * self.scale + 2, i * self.scale + 2, self.scale - 2, self.scale - 2))
        text = self.font.render(str(self.board.box[int(self.board[i][j][1:]) - 1]), True, 'black')
        self.surface.blit(text, [j * self.scale + self.scale // 2 - 6, i * self.scale + self.scale // 2 - 6]) 
        
        
    def setBlockFieldColor(self, i, j):
        color = '#000000'
        pygame.draw.rect(self.surface, color, (j * self.scale + 2, i * self.scale + 2, self.scale - 2, self.scale - 2))
        
        
    def setSpawnFieldColor(self, i, j):
        color = '#FFFFFF'
        pygame.draw.rect(self.surface, color, (j * self.scale + 2, i * self.scale + 2, self.scale - 2, self.scale - 2))
        text = self.font.render("S", True, 'black')
        self.surface.blit(text, [j * self.scale + self.scale // 2 - 6, i * self.scale + self.scale // 2 - 6] )
        
    
    def setAntColor(self, i, j):
        pygame.draw.rect(self.surface, 'black', (j * self.scale + self.scale / 2 - self.scale // 5, \
                         i * self.scale + self.scale / 2 - self.scale // 5, self.scale // 2, self.scale // 2))
    
    
    def setAntMailColor(self, ant):
        text = self.fontsmall.render(str(ant.load), True, 'white')
        self.surface.blit(text, [ant.x * self.scale + self.scale // 2, ant.y * self.scale + self.scale // 2 - 2] )             
    
    
    def boardRun(self):
        for i in range(self.board.y):         
            for j in range(self.board.x):

                if isinstance(self.board[i][j], float) or isinstance(self.board[i][j], int):
                    self.setRegFieldColor(i, j)
                            
                elif (self.board[i][j][0] == 'B'):
                    self.setSendFieldColor(i, j)
                            
                elif (self.board[i][j] == 'x'):
                    self.setBlockFieldColor(i, j)
                        
                elif (self.board[i][j] == 'S'):
                    self.setSpawnFieldColor(i, j)
                
                if self.board.ant_map[i][j] == 1:
                    self.setAntColor(i, j)
                 
        for ant in self.board.ants:
            self.setAntMailColor(ant)
            
        [pygame.draw.line(self.surface, pygame.Color('dimgray'), (x, 0), (x, self.height)) for x in range(0, self.width, self.scale)]
        [pygame.draw.line(self.surface, pygame.Color('dimgray'), (0, y), (self.width, y)) for y in range(0, self.height, self.scale)]
                
        self.board.eventForTick()
                
        pygame.display.flip()
        time.sleep(self.delay)
    
    
    def run(self):
        self.width = self.scale * self.board.x
        self.height = self.scale * self.board.y

        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        
        self.font = pygame.font.Font(None, 30)
        self.fontsmall = pygame.font.Font(None, 15)
            
        while True:    
                
            self.surface.fill(pygame.Color('white'))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                
            if len(self.board.ants) <= 0 and self.board.ticks > 0:
                self.boardRun()
                break
                
            self.boardRun()
            
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break 