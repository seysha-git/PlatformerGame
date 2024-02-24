import pygame as pg
from settings import *
from modules.platforms import *
from modules.characters import *




class Part1:
    def __init__(self, game):
        self.game = game
        self.active = True
        self.ground_length = 15
        self.portal_length = 40
        
    def new(self): 
        for i in range(1,self.ground_length):
           GroundPlatform(self.game, i*70- 70, WIN_HEIGHT-70)
        for i in range(1,20):
            GroundPlatform(self.game, WIN_WIDTH//1.5,70*i- 1000,"stone_wall")
        #BackgroundPlatform(self.game, 20, 20, "cloud")
    def update(self):
        ...
        

