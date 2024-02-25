import pygame as pg
from settings import *
from modules.platforms import *
from modules.characters import *




class Part1:
    def __init__(self, game):
        self.game = game
        self.active = True
        self.ground_length = 10
        
    def new(self): 
        for i in range(1,self.ground_length):
           GroundPlatform(self.game, i*70- 70, WIN_HEIGHT-70)
        #for i in range(1,15):
         #  GroundPlatform(self.game, WIN_WIDTH//1.535 +70*i, WIN_HEIGHT-30, "liquid_water")
        #BackgroundPlatform(self.game, 20, 20, "cloud")
    def update(self):
        ...
        

