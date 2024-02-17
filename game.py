import pygame as pg
import sys
from settings import *
from modules.player import *
from modules.platform import *





class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.p1_active = True
        self.p2_active = False 
        self.p3_active = False 
        ...
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.portals = pg.sprite.Group()

        self.player = Player(self)
        self.p1()
        self.all_sprites.add(self.player)
        self.run()
    def p1(self):
        
        self.ground =  Platform(0, WIN_HEIGHT-60, WIN_WIDTH*2, 60, "black")
        self.portal = Platform(WIN_WIDTH-100, WIN_HEIGHT-500 -60, 50, 500, "green")

        self.all_sprites.add(self.ground)
        self.platforms.add(self.ground)
        self.portals.add(self.portal)
        self.all_sprites.add(self.portal)
        
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def update(self):
        self.all_sprites.update()
        if self.player.rect.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

       
        if self.player.rect.right >= WIN_WIDTH - 200:
            #print("move")
            self.player.pos.x -= abs(self.player.vel.x)
            for p in list(self.platforms) + list(self.portals):
                p.rect.x -= abs(self.player.vel.x)
        elif self.player.rect.left <= 200:
            #print("move")
            self.player.pos.x += (abs(self.player.vel.x))
            for p in list(self.platforms) + list(self.portals):
                p.rect.x += abs(self.player.vel.x)
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False 
                print("finished")
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

            

    def draw(self):
        if self.p1_active:
            color = "light blue"
        if self.p2_active:
            color = "white"
        self.screen.fill(color)
        #self.platforms.draw(self.screen)
        self.all_sprites.draw(self.screen)
        

        pg.display.flip()
    def show_start_screen(self):
        ...
    def show_over_screen(self):
        ...
    def show_go_screen(self):
        ...
        
