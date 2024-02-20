import pygame as pg
from settings import *
from modules.platform import Platform




class Part1:
    def __init__(self, game):
        self.game = game
        self.active = True
        self.new()
        
    def new(self): 
        self.grounds =  [Platform(self.game, i*70- 70, WIN_HEIGHT-70) for i in range(1,15)]
        self.portal_wall = [Platform(self.game, WIN_WIDTH//1.5,70*i- 1000,"stone_wall") for i in range(1,20)]
        #self.green_flag = Platform(self.game, WIN_WIDTH//1.8,WIN_HEIGHT-70*2,"sign_left")
        self.cloud = Platform(self.game, WIN_WIDTH//2, 80, "cloud")
        
        #self.button_green = Platform(self.game, WIN_WIDTH//1.05,WIN_HEIGHT-70*2,"button_green")
       # self.check_point = Platform(WIN_WIDTH+40,WIN_HEIGHT-60-1,game)
        self.sprite_items = [self.cloud]#self.button_green]
        #self.game.portals.add(self.portal)
        #self.game.checkpoints.add(self.check_point)
    def add_items(self):
        for el in self.grounds:
            self.game.all_sprites.add(el)
            self.game.platforms.add(el)
        for item in self.sprite_items:
            self.game.all_sprites.add(item)
            self.game.platforms.add(item)
        for wall in self.portal_wall:
            self.game.all_sprites.add(wall)
            self.game.portals.add(wall)
    def deactivate(self):
        self.active = False

    def events(self):
        for event in pg.event.get():
            ...