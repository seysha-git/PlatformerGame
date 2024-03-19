import pygame as pg
from settings import *
import random as rd
from utils import *

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



class Checkpoint(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.check_points
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.image = self.game.spritesheet_items.get_image(504,288,70,70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Spike(pg.sprite.Sprite):
    def __init__(self, game, x, y, type, time):
        self.groups = game.all_sprites, game.spikes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = [
            self.game.spritesheet_items.get_image(347, 0, 70, 70),
            self.game.spritesheet_items.get_image(0, 0, 0, 0)
        ]
        self.type = type
        self.image = self.images[self.type]
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_toggle_time = time
        self.toggle_time = 2500

    def update(self):
        now = pg.time.get_ticks()
        time_since_last_toggle = now - self.last_toggle_time

        # If 2 seconds have passed since the last toggle
        if time_since_last_toggle >= self.toggle_time:
            self.toggle_spike()  # Toggle the spike
            self.last_toggle_time = now  # Update the last toggle time

    def toggle_spike(self):
        self.type = 1 - self.type  # Toggle between 0 and 1
        self.image = self.images[self.type]
        self.image.set_colorkey("black")

