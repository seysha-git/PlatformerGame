import pygame as pg
from settings import *
from utils import *
from modules.items import Pow
import random as rd
class GroundPlatform(pg.sprite.Sprite):
    curr = 0
    def __init__(self, game, x,y, type="ground"):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.ground_platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = {
             "ground":self.game.spritesheet_platform.get_image(792, 0,70,70),
             "sign_left": self.game.spritesheet_platform.get_image(288, 216,70,70),
             "cloud": self.game.spritesheet_items.get_image(0, 146,128,71), 
             "green_flag":self.game.spritesheet_items.get_image(216,432,70,70),
             "button_green":self.game.spritesheet_items.get_image(419, 0,70,70),
             "button_green_pressed":self.game.spritesheet_items.get_image(418, 144,70,70),
             "lava": self.game.spritesheet_platform.get_image(504,0,70,70),
             "stone_wall": self.game.spritesheet_platform.get_image(72,288,70,70),
             "stone_jump": self.game.spritesheet_platform.get_image(144,144,70,70),
             
        }
        self.image = self.images[type]
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class BackgroundPlatform(pg.sprite.Sprite):
    def __init__(self, game,x,y, type=""):
        self.groups = game.all_sprites, game.background_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = {
             "ground":self.game.spritesheet_platform.get_image(792, 0,70,70),
             "sign_left": self.game.spritesheet_platform.get_image(288, 216,70,70),
             "cloud": self.game.spritesheet_items.get_image(0, 146,128,71), 
             "green_flag":self.game.spritesheet_items.get_image(216,432,70,70),
             "button_green":self.game.spritesheet_items.get_image(419, 0,70,70),
             "button_green_pressed":self.game.spritesheet_items.get_image(418, 144,70,70),
             "lava": self.game.spritesheet_platform.get_image(504,0,70,70),
             "stone_wall": self.game.spritesheet_platform.get_image(72,288,70,70),
             "stone_jump": self.game.spritesheet_platform.get_image(144,144,70,70),
             
        }
        self.image = self.images[type]
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PortalPlatform(pg.sprite.Sprite):
    def __init__(self, game,x,y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.portals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet_platform.get_image(72,288,70,70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class JumpPlatform(pg.sprite.Sprite):
    curr = 0
    def __init__(self, game,x,y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.jump_platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet_platform.get_image(144,144,70,70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if rd.randrange(3) < POWER_COUNT:
            Pow(self.game, self)
            self.curr += 1

class MovingJumpPlatform(JumpPlatform):
    def __init__(self, game, x, y, time):
        super().__init__(game, x, y)
        self.time = time
        self.direction = 1
    def horizontal_movement(self):
        self.rect.x += self.direction
        now = pg.time.get_ticks()
        if (now - self.time) // 1000 >= 3:
            self.direction *= -1
            self.time = now
                
        
        




