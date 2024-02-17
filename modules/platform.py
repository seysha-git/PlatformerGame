import pygame as pg 
from settings import WIN_WIDTH, WIN_HEIGHT

class Platform(pg.sprite.Sprite):
    def __init__(self, x,y,width,height, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

    ...