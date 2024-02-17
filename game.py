import pygame as pg
import sys
from settings import *
from modules.player import *
from modules.platform import *
from os import path
from utils import Spritesheet





class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
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
        self.portal = Platform(WIN_WIDTH-50, WIN_HEIGHT-500 -60, 50, 500, "green")

        self.all_sprites.add(self.ground)
        self.platforms.add(self.ground)
        self.portals.add(self.portal)
        self.all_sprites.add(self.portal)
    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "images")
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

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
       
        if self.player.rect.right >= WIN_WIDTH-100:
            self.player.pos.x -= abs(self.player.vel.x)
            for p in list(self.platforms) + list(self.portals):
                p.rect.x -= abs(self.player.vel.x)
        if self.player.rect.left <= 100:
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
        self.screen.fill("light blue")
        self.player.draw()
        self.all_sprites.draw(self.screen)
        self.draw_text(f"Level {0}/{5}", 35, "white", 50, 50)

        pg.display.flip()
    def show_start_screen(self):
        self.screen.fill("dark blue")
        self.draw_text(
            "Opplev 2.verdenskrig som en soldat",
            40,
            "white",
            WIN_WIDTH//4,
            200
        )

        self.draw_text(
            "W,A,S,D er kontroll tastene og SPACE for å hoppe.",
            30, 
            "white",
            WIN_WIDTH//4, 
            400
        )
        self.draw_text(
            "Press en key for å begynne",
            20,
            "white",
            WIN_WIDTH//4,
            600
        )
        pg.display.flip()
        self.wait_for_key()
    def show_over_screen(self):
        self.screen.fill("dark blue")
        self.draw_text(
            "Opplev 2.verdenskrig som en soldat",
            40,
            "white",
            WIN_WIDTH//4,
            200
        )

        self.draw_text(
            "W,A,S,D er kontroll tastene og SPACE for å hoppe.",
            30, 
            "white",
            WIN_WIDTH//4, 
            400
        )
        self.draw_text(
            "Press en key for å begynne",
            20,
            "white",
            WIN_WIDTH//4,
            600
        )
        pg.display.flip()
        self.wait_for_key()
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False 
                    self.running = False 
                if event.type == pg.KEYUP:
                    waiting = False



    def show_go_screen(self):
        ...
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.screen.blit(text_surface, text_rect)

        
