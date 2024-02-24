import pygame as pg
from settings import *
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
        self.jump_platform_cordinates = [
            (1100,600),
            (1400,400),
            (1600,300),
            (1200, 500)

        ]
    
    def background(self):
        BackgroundPlatform(self.game, WIN_WIDTH*1.2, WIN_HEIGHT//4, "cloud")
        BackgroundPlatform(self.game, WIN_WIDTH*1.3, WIN_HEIGHT//2, "cloud")
        BackgroundPlatform(self.game, WIN_WIDTH*1.6, WIN_HEIGHT//1, "cloud")

        BackgroundPlatform(self.game, WIN_WIDTH//2.5,WIN_HEIGHT-70*2,"sign_left")
    def new(self):
        self.enemies_timer = 0 
        for i in range(1,20):
            GroundPlatform(self.game, 1850 + 50 + i*70, WIN_HEIGHT//2)
        for i in range(1,20):
            PortalPlatform(self.game, WIN_WIDTH*1.5,70*i- 1000)
        for pos in self.jump_platform_cordinates:
            JumpPlatform(self.game, pos[0],pos[1])
        #self.background()
        self.update() 
        
        
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
        if (now - self.enemies_timer) // 1000 > 3:
            self.enemies_timer = now 
            i = 0
            while i < 3:
                el = EnemyFly(self.game)
                hit = pg.sprite.spritecollide(el, self.game.enemies, False)
                if hit:
                    for n in hit:
                        if n != el:
                            print("collided, try again")
                            el.kill()
                    else:       
                        i += 1
           

        
            

    
 