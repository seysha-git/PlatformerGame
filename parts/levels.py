import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *




class Level:
    def __init__(self, game):
        self.scroll_timer = 0
        self.scroll_duration = 1300
        self.game = game
        self.ground_length = 23
    def check_wall_collision_x(self):
        wall_hits = pg.sprite.spritecollide(self.game.player, self.game.walls, False)
        for tile in wall_hits:
            if self.game.player.vel.x > 0:
                self.game.player.pos.x = tile.rect.left - self.game.player.rect.w+30
                self.game.player.rect.x = self.game.player.pos.x
            elif self.game.player.vel.x < 0:
                self.game.player.pos.x = tile.rect.right + self.game.player.rect.w-30
                self.game.player.rect.x = self.game.player.pos.x
    def check_wall_collision_y(self):
        wall_hits = pg.sprite.spritecollide(self.game.player, self.game.walls, False)
        #self.game.player.rect.bottom += 1
        for tile in wall_hits:
            if self.game.player.vel.y < 0:
                self.game.player.vel.y = 0
                print("move down")
                self.game.player.pos.y = tile.rect.bottom + self.game.player.rect.height
                self.game.player.rect.bottom = self.game.player.pos.y
                #print("hit")
    def update(self):
        self.check_wall_collision_x()
        self.check_wall_collision_y()
        """
        if self.game.check_point_active:
            current_time = pg.time.get_ticks()
            # if current_time - self.scroll_timer < self.scroll_duration:
            if self.game.scroll_distance > 0:
                print("active")
                self.game.move_screen()
            else:
                # Deactivate the check point after the timer expires
                self.game.check_point_active = False
                self.check_point_active_1 = True
        """
        
    def new(self):
        self.scroll_time = 0
        
        self.enemies_timer = 0 
        self.platform_timer = 0

        for i in range(1,15):
            WallPlatform(self.game,WIN_WIDTH-70, 70*i-180)
        for i in range(1,15):
            WallPlatform(self.game,0, 70*i-180)
        for i in range(1,self.ground_length):
           GroundPlatform(self.game, i*70- 70, WIN_HEIGHT-30)
        for i in range(1,self.ground_length):
           WallPlatform(self.game, i*70- 70, 40)
    def boost_platform(self):
        hits = pg.sprite.spritecollide(self.game.player, self.game.boosters, False)
        if hits:
            self.game.player.vel.y = -MAIN_JUMP_VEL*2
            hits[0].animate()
    def handle_checkpoint_collisions(self):
        hit = pg.sprite.spritecollide(self.game.player, self.game.check_points, True)
        if hit:
            print("hit")
            self.game.check_point_active = True
            self.game.scroll_distance = 400
            # Activate the scroll timer
            self.scroll_timer = pg.time.get_ticks()


