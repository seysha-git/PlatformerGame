import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *
from modules.weapons import CourseBullet


class GameGround:
    def __init__(self, game):
        self.spikes_time = 0
        self.game = game
        self.ground_length = 23
        self.water_length = 14
        self.spawn_course_bullets = False
        self.check_point_active_2 = False
    def update(self):
        self.check_wall_collision_x()
        self.check_wall_collision_y()
        self.player_ladder_colission()
        #self.player_spike_colission()
        self.create_bullets()
        #self.create_enemies()
    def new(self):
        self.side_field_backgrounds()
        self.start_runner_room()
        self.jump_gun_room()
        self.question_room()
        self.shoot_room()
    def draw(self):
        pass
        #self.draw_course_gun()
        #CourseBullet(self.game, WIN_WIDTH-100, 80, rd.randint(1,4))
    def player_spike_colission(self):
        hits = pg.sprite.spritecollide(self.game.player, self.game.spikes, False)
        if hits:
            if hits[0].type == 0:
                hits[0].kill()
                self.game.player.health -= 20

    def player_ladder_colission(self):
        hits = pg.sprite.spritecollide(self.game.player, self.game.background_sprites, False)
        if not hits:
            self.game.player.on_stairs = False
        else:
            for hit in hits:
                if hit.type == "stairs":
                    keys = pg.key.get_pressed()
                    self.game.player.on_stairs = True
                    if keys[pg.K_w]:
                        self.game.player.vel.y -= 0.5
        

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
        wall_hits = pg.sprite.spritecollide(self.game.player, self.game.roofs, False)
        #self.game.player.rect.bottom += 1
        for tile in wall_hits:
            if self.game.player.vel.y > 0:
                self.game.player.vel.y = 0
            if self.game.player.vel.y < 0:
                self.game.player.vel.y = 0
                self.game.player.pos.y = tile.rect.bottom + self.game.player.rect.height
                self.game.player.rect.bottom = self.game.player.pos.y
                #print("hit")   
    def side_field_backgrounds(self):
        for i in range(1,15):
            WallPlatform(self.game,WIN_WIDTH-60, 70*i-180)
        for i in range(1,15):
            WallPlatform(self.game,0, 70*i-180)
        for i in range(1,self.ground_length):
           GroundPlatform(self.game, i*70- 70, WIN_HEIGHT-30)
        for i in range(1,self.ground_length):
           RoofPlatform(self.game, i*70- 70, 20)
    def handle_checkpoint_collisions(self):
        hit = pg.sprite.spritecollide(self.game.player, self.game.check_points, True)
        if hit:
            print("hit")
            self.game.check_point_active = True
            self.game.scroll_distance = 400
            # Activate the scroll timer
            self.scroll_timer = pg.time.get_ticks()
    def question_room(self):
        for i in range(1,7):
            GroundPlatform(self.game, 70*i, WIN_HEIGHT-360)
        for i in range(1,8):
           WallPlatform(self.game, 495, 70*i-20)
        for i in range(1,6):
           GroundPlatform(self.game, 70*i, 240, "half_ground")
        BackgroundItem(self.game, 300, 170, "tresure")
        BackgroundItem(self.game, 75, 170, "door_mid")
        BackgroundItem(self.game, 75, 170-70, "door_top")
        BackgroundItem(self.game, 340, WIN_HEIGHT//2+19, "flag_green")
    def jump_gun_room(self):
        for i in range(1,6): #dør gulvet
            WallPlatform(self.game,WIN_WIDTH-380, 70*i+180)
        for i in range(1,3):
            GroundPlatform(self.game, WIN_WIDTH-520 + 70*i, 210, "half_ground")
        JumpPlatform(self.game, WIN_WIDTH-130, WIN_HEIGHT-190, 0)
        MovingJumpPlatform(self.game, WIN_WIDTH-130, WIN_HEIGHT-480.5, 0, -1)
        MovingJumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-320, 0, 1)
        MovingJumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-620, 0, -1)
        #MovingJumpPlatform(self.game, WIN_WIDTH-130, WIN_HEIGHT-650, 0, 1)
       # MovingJumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-630, 0, 1)

    def start_runner_room(self):
        for i in range(1,11): # Nest nederste taket
            RoofPlatform(self.game, i*70+420, WIN_HEIGHT-360) #roof
        for i in range(1,5):
            BackgroundItem(self.game, 499, WIN_HEIGHT-50 - 40*i, "stairs")
        for i in range(1,8):
            GroundPlatform(self.game, 500 + 70*i, WIN_HEIGHT-200, "half_ground")
        for i in range(1,5):
            BackgroundItem(self.game, 1060, WIN_HEIGHT-50 - 40*i, "stairs")
        for i in range(1,3):
            for j in range(1,8):
                WallPlatform(self.game, 500 + 70*j,WIN_HEIGHT-230+70*i)
        #Spike(self.game, 670, WIN_HEIGHT-270, 0,self.spikes_time )
        #Spike(self.game, 770, WIN_HEIGHT-270, 0, self.spikes_time)
        #Spike(self.game, 920, WIN_HEIGHT-270, 0, self.spikes_time)
        self.star = BackgroundItem(self.game, 1150, WIN_HEIGHT-100, "star")
    def shoot_room(self):
        for i in range(1,9):
            GroundPlatform(self.game, 490 + 70*i, 515, "lava")
        JumpPlatform(self.game, WIN_WIDTH//2, WIN_HEIGHT-500, 0)
        JumpPlatform(self.game, WIN_WIDTH//2+120, WIN_HEIGHT-600, 0)
        JumpPlatform(self.game, WIN_WIDTH//2-120, WIN_HEIGHT-650, 0)
    def create_enemies(self):
        while len(list(self.game.enemies)) < 2:
            EnemyFly(self.game,  WIN_WIDTH-450,rd.randint(WIN_HEIGHT-600, WIN_HEIGHT-500))
    
            #GroundPlatform(self.game, 350, 535, "wood_box")
            #GroundPlatform(self.game, 350, 530-70, "wood_box")
    def create_bullets(self):
        if pg.sprite.collide_mask(self.game.player, self.star):
            self.spawn_course_bullets = True
        if self.spawn_course_bullets:
            while len(list(self.game.course_bullets)) < 2:
                print("bullet")
                CourseBullet(self.game)
    def draw_course_gun(self):
        pg.draw.rect(self.game.screen, "blue", (WIN_WIDTH-210,100,60,80))
        #pg.draw.rect(self.game.screen, "blue", (WIN_WIDTH-180,80,30,30))
        #pg.draw.rect(self.game.screen, "blue", (WIN_WIDTH-220,80,30,30))
        

