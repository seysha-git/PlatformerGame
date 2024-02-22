import pygame as pg
from settings import *
from modules import *
import random as rd


class Part2:
    def __init__(self, game):
        self.game = game
        self.check_point_active = False
        self.start_wall_move = False
        self.hit = False
        self.portal_closed = False
        self.jump_platform_cordinates = [
            (1100,600),
            (1400,400),
            (1600,300),

        ]
    
    def background(self):
        Platform(self.game, WIN_WIDTH*1.2, WIN_HEIGHT//4, "cloud")
        Platform(self.game, WIN_WIDTH*1.3, WIN_HEIGHT//2, "cloud")
        Platform(self.game, WIN_WIDTH*1.6, WIN_HEIGHT//1, "cloud")

        Platform(self.game, WIN_WIDTH//2.5,WIN_HEIGHT-70*2,"sign_left")
    def new(self):  
        for i in range(1,20):
            Platform(self.game, 1850 + 50 + i*70, WIN_HEIGHT//2)
        for i in range(1,20):
            Platform(self.game, WIN_WIDTH*1.5,70*i- 1000,"stone_wall")
        for pos in self.jump_platform_cordinates:
            Platform(self.game, pos[0],pos[1],"stone_jump")
        self.background()
        self.enemies_timer = 0
    def create_jump_platforms(self):
        jump_platforms = []
        for pos in self.jump_platform_cordinates:
            jump_platforms.append(Platform(self.game, pos[0],pos[1],"stone_jump"))
        return jump_platforms
    
        
    def move_portal_down(self):
        for item in self.portal_wall:
            item.rect.y += 2
        self.check_portal_closed()
    def check_portal_closed(self):
        for item in self.portal_wall:
            if pg.sprite.spritecollide(item, self.grounds, False):
                self.portal_closed = True

    def update(self):
        now = pg.time.get_ticks()
        if now - self.enemies_timer > 5000 + rd.choice([-1000,-500,0,500,1000]):
            self.enemies_timer = now 
            print("create enemy")
            Enemy(self.game)

        
 