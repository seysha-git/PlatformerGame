import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *




class Part1:
    def __init__(self, game):
        self.game = game
        self.check_point_active = False
        self.ground_length = 10
        self.water_length = 50
        
    def new(self): 
        self.scroll_time = 0
        for i in range(1,self.ground_length):
           GroundPlatform(self.game, i*70- 70, WIN_HEIGHT//2+100)
        for i in range(1, self.water_length):
            BackgroundPlatform(self.game, i*70- 70, WIN_HEIGHT-70, "water")
        self.check_point_1 = CheckPoint(self.game, 500, WIN_HEIGHT//2+28)
        #for i in range(1,15):
         #  GroundPlatform(self.game, WIN_WIDTH//1.535 +70*i, WIN_HEIGHT-30, "liquid_water")
        #BackgroundPlatform(self.game, 20, 20, "cloud")
    def update(self):
        hit = pg.sprite.spritecollide(self.game.player, self.game.check_points, True)
        if hit:
            self.game.check_point_active = True 
        if self.game.check_point_active:
            self.now = pg.time.get_ticks()
            if self.now - self.scroll_time < 1500:
                print("move screen")
                self.game.move_screen(600)
            elif self.now > 1500:
                self.game.check_point_active = False
                self.now = self.scroll_time


        

        
        

