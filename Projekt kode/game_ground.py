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
        self.spawn_course_bullets = False
        self.check_point_active_2 = False
    def update(self):
        self.check_wall_collision_x()
        self.check_wall_collision_y()
        self.player_ladder_colission()
        self.player_spike_colission()
        self.handle_checkpoint_collisions()
        self.create_bullets()
        #self.create_enemies()
    def new(self):
        self.side_field_backgrounds()
        self.start_runner_room()
        self.jump_gun_room()
        self.question_room()
        self.shoot_room()
        self.draw_course_gun()
        self.player = Player(self.game)
        self.princess = Princess(self.game)
    def player_spike_colission(self):
        hits = pg.sprite.spritecollide(self.player, self.game.spikes, False)
        if hits:
            if hits[0].type == 0:
                hits[0].kill()
                self.player.health -= 20
    def player_ladder_colission(self):
        hits = pg.sprite.spritecollide(self.player, self.game.background_sprites, False)
        if not hits:
            self.player.on_stairs = False
        else:
            for hit in hits:
                if hit.type == "stairs":
                    keys = pg.key.get_pressed()
                    self.player.on_stairs = True
                    if keys[pg.K_w]:
                        self.player.vel.y -= 0.5
        

    def check_wall_collision_x(self):
        wall_hits = pg.sprite.spritecollide(self.player, self.game.walls, False)
        for tile in wall_hits:
            if self.player.vel.x > 0:
                self.player.pos.x = tile.rect.left - self.player.rect.w+30
                self.player.rect.x = self.player.pos.x
            elif self.player.vel.x < 0:
                self.player.pos.x = tile.rect.right + self.player.rect.w-30
                self.player.rect.x = self.player.pos.x
    def check_wall_collision_y(self):
        wall_hits = pg.sprite.spritecollide(self.player, self.game.roofs, False)
        #self.game.player.rect.bottom += 1
        for tile in wall_hits:
            if self.player.vel.y > 0:
                self.player.vel.y = 0
            if self.player.vel.y < 0:
                self.player.vel.y = 0
                self.player.pos.y = tile.rect.bottom + self.player.rect.height
                self.player.rect.bottom = self.player.pos.y
                #print("hit")   
    def side_field_backgrounds(self):
        for i in range(1,15):
            WallPlatform(self.game,WIN_WIDTH-60, 70*i-180)
        for i in range(1,15):
            WallPlatform(self.game,0, 70*i-180)
        for i in range(1,self.ground_length):
           GroundPlatform(self.game, i*70- 70, WIN_HEIGHT-30)
        for i in range(1,self.ground_length):
           RoofPlatform(self.game, i*70- 70, -30)
    def handle_checkpoint_collisions(self):
        hits = pg.sprite.spritecollide(self.player, self.game.check_points, True)
        if hits:
            if hits[0].type == "1":
                self.spawn_course_bullets = True
                print("hit")
            self.game.create_new_message()
    def question_room(self):
        for i in range(1,7):
            GroundPlatform(self.game, 70*i, WIN_HEIGHT-360)
        for i in range(1,5):
           WallPlatform(self.game, 495, 70*i-20)
        for i in range(1,6):
           GroundPlatform(self.game, 70*i, 240, "half_ground")
        BackgroundItem(self.game, 300, 170, "tresure")
        BackgroundItem(self.game, 75, 170, "door_mid")
        BackgroundItem(self.game, 75, 170-70, "door_top")
        Checkpoint(self.game, 340, WIN_HEIGHT//2+19, "3")
    def jump_gun_room(self):
        for i in range(1,6): #dør gulvet
            WallPlatform(self.game,WIN_WIDTH-380, 70*i+180)
        for i in range(1,3):
            GroundPlatform(self.game, WIN_WIDTH-520 + 70*i, 210, "half_ground")
        JumpPlatform(self.game, WIN_WIDTH-130, WIN_HEIGHT-190, 0)
        JumpPlatform(self.game, WIN_WIDTH-240, WIN_HEIGHT-478, 0)
        MovingJumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-320, 0, 1)
        MovingJumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-620, 0, -1)
        Checkpoint(self.game, WIN_WIDTH-390, 130, "2")
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
        Spike(self.game, 670, WIN_HEIGHT-270, 0,self.spikes_time )
        Spike(self.game, 770, WIN_HEIGHT-270, 0, self.spikes_time)
        Spike(self.game, 920, WIN_HEIGHT-270, 0, self.spikes_time)
        Checkpoint(self.game, 1150, WIN_HEIGHT-100, "1")
    def shoot_room(self):
        for i in range(1,9):
            GroundPlatform(self.game, 490 + 70*i, 515, "lava")
        JumpPlatform(self.game, WIN_WIDTH//2, WIN_HEIGHT-500, 0)
        JumpPlatform(self.game, WIN_WIDTH//2+120, WIN_HEIGHT-600, 0)
        JumpPlatform(self.game, WIN_WIDTH//2-120, WIN_HEIGHT-650, 0)
        JumpPlatform(self.game, WIN_WIDTH//2-120, WIN_HEIGHT-450, 0)
    def create_enemies(self):
        while len(list(self.game.enemies)) < 2:
            EnemyFly(self.game,  WIN_WIDTH-450,rd.randint(WIN_HEIGHT-600, WIN_HEIGHT-500))
    
            #GroundPlatform(self.game, 350, 535, "wood_box")
            #GroundPlatform(self.game, 350, 530-70, "wood_box")
    def create_bullets(self):
        if self.spawn_course_bullets:
            while len(list(self.game.course_bullets)) < 1:
                print("bullet")
                CourseBullet(self.game)
    def draw_course_gun(self):
        BackgroundItem(self.game, WIN_WIDTH-250, 80, "cloud" )
        

