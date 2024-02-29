import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *



class Level:
    def __init__(self, game) -> None:
        self.scroll_timer = 0
        self.scroll_duration = 1300
        self.game = game
        self.water_length = 15
    def handle_checkpoint_collisions(self):
        hit = pg.sprite.spritecollide(self.game.player, self.game.check_points, True)
        if hit:
            print("hit")
            self.game.check_point_active = True
            self.game.scroll_distance = 400
            # Activate the scroll timer
            self.scroll_timer = pg.time.get_ticks()
    def background(self):
        for i in range(1, self.water_length):
            BackgroundPlatform(self.game, i*70+ 350, WIN_HEIGHT-70, "water")
    def new(self):
        for i in range(1,8):
          GroundPlatform(self.game, i*70- 70, WIN_HEIGHT-70)
        for i in range(10):
            PortalPlatform(self.game, 0, 70*i+35)
        for i in range(10):
            PortalPlatform(self.game, WIN_WIDTH-70, 70*i+35)
    def update(self):
        self.handle_checkpoint_collisions()
        if self.game.check_point_active:
            current_time = pg.time.get_ticks()
            # if current_time - self.scroll_timer < self.scroll_duration:
            if self.game.scroll_distance > 0:
                self.game.move_screen()
            else:
                # Deactivate the check point after the timer expires
                self.game.check_point_active = False
                self.check_point_active_1 = True
        
