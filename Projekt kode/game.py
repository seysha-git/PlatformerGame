import pygame as pg
import sys
from settings import *
from modules.characters import *
from modules.guide_items import *
from os import path
from game_ground import GameGround
pg.font.init()
from utils import *



class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.font_name = pg.font.match_font(FONT_NAME)
        self.quiz_font = pg.font.Font("freesansbold.ttf", 20)
        self.clock = pg.time.Clock()
        self.running = True
        self.completed = True
        self.player_dead = False
        self.quiz_rect = pg.Rect(WIN_WIDTH//2-250, 80,500,300)
        self.load_game_data()
        self.game_ground = GameGround(self)
        self.time = 0
    def level_guide(self):
        self.scrolling_text_font = pg.font.Font("freesansbold.ttf", 20)
        self.levels_messages = [ 
            "This is my intro message",
            "This is CP nr 2",
            "This is CP nr 3"
        ]
        self.guide_rect = pg.Rect(WIN_WIDTH//2-200, 80,400,170)
        self.active_message = 0
        self.message = self.levels_messages[self.active_message]
        self.snip_guide = self.scrolling_text_font.render(self.message, True, 'white')
        self.counter = 9
        self.speed = 4
        self.all_message_completed = False
        self.done = False

    def animated_message(self):
        if self.active_message < len(self.levels_messages):
            if self.counter < self.speed * len(self.message):
                self.counter += 1
            elif self.counter >= self.speed* len(self.message):
                self.done = True
        self.snip_guide = self.scrolling_text_font.render(self.message[0:self.counter//self.speed], True, "white")
    def draw_guide_message(self):
        if not self.all_message_completed:
            pg.draw.rect(self.screen, "#475F77", self.guide_rect, border_radius= 12)
            self.screen.blit(self.snip_guide, (self.guide_rect.x + 10, self.guide_rect.y + 40))
    def create_new_message(self):
        if self.active_message < len(self.levels_messages) -1:
            self.active_message += 1
            self.done = False
            self.all_message_completed = False
            self.message = self.levels_messages[self.active_message]
            self.counter = 0
        else:
            return
    def new(self):
        
        self.all_sprites = pg.sprite.LayeredUpdates()

        self.ground_platforms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.roofs = pg.sprite.Group()
        self.jump_platforms = pg.sprite.Group()
        self.background_sprites = pg.sprite.Group()
        self.player_bullets = pg.sprite.Group()
        self.course_bullets = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.logos =pg.sprite.Group()
        
        self.keys = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.princesses = pg.sprite.Group()
        
        self.grounds = pg.sprite.Group()
        self.check_points = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

        self.game_ground.new()

        self.delayed_time = self.time

        pg.mixer.music.load(path.join(self.snd_dir, "part1.ogg"))
        self.run()
    def load_game_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, TS_FILE),'w') as f:
            try:
                self.top_time_score = int(f.read())
            except:
                self.top_time_score = 0

        img_dir = path.join(self.dir, "images")
        self.spritesheet_char = Spritesheet(path.join(img_dir, SPRITESHEET_CHAR))
        self.spritesheet_platform = Spritesheet(path.join(img_dir, SPRITESHEET_PLATFORM))
        self.spritesheet_items = Spritesheet(path.join(img_dir, SPRITESHEET_ITEMS))
        self.spritesheet_enemies = Spritesheet(path.join(img_dir, SPRITESHEET_ENEMIES))
        self.spritesheet_huds = Spritesheet(path.join(img_dir, SPRITESHEET_HUD))
        self.spritesheet_princess = Spritesheet(path.join(img_dir, SPRITESHEET_PRINCESS))
        self.snd_dir = path.join(self.dir, "sounds")
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, "Jump33.wav"))
        self.gems_sound = pg.mixer.Sound(path.join(self.snd_dir, "boost.wav"))
        self.level_guide()
    def run(self):
        #pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.animated_message()
            self.clock.tick(FPS)
            self.game_ground.events()
            self.update()
            self.draw()
            
        pg.mixer.music.fadeout(500)
    def update(self):
        self.game_ground.update()
        self.all_sprites.update()
        self.delayed_time = (pg.time.get_ticks() - self.time) // 1000
    def draw(self):
        self.screen.fill((50, 168, 82))
        self.all_sprites.draw(self.screen)
        self.navbar()
        self.game_ground.player.draw()
        self.draw_guide_message()
        pg.display.update()
    def show_start_screen(self):
        self.screen.fill("light green")
        self.draw_text("Mitt Platform spill", 100, "white",400,200)
        self.draw_text("Kontrollene", 50, "white", 590, 320)
        self.w = Button(self.screen, "w", 120, 70, (630,400))
        self.a = Button(self.screen, "a", 120, 70, (630,500))
        self.s = Button(self.screen, "s", 120, 70, (480,500))
        self.d = Button(self.screen, "d", 120, 70, (780,500))

        self.play_button = Button(self.screen, "Spill nå", 200, 60, (590,630), "green")
        self.play_button.draw()
        self.w.draw()
        self.a.draw()
        self.s.draw()
        self.d.draw()

        

        

        pg.display.flip()
        self.wait_for_key()
    def show_go_screen(self): 
        if self.playing:
           return
        self.title = ""
        self.play_button = Button(self.screen, "Spill igjen", 200, 50, (520,800))
        self.quit_button = Button(self.screen, "Avslutt", 200, 50, (780,800))

        self.screen.fill("dark grey")

        pg.draw.rect(self.screen, "light blue", (460, 290, 620, 400), 0, 5)
        self.play_button.draw()
        self.quit_button.draw()
        if self.completed:
            self.title = "Bra Jobba!"
            if self.delayed_time > self.top_time_score:
                self.top_time_score = self.delayed_time
                with open(path.join(self.dir, TS_FILE), "w") as f:
                    f.write(str(self.top_time_score))
            self.draw_text("Statistikk", 50, "white", 460+220, 320)
            self.draw_text(f"Beste tid: {self.top_time_score}          Din tid: {self.delayed_time}", 30, "white", 460 + 100, 400)
            self.draw_text(f"Best aim: 5/20            Ditt aim : 20/30", 30, "white", 460 + 100, 460)
            self.draw_text(f"Mest liv: 80/100          Ditt liv: 60/100", 30, "white", 460 + 100, 520)
            self.draw_text(f"Godt forsøk, prøv igjen :)", 30, "white", 460 + 150, 620)
        if self.player_dead:
            self.title = "Du døde"
            if self.delayed_time > self.top_time_score:
                self.top_time_score = self.delayed_time
                with open(path.join(self.dir, TS_FILE), "w") as f:
                    f.write(str(self.top_time_score))
            self.draw_text("Statistikk", 50, "white", 460+220, 320)
            self.draw_text(f"Beste tid: {self.top_time_score}          Din tid: {self.delayed_time}", 30, "white", 460 + 100, 400)
            self.draw_text(f"Best aim: 5/20            Ditt aim : 20/30", 30, "white", 460 + 100, 460)
            self.draw_text(f"Mest liv: 80/100          Ditt liv: 60/100", 30, "white", 460 + 100, 520)
            self.draw_text(f"Godt forsøk, prøv igjen :)", 30, "white", 460 + 150, 620)
        self.draw_text(f"{self.title}", 120, "white",570,80)
        pg.draw.rect(self.screen, "black", (0, 220, WIN_WIDTH, 20))
        pg.draw.rect(self.screen, "black", (0, WIN_HEIGHT-180, WIN_WIDTH, 20))
        pg.display.flip()
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
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.screen.blit(text_surface, text_rect)
    def get_logo(self, type):
        images = {
            "main": self.spritesheet_huds.get_image(55,49,47,47),
            "princess": self.spritesheet_huds.get_image(49,190,47,47),
            "keys": self.spritesheet_huds.get_image(146,147,44,40)
        }
        image = images[type]
        image.set_colorkey("black")
        return image
    def navbar(self):
        navbar_rect = pg.Rect(0,0, WIN_WIDTH, 60)
        pg.draw.rect(self.screen, (77, 219, 115), navbar_rect)
        self.screen.blit(self.get_logo("main"), (30,10))
        self.screen.blit(self.get_logo("princess"), (WIN_WIDTH//2-10, 10))
        for i in range(self.game_ground.player.keys):
            self.screen.blit(self.get_logo("keys"), (100+ 70*i, 10))
        pg.draw.rect(self.screen, "light blue", (WIN_WIDTH-240, 10, 150, 40), 0, 5)
        self.draw_text(f"Tid: {self.delayed_time}:00", 30, "white", WIN_WIDTH-220, 12)



        
