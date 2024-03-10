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



class Switch(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self.groups = game.all_sprites, game.switches
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = [
            self.game.spritesheet_items.get_image(504,216,70,70),
            self.game.spritesheet_items.get_image(491,0,70,70)
        ] 
        self.active_image = 0
        self.draw()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        self.image = self.images[self.active_image]
        self.image.set_colorkey("black")
    def update(self):
        hit = pg.sprite.collide_mask(self, self.game.player)
        if hit:
            self.animate()
            for plat in self.game.ground_platforms:
                if plat.type == "wood_box":
                    if plat.rect.y <= WIN_HEIGHT-375:
                        plat.rect.y += 3
            
    def animate(self):
        print("animate")
        if self.active_image == 0:
            self.active_image = 1
       ## elif self.active_image == 1:
        #    self.active_image = 0
        self.draw()
        

class Spike(pg.sprite.Sprite):
    def __init__(self, game, x,y, type):
        self.groups = game.all_sprites, game.spikes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = [
            self.game.spritesheet_items.get_image(347,0,70,70),
            pg.transform.flip(self.game.spritesheet_items.get_image(347,0,70,70), True, False)
        ]
        self.image = self.images[type]
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        ...
        #now = pg.time.get_ticks()
        #if (now-self.time) // 1000 > 2:
        #    self.kill()
        #    self.time = now

class Switch(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self.groups = game.all_sprites, game.switches
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = [
            self.game.spritesheet_items.get_image(504,216,70,70),
            self.game.spritesheet_items.get_image(491,0,70,70)
        ] 
        self.active_image = 0
        self.draw()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        self.image = self.images[self.active_image]
        self.image.set_colorkey("black")
    def update(self):
        hit = pg.sprite.collide_mask(self, self.game.player)
        if hit:
            self.animate()
            for plat in self.game.ground_platforms:
                if plat.type == "wood_box":
                    if plat.rect.y <= WIN_HEIGHT-375:
                        plat.rect.y += 3
            
    def animate(self):
        print("animate")
        if self.active_image == 0:
            self.active_image = 1
       ## elif self.active_image == 1:
        #    self.active_image = 0
        self.draw()