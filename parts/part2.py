import pygame as pg
from settings import *
from modules.items import *
from modules.characters import *
from modules.platforms import *
import random as rd


class Part2:
    def __init__(self, game):
        self.game = game
        self.check_point_active = False
        self.start_wall_move = False
        self.hit = False
        self.portal_closed = False
        self.vel = 1
        self.jump_platform_cordinates = [
            (1000,600),
            (850, 500),
            (990, 200),
            (1100,188),
            (1200,100),
            (1300,530),
            (1300,400),

        ]
    
    def background(self):
        BackgroundPlatform(self.game, WIN_WIDTH*1.2, WIN_HEIGHT//4, "cloud")
        BackgroundPlatform(self.game, WIN_WIDTH*1.3, WIN_HEIGHT//2, "cloud")
        BackgroundPlatform(self.game, WIN_WIDTH*1.6, WIN_HEIGHT//1, "cloud")

        BackgroundPlatform(self.game, WIN_WIDTH//2.5,WIN_HEIGHT-70*2,"sign_left")
    def new(self):
        self.enemies_timer = 0 
        self.platform_timer = 0
        for i in range(1,10):
            GroundPlatform(self.game, 1500 + 50 + i*70, WIN_HEIGHT//2)
        for pos in self.jump_platform_cordinates:
            rand = rd.randint(0,1)
            if rand:
                MovingJumpPlatform(self.game,pos[0],pos[1], self.platform_timer)
            else:
                JumpPlatform(self.game, pos[0], pos[1], self.platform_timer)
        #self.background()
        self.update() 
        
        
    def move_portal_down(self):
        for item in self.game.portals:
            if not self.portal_closed:
                item.rect.y += 0.5
        self.check_portal_closed()
   
    
    def move_plat(self):
        for plat in self.game.jump_platforms:
            if isinstance(plat,MovingJumpPlatform):
                plat.horizontal_movement()
                if self.game.player.on_moving_plat:
                    player = self.game.player 
                    player.rect.x += plat.direction
            
    def check_portal_closed(self):
        for item in self.game.portals:
            if pg.sprite.spritecollide(item, self.game.ground_platforms, False):
                self.portal_closed = True
    def create_enemies(self):
        now = pg.time.get_ticks()
        if (now - self.enemies_timer) // 1000 > 3:
            self.enemies_timer = now 
            el = EnemyFly(self.game, rd.randint(900,1000), rd.randint(WIN_HEIGHT, WIN_HEIGHT + 200))
                
    def update(self):
        self.move_plat()
        self.move_portal_down()
        #self.create_enemies()

        
           

        
            

    
 