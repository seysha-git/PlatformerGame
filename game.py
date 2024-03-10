import pygame as pg
import sys
from settings import *
from modules.characters import *
from modules.guide_items import *
from modules.weapons import PlayerBullet
from os import path
from game_ground import GameGround
pg.font.init()





class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.v = pg.image.load(os.path.join("images", "background0.png")).convert()
        self.BG = pg.transform.scale(self.v, (WIN_WIDTH, WIN_HEIGHT))
        self.font_name = pg.font.match_font(FONT_NAME)

        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()
        self.top_scroll = 200
        self.scroll_distance = 0

        self.check_point_active = False

        self.game_ground = GameGround(self)
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
        
        self.switches = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.princesses = pg.sprite.Group()
        
        self.grounds = pg.sprite.Group()
        self.check_points = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.princess = Princess(self)


        self.game_ground.new()
        pg.mixer.music.load(path.join(self.snd_dir, "part1.ogg"))
        self.run()

    def load_data(self):
        self.dir = path.dirname(__file__)
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
        self.scroll_items = [item for item in self.all_sprites if not isinstance(item, Player)]
        self.scroll_page() 
        self.game_ground.update()
        self.all_sprites.update()
               
    def scroll_page(self):
        if self.player.rect.y <= self.top_scroll:
            self.player.pos.y += abs(self.player.acc.y + 2)
            for p in self.scroll_items:
                p.rect.y += abs(self.player.acc.y + 2)
        if self.player.rect.top >= WIN_HEIGHT-100:
            self.player.pos.y -= abs(self.player.acc.y + 2)
            for p in self.scroll_items:
                p.rect.y -= abs(self.player.acc.y + 2)
    def move_screen(self):
            print("move screen")
            self.player.vel.x = SCREEN_SCROLL_SPEED
            self.player.pos.x -= SCREEN_SCROLL_SPEED
            self.scroll_distance -= SCREEN_SCROLL_SPEED
            for p in self.scroll_items:
                p.rect.x -= SCREEN_SCROLL_SPEED
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False 
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_w or event.key == pg.K_SPACE) and not self.player.on_stairs:
                    self.player.jump()
            if event.type == pg.MOUSEBUTTONDOWN:
                x,y = pg.mouse.get_pos()     
                PlayerBullet(self, self.player.rect.centerx, self.player.rect.centery, 6, x,y)
    def draw(self):
        self.screen.fill((50, 168, 82))
        self.game_ground.draw()
        self.all_sprites.draw(self.screen)
        self.navbar()
        self.player.draw_healthbar()
        pg.display.update()
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
    def get_logo(self, type):
        images = {
            "main": self.spritesheet_huds.get_image(55,49,47,47),
            "princess": self.spritesheet_huds.get_image(49,190,47,47)
        }
        image = images[type]
        image.set_colorkey("black")
        return image
    def navbar(self):
        max_health = 100
        health = 100
        navbar_rect = pg.Rect(0,0, WIN_WIDTH, 70)
        pg.draw.rect(self.screen, (77, 219, 115), navbar_rect)
        self.screen.blit(self.get_logo("main"), (30,20))
        self.screen.blit(self.get_logo("princess"), (WIN_WIDTH//2-10, 10))
        #pg.draw.rect(self.screen, (255, 0,0), (WIN_WIDTH//2-45, 65, 120, 10 ))
        #pg.draw.rect(self.screen, (00, 255,0), (WIN_WIDTH//2-45, 65, 120 * (1-((max_health - health))/max_health), 10 ))
        pg.draw.rect(self.screen, "light blue", (WIN_WIDTH-250, 10, 200, 50), 0, 5)
        self.draw_text("Tid: 00:00", 30, "white", WIN_WIDTH-210, 18)

        #self.draw_text(f"Level {0}/{5}", 35, "white", 50, 30)



        
