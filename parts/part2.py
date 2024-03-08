import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *
from parts.levels import Level


class Part2(Level):
    def __init__(self, game):
        super().__init__(game)
        self.water_length = 14
        self.check_point_active_2 = False
        self.start_wall_move = False
    def background(self):
       for i in range(1,self.ground_length-2):
           GroundPlatform(self.game, i*70, -10, "half_ground")
    def new(self): 
        super().new()
        self.background()
    def update(self):
        super().update()


    