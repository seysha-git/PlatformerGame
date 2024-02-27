import pygame as pg, sys
from settings import *

class Button:
    def __init__(self, screen, text, width, height, pos):
        self.pressed = False
        self.top_rect = pg.Rect(pos, (width, height))
        self.top_color = "#475F77"
        self.screen = screen

        self.text_surf = MENU_FONT.render(text, True, "white")
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
    def draw(self):
        pg.draw.rect(self.screen, self.top_color, self.top_rect, border_radius= 12)
        self.screen.blit(self.text_surf, self.text_rect)
        
    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            
            self.top_color = "red"
            if pg.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    print("click")
                    self.pressed = False
        else:
            self.top_color = "#475F77"



class LevelGuide():
    def __init__(self, game, x, y, text):
        self.groups =  game.all_sprites, game.guides,
        self.game = game
        self.scrolling_text_font = pg.font.Font("freesansbold.ttf", 28)
        self.snip = self.scrolling_text_font.render(text, True, 'white')
        
        self.levels_messages = [ 
            "Test 1",
            "Test 2",
            "Test 3"

        ]
        self.rect = pg.Rect(x,y,400,170)

        self.active_message = 0
        self.message = self.levels_messages[self.active_message]
        self.counter = 9
        self.speed = 3
        self.done = False

    def update_text(self):
        if self.active_message < len(self.levels_messages):
            if self.counter < self.speed * len(self.message):
                self.counter += 1
            elif self.counter >= self.speed* len(self.message):
                self.done = True
        self.snip = self.scrolling_text_font.render(self.message[0:self.counter//self.speed], True, "white")
        
    def draw(self):
        #self.update_text()
        pg.draw.rect(self.game.screen, "#475F77", self.rect, border_radius= 12)
        self.game.screen.blit(self.snip, (self.rect.x + 60, self.rect.y + 70))
    def create_new(self):
        self.active_message += 1
        self.done = False
        self.message = self.messages[self.active_message]
        self.counter = 0
