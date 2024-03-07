import pygame as pg
import math
from settings import *

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, color, x, y, width, height, speed, targetx,targety):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.spritesheet_items.get_image(0, 553,19,20)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.direction = 'E'
        self.speed = speed
        angle = math.atan2(targety-y, targetx-x)
        self.dx = math.cos(angle)*speed
        self.dy = math.sin(angle)*speed

        



    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    def update(self):
        self.move()
        self.check_colission()
    def check_colission(self):
        hits = pg.sprite.spritecollide(self, self.game.enemies, True) #or pg.sprite.spritecollide(self, self.game.ground_platforms, True)
        if hits:
            self.kill()
        
        
