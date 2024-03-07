import pygame as pg
from settings import *

class PlatItem(pg.sprite.Sprite):
    def __init__(self, game, plat, type="gems"):
        self._layer = POW_LAYER
        self.game = game
        self.plat = plat
        self.image = self.game.spritesheet_items.get_image(347,0,70,70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top


class Booster(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self.groups = game.all_sprites, game.boosters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = [
            self.game.spritesheet_items.get_image(504,216,70,70),
            self.game.spritesheet_items.get_image(491,0,70,70)
        ] 
        self.active_image = 0
        self.image = self.images[self.active_image]
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def animate(self):
        print("animate")
        if self.active_image == 0:
            self.active_image = 1
        elif self.active_image == 1:
            self.active_image = 0
    
class Pow(PlatItem):
    def __init__(self, game, plat,type="gems"):
        super().__init__(game, plat, type)
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.type = type
        self.image = self.game.spritesheet_items.get_image(144,362,70,70)
        self.image.set_colorkey("black")

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        self.rect.centerx = self.plat.rect.centerx
        if not self.game.jump_platforms.has(self.plat):
            self.kill()
class Spike(PlatItem):
    def __init__(self, game, plat, time):
        super().__init__(game, plat)
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.spikes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.time = time
        self.image = self.game.spritesheet_items.get_image(347,0,70,70)
        self.image.set_colorkey("black")
    def update(self):
        now = pg.time.get_ticks()
        if (now-self.time) // 1000 > 2:
            self.kill()
            self.time = now


#class CheckPoint(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.check_points
        pg.sprite.Sprite.__init__(self, self.groups)
        #self.game = game
        #self.images = [
        #    self.game.spritesheet_items.get_image(432,288,70,70)
        #     self.game.spritesheet_items.get_image(432,216,70,70)
        #] 
        #self.active_image = 0
        #self.image = self.images[self.active_image]
        #self.image.set_colorkey("black")
        #self.rect = self.image.get_rect()
        #self.rect.x = x
        #self.rect.y = y