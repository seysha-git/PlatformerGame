import pygame as pg 
from settings import WIN_WIDTH, WIN_HEIGHT

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x,y, type="ground"):
        pg.sprite.Sprite.__init__(self)
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