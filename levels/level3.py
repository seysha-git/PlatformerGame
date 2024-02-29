import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *
from levels.level import Level


class Level3(Level):
    def __init__(self, game):
        super().__init__(game)

    def background(self):
        ...
    def new(self): 
        #super.new()
        self.scroll_time = 0
        #self.check_point_2 = CheckPoint(self.game, 2000, WIN_HEIGHT-140)
        self.background()
    def chekpoint_2_hit(self):
        if pg.sprite.collide_rect(self.game.player, self.check_point_2):
            print("hello")
    def update(self):
        super().update()
        #self.chekpoint_2_hit()
