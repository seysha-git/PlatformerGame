import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *
from levels.level import Level

class Level2(Level):
    def __init__(self, game):
        super().__init__(game)
        self.hit = False
        self.vel = 1
        self.jump_platform_cordinates = [
            ()
        ]
    def background(self):
        ...
    def new(self):
        super().new()
        self.enemies_timer = 0 
        self.platform_timer = 0
        self.background()
    def move_plat(self):
        for plat in self.game.jump_platforms:
            if isinstance(plat,MovingJumpPlatform):
                plat.horizontal_movement()
                if self.game.player.on_moving_plat:
                    player = self.game.player 
                    player.rect.x += plat.direction
    def move_portal_down(self):
        for portal in self.game.portals:
            if pg.sprite.spritecollide(portal, self.game.ground_platforms, False):
                self.portal_closed = True
            portal.rect.y += 0.35
    def create_enemies(self):
        now = pg.time.get_ticks()
        if (now - self.enemies_timer) // 1000 > 3:
            self.enemies_timer = now 
            EnemyFly(self.game, rd.randint(900,1000), rd.randint(WIN_HEIGHT, WIN_HEIGHT + 200))         
    def update(self):
        super().update()
        #self.move_portal_down()
        self.move_plat()

