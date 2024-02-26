import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *




class Part1:
    def __init__(self, game):
        self.game = game
        self.check_point_active = False
        self.ground_length = 10
        self.water_length = 50

        self.scroll_timer = 0
        self.scroll_duration = 600  # Time in milliseconds for scrolling
    def background(self):
        BackgroundPlatform(self.game, 100, WIN_HEIGHT//2+28, "sign_left")
    def new(self): 
        self.scroll_time = 0
        for i in range(1,self.ground_length):
           GroundPlatform(self.game, i*70- 70, WIN_HEIGHT//2+100)
        for i in range(1, self.water_length):
            BackgroundPlatform(self.game, i*70- 70, WIN_HEIGHT-70, "water")
        self.check_point_1 = CheckPoint(self.game, 500, WIN_HEIGHT//2+28)
        self.background()
    def handle_collisions(self):
        hit = pg.sprite.spritecollide(self.game.player, self.game.check_points, True)
        if hit:
            self.game.check_point_active = True
            # Activate the scroll timer
            self.scroll_timer = pg.time.get_ticks()

    def update(self):
        self.handle_collisions()
        if self.game.check_point_active:
            current_time = pg.time.get_ticks()
            if current_time - self.scroll_timer < self.scroll_duration:
                print("active")
                self.game.move_screen()
            else:
                # Deactivate the check point after the timer expires
                self.game.check_point_active = False
                


        

        
        

