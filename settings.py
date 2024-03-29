import pygame as pg
import os
pg.init()


WIN_WIDTH = 1500
WIN_HEIGHT = 900

SCROLLING_TEXT_FONT = pg.font.Font("freesansbold.ttf", 24)
MENU_FONT = pg.font.Font("freesansbold.ttf", 24)

TITLE = "WW2 Story gmae"
FONT_NAME = 'arial'

SPRITESHEET_CHAR = "p1_spritesheet.png"
SPRITESHEET_PLATFORM = "tiles_spritesheet.png"
SPRITESHEET_ITEMS = "items_spritesheet.png"
SPRITESHEET_ENEMIES = "enemies_spritesheet.png"
SPRITESHEET_HUD = "hud_spritesheet.png"
SPRITESHEET_PRINCESS = "p3_spritesheet.png"

SCREEN_SCROLL_SPEED = 10

GAME_DESCRIPTION_1 = "- Målet med spillet er å komme seg gjennom alle nivåene"
GAME_DESCRIPTION_2 = "- Målet med spillet er å komme seg gjennom alle nivåene"
GAME_DESCRIPTION_3 = "- Målet med spillet er å komme seg gjennom alle nivåene"
GAME_DESCRIPTION_4 = "- Målet med spillet er å komme seg gjennom alle nivåene"

BOOST_POWER = 60
POWER_COUNT = 1


PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
ENEMIES_LAYER = 2


BULLET_WIDTH, BULLET_HEIGHT = 20,20


FPS = 60

#Player properaties
MAIN_CHAR_COLOR = "white"
MAIN_CHAR_WIDTH, MAIN_CHAR_HEIGHT = 50,100
MAIN_ACC = 5
MAIN_FRICTION = 0.12
MAIN_GRAVITY = 0.8
MAIN_JUMP_VEL = 15

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self,x,y,width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        return image












































































































