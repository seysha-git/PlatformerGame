import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((MAIN_CHAR_WIDTH, MAIN_CHAR_HEIGHT))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect.center = (WIN_WIDTH//2, WIN_HEIGHT-MAIN_CHAR_HEIGHT/2)
        self.pos = vec(WIN_WIDTH//2, WIN_HEIGHT//2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -MAIN_JUMP_VEL
    def update(self):
        self.acc = vec(0,MAIN_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            self.acc.x = MAIN_ACC
        if keys[pg.K_a] and self.rect.x > 0:
            self.acc.x = -MAIN_ACC
        self.acc.x += self.vel.x * -MAIN_FRICTION
        self.vel += self.acc 
        self.pos += self.vel + 0.5*self.acc
        
        self.rect.midbottom = self.pos
    



