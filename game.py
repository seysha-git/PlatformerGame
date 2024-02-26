import pygame as pg
import sys
from settings import *
from modules.characters import *
from os import path
from parts.part1 import Part1
from parts.part2 import Part2
from modules.menu import Button
pg.font.init()





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
        self.scrolling_text_font = pg.font.Font("freesansbold.ttf", 24)
        self.snip = self.scrolling_text_font.render('', True, 'white')
        self.messages = [
            "Test 1",
            "test 2", 
            "test 3"
        ]
        self.active_message = 0
        self.message =self.messages[self.active_message]
        self.counter = 0
        self.speed = 3
        self.done = False


        self.check_point_hit = 0
        self.not_passed = True  # Initialize not_passed at class level
        self.load_data()

        self.check_point_active = False
        self.x = False

        self.parts = [Part1(self), Part2(self)]
    def new(self):
        
        self.all_sprites = pg.sprite.LayeredUpdates()

        self.ground_platforms = pg.sprite.Group()
        self.jump_platforms = pg.sprite.Group()
        self.background_sprites = pg.sprite.Group()

        self.powerups = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
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
            + list(self.powerups) + list(self.spikes)
        
        
        if self.player.rect.y + self.player.vel.y + self.player.rect.height > WIN_HEIGHT:
            self.show_over_screen()
        self.scroll_page() 
        for part in self.parts:
            part.update()
        self.all_sprites.update()
               
    def scroll_page(self):
        if self.player.rect.right >= WIN_WIDTH-200:
            self.player.pos.x -= abs(self.player.vel.x)
            for p in self.scroll_items:
                p.rect.x -= abs(self.player.vel.x)
        if self.player.rect.left <= 100 and self.player.rect.x + self.player.vel.x + self.player.rect.width + 50 > 0:
            self.player.pos.x += (abs(self.player.vel.x))
            for p in self.scroll_items:
                p.rect.x += abs(self.player.vel.x)
    def move_screen(self):
            print("move screen")
            self.player.vel.x = SCREEN_SCROLL_SPEED
            self.player.pos.x -= SCREEN_SCROLL_SPEED
            for p in self.scroll_items:
                p.rect.x -= SCREEN_SCROLL_SPEED
    def create_animated_text(self):
        if self.active_message <2:
            if self.counter < self.speed * len(self.message):
                self.counter += 1
            elif self.counter >= self.speed* len(self.message):
                self.done = True
    def draw_animated_text(self):
        if self.active_message < 2:
            pg.draw.ellipse(self.screen, "light green", (190,190,300,100))
            self.screen.blit(self.snip, (320,220))
    def events(self):
        #self.create_animated_text()
        #self.draw_scrolling_text("Prøv å spill min platformer")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False 
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                print(self.done, self.active_message)
                if event.key == pg.K_RETURN and self.done and self.active_message < len(self.messages)-1:
                    print("create new")
                    self.active_message += 1
                    self.done = False
                    self.message = self.messages[self.active_message]
                    self.counter = 0
                

        self.snip = self.scrolling_text_font.render(self.message[0:self.counter//self.speed], True, "black")
            
    def draw(self):
        self.screen.blit(self.BG, (0,0))
        self.player.draw_healthbar()
        self.all_sprites.draw(self.screen)
        self.draw_text(f"Level {0}/{5}", 35, "white", 50, 50)

        pg.display.update()
    def info_screen(self):
        message = "Mål: Kom deg til andre side uten å bli truffet eller treffe vannet"
        self.screen.fill("light blue")
        self.draw_text(
            message,
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
        self.screen.fill("light green")
        self.draw_text("Mitt Platform spill", 100, "white",200,180)
        self.play_button = Button(self.screen, "Spill nå", 200, 50, (200,400))
        self.settings_button = Button(self.screen, "Instillinger", 200, 50, (200,500))
        self.quit_button = Button(self.screen, "Avslutt", 200, 50, (200,600))
        self.draw_text(GAME_DESCRIPTION_1, 30, "white", 600,400)
        self.draw_text(GAME_DESCRIPTION_2, 30, "white", 600,450)
        self.draw_text(GAME_DESCRIPTION_3, 30, "white", 600,500)
        self.draw_text(GAME_DESCRIPTION_4, 30, "white", 600,550)
        self.draw_text(GAME_DESCRIPTION_4, 30, "white", 600,600)

        self.play_button.draw()
        self.settings_button.draw()
        self.quit_button.draw()

        pg.display.flip()
        self.wait_for_key()
    def show_over_screen(self):
        self.show_start_screen()
        self.new()
        self.wait_for_key()
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            self.play_button.check_click()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False 
                    self.running = False 
                    sys.exit()
            if self.play_button.pressed:
                waiting = False
    def show_go_screen(self):
        ...
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.screen.blit(text_surface, text_rect)

        
