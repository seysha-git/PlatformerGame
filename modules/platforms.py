import pygame as pg
from settings import *
from modules.items import Spike
from modules.items import Pow
import random as rd

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x,y, type="ground"):
        self._layer = PLATFORM_LAYER
        self.type = type
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet_platform.get_image(792, 0,70,70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class GroundPlatform(Platform):
    def __init__(self, game, x,y, type="ground"):
        super().__init__(game, x,y,type)
        self.groups = game.all_sprites, game.ground_platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = {
             "ground": self.game.spritesheet_platform.get_image(648,0,70,70),
             "half_ground": self.game.spritesheet_platform.get_image(576,432,70,70),
             "lava": self.game.spritesheet_platform.get_image(504, 0,70,30),
             "tresure": self.game.spritesheet_huds.get_image(146,147,44,40), 
        }
        self.image = self.images[type]
        self.image.set_colorkey("black")


class BackgroundPlatform(Platform):
    def __init__(self, game,x,y, type=""):
        super().__init__(game, x,y,type)
        self.groups = game.all_sprites, game.background_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = {
             "door_mid": self.game.spritesheet_platform.get_image(648, 432,70,70),
             "door_top": self.game.spritesheet_platform.get_image(648, 360,70,70),
             "cloud": self.game.spritesheet_items.get_image(0, 146,128,71), 
             "water": self.game.spritesheet_platform.get_image(504, 216,70,70),
             "flag_green":self.game.spritesheet_items.get_image(216,432,70,70), 
        }
        self.image = self.images[type]
        self.image.set_colorkey("black")

class WallPlatform(Platform):
    def __init__(self, game,x,y):
        super().__init__(game, x,y)
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet_platform.get_image(0,432,70,70)
        self.image.set_colorkey("black")
class RoofPlatform(Platform):
    def __init__(self, game,x,y):
        super().__init__(game, x,y)
        self.groups = game.all_sprites, game.roofs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet_platform.get_image(0,432,70,70)
        self.image.set_colorkey("black")
        

class JumpPlatform(Platform):
    def __init__(self, game, x,y, time):
        super().__init__(game, x,y)
        self.groups = game.all_sprites, game.jump_platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.time = time
        self.game = game
        self.image = self.game.spritesheet_platform.get_image(720,432,70,70)
        self.image.set_colorkey("black")
        self.spike_active = False


class MovingJumpPlatform(JumpPlatform):
    def __init__(self, game, x, y, time):
        super().__init__(game, x, y, time)
        self.direction = 1
        if rd.randrange(3) < POWER_COUNT:
            Pow(self.game, self)
    def horizontal_movement(self):
        self.rect.x += self.direction
        now = pg.time.get_ticks()
        if (now - self.time) // 1000 >= 3:
            self.direction *= -1
            self.time = now
                
        
        




