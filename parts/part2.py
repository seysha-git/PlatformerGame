import pygame as pg
from settings import *
from modules.platform import Platform
import random as rd


class Part2:
    def __init__(self, game):
        self.game = game
        self.check_point_active = False
        self.hit = False
        self.jump_platform_cordinates = [
            (1000,700),
            (1320,750),
            (1200,700),
            (1430,750),
            (1650,650),
            (1760,750),
            (2100,800),
            (2150, 500)
        ]

        self.new()
    
        
    def new(self):  
        self.grounds =  [Platform(self.game, 2100 + 50 + i*70, WIN_HEIGHT//2) for i in range(1,15)]
        self.jump_platforms = self.create_jump_platforms()

        self.cloud = Platform(self.game, WIN_WIDTH*1.5, WIN_HEIGHT//4, "cloud")
        self.button_green_pressed = Platform(self.game, WIN_WIDTH//1.5,WIN_HEIGHT-70*2, "button_green_pressed")
        self.button_green = Platform(self.game, WIN_WIDTH//1.5,WIN_HEIGHT-70*2, "button_green")
        self.sign_left = Platform(self.game, WIN_WIDTH//2.5,WIN_HEIGHT-70*2,"sign_left")
        

        self.sprite_items = [self.sign_left, self.cloud]
        self.check_points = [self.button_green]

    def create_jump_platforms(self):
        jump_platforms = []
        for pos in self.jump_platform_cordinates:
            jump_platforms.append(Platform(self.game, pos[0],pos[1],"stone_jump"))
        return jump_platforms
    
    def add_items(self):
        self.update()
        items = []
        for item in self.sprite_items + self.jump_platforms + self.grounds + self.check_points:
            self.game.all_sprites.add(item)
            if item in self.check_points:
                self.game.check_points.add(item)
            if item in self.jump_platforms + self.grounds + self.sprite_items:
                self.game.platforms.add(item)
        
    def update(self):
        
        if self.check_point_active:  # Check if the button has been pressed
            self.game.move_screen(1200)
            self.check_point_active = False
            self.hit = True
        if pg.sprite.collide_rect(self.game.player, self.check_points[0]) and self.check_point_active == False:
            print("pressed")
            self.button_pressed()
        

    def button_pressed(self):
        self.check_points[0].image = self.button_green_pressed.image
        self.check_point_active = True
        
        #self.game.info_screen()
    def deactivate(self):
        self.active = False

    def events(self):
        for event in pg.event.get():
            ...