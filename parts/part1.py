import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *
from parts.levels import Level


class Part1(Level):
    def __init__(self, game):
        super().__init__(game)
        self.water_length = 14
        self.check_point_active_2 = False
        self.start_wall_move = False
    def background(self):
        for i in range(1,18): # Nest nederste taket
            WallPlatform(self.game, i*70- 70, WIN_HEIGHT-320)
        for i in range(1,5): #dør gulvet
            WallPlatform(self.game,WIN_WIDTH-380, 70*i+270)
        for i in range(1,4):
            GroundPlatform(self.game, WIN_WIDTH-590 + 70*i, WIN_HEIGHT//4+50)
        for i in range(1,10 ):
            WallPlatform(self.game, 420, 70*i-120)
        for i in range(1,6):
            GroundPlatform(self.game, 70*i, 360)

        JumpPlatform(self.game, WIN_WIDTH-140, WIN_HEIGHT-350, 0)
        JumpPlatform(self.game, WIN_WIDTH-140, WIN_HEIGHT-150, 0)
        JumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-290, 0)
        JumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-450, 0)
        JumpPlatform(self.game, WIN_WIDTH-140, WIN_HEIGHT-520, 0)
        JumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-620, 0)
    def new(self): 
        super().new()
        #self.spring = Booster(self.game, 390, WIN_HEIGHT-150)
        self.background()
    def update(self):
        super().update()


    
    
        

