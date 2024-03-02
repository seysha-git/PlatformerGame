import pygame as pg
from settings import *
from modules.guide_items import *
import sys


class Start:
    def __init__(self, game, screen, gameStateManager):
        self.game = game
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.font_name = pg.font.match_font(FONT_NAME)
    def new(self):
        self.play_button = Button(self.screen, "Spill nå", 200, 50, (200,400))
        self.settings_button = Button(self.screen, "Instillinger", 200, 50, (200,500))
        self.quit_button = Button(self.screen, "Avslutt", 200, 50, (200,600))
    def draw(self):
        self.new()
        self.screen.fill("light green")
        self.draw_text("Mitt Platform spill", 100, "white",200,180)
        self.draw_text(GAME_DESCRIPTION_1, 30, "white", 600,400)
        self.draw_text(GAME_DESCRIPTION_2, 30, "white", 600,450)
        self.draw_text(GAME_DESCRIPTION_3, 30, "white", 600,500)
        self.draw_text(GAME_DESCRIPTION_4, 30, "white", 600,550)
        self.draw_text(GAME_DESCRIPTION_4, 30, "white", 600,600)

        self.play_button.draw()
        self.settings_button.draw()
        self.quit_button.draw()
        pg.display.update()
        
    def run(self):
        self.draw()
        self.events()
        
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.screen.blit(text_surface, text_rect)
    def events(self):
        self.play_button.check_click()
        if self.play_button.pressed:
            self.gameStateManager.set_state("level1")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
    