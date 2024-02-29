
import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *
from levels.level import Level


class Level1(Level):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.hit = False
        self.vel = 1
        self.ground_length = 7
        self.jump_platform_cordinates = [
            ()
        ]
    def background(self):
        super().background()
        BackgroundPlatform(self.game, 100, WIN_HEIGHT-130, "sign_left")
    def new(self):
        self.background() 
        for i in range(1,6):
          GroundPlatform(self.game, WIN_WIDTH//2-300 + 70*i, WIN_HEIGHT-200)
        for i in range(1,6):
          GroundPlatform(self.game, WIN_WIDTH-490+ 70*i, WIN_HEIGHT-700)
       
    def move_plat(self):
        for plat in self.game.jump_platforms:
            if isinstance(plat,MovingJumpPlatform):
                plat.horizontal_movement()
                if self.game.player.on_moving_plat:
                    player = self.game.player 
                    player.rect.x += plat.direction
    def create_enemies(self):
        now = pg.time.get_ticks()
        if (now - self.enemies_timer) // 1000 > 3:
            self.enemies_timer = now 
            EnemyFly(self.game, rd.randint(900,1000), rd.randint(WIN_HEIGHT, WIN_HEIGHT + 200))         
    def update(self):
        super().update()
        self.move_plat()