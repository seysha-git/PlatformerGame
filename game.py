import pygame as pg
import sys
from settings import *
from modules.characters import *
from os import path
from utils import Spritesheet
from parts.part1 import Part1
from parts.part2 import Part2





class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.v = pg.image.load(os.path.join("images", "background0.png")).convert()
        self.BG = pg.transform.scale(self.v, (WIN_WIDTH, WIN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

        self.check_point_hit = 0
        self.not_passed = True  # Initialize not_passed at class level
        self.load_data()

        self.parts = [Part1(self), Part2(self)]
    def new(self):
        
        self.all_sprites = pg.sprite.LayeredUpdates()

        self.ground_platforms = pg.sprite.Group()
        self.jump_platforms = pg.sprite.Group()
        self.background_sprites = pg.sprite.Group()

        self.powerups = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.grounds = pg.sprite.Group()
        self.check_points = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)

        for part in self.parts:
            part.new()
        
        pg.mixer.music.load(path.join(self.snd_dir, "part1.ogg"))
        self.run()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "images")
        self.spritesheet_char = Spritesheet(path.join(img_dir, SPRITESHEET_CHAR))
        self.spritesheet_platform = Spritesheet(path.join(img_dir, SPRITESHEET_PLATFORM))
        self.spritesheet_items = Spritesheet(path.join(img_dir, SPRITESHEET_ITEMS))
        self.spritesheet_enemies = Spritesheet(path.join(img_dir, SPRITESHEET_ENEMIES))
        self.snd_dir = path.join(self.dir, "sounds")
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, "Jump33.wav"))
        self.gems_sound = pg.mixer.Sound(path.join(self.snd_dir, "boost.wav"))

    def run(self):
        #pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)
            
    def update(self):
        self.player.not_hit_portal = True
        self.scroll_items = list(self.ground_platforms) \
            + list(self.jump_platforms) + list(self.background_sprites) \
            + list(self.portals) + list(self.check_points) + list(self.enemies)\
            + list(self.powerups)
        
        
        if self.player.rect.y + self.player.vel.y + self.player.rect.height > WIN_HEIGHT:
            self.show_over_screen()
        for part in self.parts:
            part.update()
        self.all_sprites.update()
        self.scroll_page()        
    def scroll_page(self):
        if self.player.rect.right >= WIN_WIDTH-300:
            self.player.pos.x -= abs(self.player.vel.x)
            for p in self.scroll_items:
                p.rect.x -= abs(self.player.vel.x)
        if self.player.rect.left <= 100 and self.player.rect.x + self.player.vel.x > 0:
            self.player.pos.x += (abs(self.player.vel.x))
            for p in self.scroll_items:
                p.rect.x += abs(self.player.vel.x)
    def move_screen(self, screen_width):
        self.check_point_hit = pg.time.get_ticks()
        
        if self.screen.get_width() - self.player.pos.x < screen_width:
            #self.info_screen()
            self.player.vel.x = 0
            self.player.pos.x -= SCREEN_SCROLL_SPEED
            for p in self.scroll_items:
                p.rect.x -= SCREEN_SCROLL_SPEED
                #self.info_screen()
        else:
             for el in self.check_points:
                el.rect.x = - self.player.pos.x - 150
             self.info_screen()
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False 
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                    #self.jump_sound.play()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
            

            

    def draw(self):
        self.screen.blit(self.BG, (0,0))
        self.player.draw_healthbar()
        self.all_sprites.draw(self.screen)
        self.draw_text(f"Level {0}/{5}", 35, "white", 50, 50)

        pg.display.update()
    def info_screen(self):
        self.screen.fill("light blue")
        self.draw_text(
            "Mål: Kom deg til andre side uten å bli truffet eller treffe vannet",
            40,
            "white",
            200,
            350
        )
        #pg.display.flip()
        #pg.mixer.music.fadeout(500)
        self.wait_for_key()
        #pg.mixer.music.load(path.join(self.snd_dir, "part4.ogg"))
        #pg.mixer.music.play(loops=-1)
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
        self.screen.fill("black")
        pg.display.flip()
        pg.time.delay(500)
        sys.exit()
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

        
