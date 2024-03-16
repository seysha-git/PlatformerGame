import pygame as pg
import math
from settings import *
import random as rd


class Bullet(pg.sprite.Sprite):
     def __init__(self, game):
        self.game = game
        self.image = self.game.spritesheet_items.get_image(0, 553,19,20)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
     def move(self):
        pass

     def collided(self, other_rect):
        return self.rect.colliderect(other_rect)

class PlayerBullet(Bullet):
    def __init__(self, game, x, y, speed, targetx,targety):
        super().__init__(game)
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.player_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
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
        hit = pg.sprite.spritecollide(self, self.game.walls, False)
        if hit:
            self.kill()


class CourseBullet(Bullet):
    def __init__(self, game):
        super().__init__(game)
        self.groups = game.all_sprites, game.course_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.spritesheet_items.get_image(0,553,19,14)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = rd.randint(WIN_WIDTH-250, WIN_WIDTH-200)
        self.rect.y = 60+70
        self.speed = rd.randint(1,4)
    def move(self):
        self.rect.y += 5
    def draw(self):
        pg.draw.rect(self.game.screen, "red", (300,300,50,50))
    def update(self):
        self.move()
        self.check_colission()
    def check_colission(self):
        hit = pg.sprite.spritecollide(self, self.game.ground_platforms, False)
        hit_player = pg.sprite.collide_mask(self, self.game.game_ground.player)
        #hit_jump_platform = pg.sprite.spritecollide(self, self.game.jump_platforms, False)
        if hit:
            self.kill()
        if hit_player:
            self.kill()
            self.game.player.health -= 5


