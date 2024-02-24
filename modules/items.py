import pygame as pg
from settings import *
class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat,type="gems"):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.plat = plat
        self.image = self.game.spritesheet_items.get_image(144,362,70,70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5


    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.jump_platforms.has(self.plat):
            self.kill()



