import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *
from modules.weapons import CourseBullet, PlayerBullet


class GameGround:
    def __init__(self, game:object):
        self.start_toggle_time = 0
        self.game = game
        self.ground_length = 23
        self.spawn_course_bullets = False
        self.game_door_arrived = True
    def update(self):
        self.player_wall_collision_x()
        self.player_wall_collision_y()
        self.player_jump_colissions()

        self.player_ladder_colission()
        self.handle_checkpoint_collisions()
        self.player_enemies_colission()
        self.player_door_colission()
        self.player_spike_colission()
        self.player_lava_colission()
        
        self.move_wall_down()
        self.check_player_alive()
        
        self.update_create_bullets()
        self.player_key_pickup()
        self.create_enemies()

        
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.game.playing:
                    self.game.playing = False
                self.game.running = False 
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_w or event.key == pg.K_SPACE) and not self.player.on_stairs:
                    self.player.jump()
                if event.key == pg.K_RETURN:
                    self.game.all_message_completed = True
            if event.type == pg.MOUSEBUTTONDOWN:
                x,y = pg.mouse.get_pos()
                self.player.shoot(x,y)     
    def new(self):
        self.side_field_backgrounds()
        self.start_runner_room()
        self.jump_gun_room()
        self.shoot_room()
        self.player = Player(self.game, 200,WIN_HEIGHT-100)
    def player_key_pickup(self):
        hits = pg.sprite.spritecollide(self.player, self.game.keys, False)
        if hits:
            self.player.keys += 1
            hits[0].kill()
    def player_ladder_colission(self):
        hits = pg.sprite.spritecollide(self.player, self.game.background_sprites, False)
        if not hits:
            self.on_stairs = False
        else:
            for hit in hits:
                if hit.type == "stairs" or hit.type=="rope":
                    keys = pg.key.get_pressed()
                    self.on_stairs = True
                    if keys[pg.K_w]:
                        self.player.vel.y = -5
    def player_spike_colission(self):
        hits = pg.sprite.spritecollide(self.player, self.game.spikes, False)
        if hits:
            if hits[0].index == 0:
                self.player.health -= 20
                hits[0].toggle_spike()
    def player_door_colission(self):
        hits = pg.sprite.spritecollide(self.player, self.game.background_sprites, False)
        if hits:
            for hit in hits:
                if hit.type == "door_open_mid":
                    self.game.playing = False
                    self.game.completed = True
    def player_wall_collision_x(self):
        wall_hits = pg.sprite.spritecollide(self.player, self.game.walls, False)
        for tile in wall_hits:
                if self.player.vel.x > 0:
                    self.player.pos.x = tile.rect.left - self.player.rect.w+30
                    self.player.rect.x = self.player.pos.x
                elif self.player.vel.x < 0:
                    self.player.pos.x = tile.rect.right + self.player.rect.w-30
                    self.player.rect.x = self.player.pos.x
    def player_wall_collision_y(self):
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
    def player_enemies_colission(self):
        enemies = pg.sprite.spritecollide(self.player, self.game.enemies, True)
        if enemies:
            self.player.health -= 20
    def player_lava_colission(self):
        hit = pg.sprite.spritecollide(self.player, self.game.ground_platforms, False)
        if hit:
            for i in hit:
                if i.type == "lava":
                    pass
    def player_jump_colissions(self):
        if self.player.vel.y > 0:
            self.player_ground_plat_collission()
            self.player_jump_plat_colission()
    def player_ground_plat_collission(self):
        hits = pg.sprite.spritecollide(self.player, self.game.ground_platforms, False)
        if hits:
            if self.player.pos.y < hits[0].rect.bottom:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.jumping = False
    def player_jump_plat_colission(self):
        jump_plat_hit = pg.sprite.spritecollide(self.player, self.game.jump_platforms, False)
        if jump_plat_hit:
            lowest = jump_plat_hit[0]
            for hit in jump_plat_hit:
                if hit.rect.bottom > lowest.rect.bottom:
                    lowest = jump_plat_hit[0]
                if isinstance(lowest,MovingJumpPlatform):
                    self.player.on_moving_plat = True
                    self.player.pos.x=  lowest.rect.centerx
            if self.player.pos.x < lowest.rect.right + 10 \
                and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
    def handle_checkpoint_collisions(self):
        hits = pg.sprite.spritecollide(self.player, self.game.check_points, True)
        if hits:
            if hits[0].type == "1":
                self.spawn_course_bullets = True
            if hits[0].type == "2":
                self.player.gun_active = True
            elif hits[0].type == "3":
                self.game.quiz_active = True
            self.game.create_new_message()
    def move_wall_down(self):
        if self.player.keys >= 3:
            for wall in self.game.walls:
                if wall.type == "portal":
                    if wall.rect.y > 50:
                        wall.rect.y -= 1  
    def check_player_alive(self):
         if self.player.health < 10:
            self.game.playing = False
            self.game.player_dead = True
    def side_field_backgrounds(self):
        for i in range(1,15):
            WallPlatform(self.game,WIN_WIDTH-60, 70*i-180)
        for i in range(1,15):
            WallPlatform(self.game,0, 70*i-180)
        for i in range(1,self.ground_length):
           GroundPlatform(self.game, i*70- 70, WIN_HEIGHT-30)
        for i in range(1,self.ground_length):
           RoofPlatform(self.game, i*70- 70, -30)                  
    def jump_gun_room(self):
        for i in range(1,7): #dør gulvet
            WallPlatform(self.game,WIN_WIDTH-380, 70*i+120)
        for i in range(1,3):
            GroundPlatform(self.game, WIN_WIDTH-520 + 70*i, 150, "half_ground")
        BackgroundBlocks(self.game, WIN_WIDTH-150, WIN_HEIGHT-190-135, "umbrella_shield")
        JumpPlatform(self.game, WIN_WIDTH-130, WIN_HEIGHT-190)
        MovingJumpPlatform(self.game, WIN_WIDTH-200, WIN_HEIGHT-320, self.start_toggle_time, 1)
        BackgroundBlocks(self.game, WIN_WIDTH-320, WIN_HEIGHT-460-135, "umbrella_shield")
        JumpPlatform(self.game, WIN_WIDTH-300, WIN_HEIGHT-460)
        MovingJumpPlatform(self.game, WIN_WIDTH-180, WIN_HEIGHT-580, self.start_toggle_time, -1)
        for i in range(1,3):
            BackgroundBlocks(self.game, WIN_WIDTH-250, 70*i-20, "rope")
        Checkpoint(self.game, WIN_WIDTH-390, 80, "2")
        #BackgroundBlocks(self.game, WIN_WIDTH-250, 80, "cloud" )
    def start_runner_room(self):
        for i in range(1,16): # Nest nederste taket
            RoofPlatform(self.game, i*70, WIN_HEIGHT-360) #roof
        for i in range(1,5):
            BackgroundBlocks(self.game, 499, WIN_HEIGHT-50 - 40*i, "stairs")
        for i in range(1,8):
            GroundPlatform(self.game, 495 + 70*i, WIN_HEIGHT-190, "half_ground")
        for i in range(1,5):
            BackgroundBlocks(self.game, 1060, WIN_HEIGHT-50 - 40*i, "stairs")
        for i in range(1,3):
            for j in range(1,8):
                WallPlatform(self.game, 500 + 69*j,WIN_HEIGHT-230+70*i, type="block")
        Spike(self.game, 630, WIN_HEIGHT-260, 0,self.start_toggle_time)
        Spike(self.game, 810, WIN_HEIGHT-290, 1, self.start_toggle_time)
        Spike(self.game, 950, WIN_HEIGHT-260, 0, self.start_toggle_time)
        Checkpoint(self.game, 1150, WIN_HEIGHT-100, "1")
    def shoot_room(self):
        for i in range(1,16):
            GroundPlatform(self.game, 70*i, 515, "lava")
        JumpPlatform(self.game, WIN_WIDTH//2, WIN_HEIGHT-500)
        JumpPlatform(self.game, WIN_WIDTH//2+120, WIN_HEIGHT-600)
        JumpPlatform(self.game, WIN_WIDTH//2-120, WIN_HEIGHT-650)
        JumpPlatform(self.game, WIN_WIDTH//2-120, WIN_HEIGHT-450)
        JumpPlatform(self.game, WIN_WIDTH//2-350, WIN_HEIGHT-500)
        JumpPlatform(self.game, WIN_WIDTH//2-450, WIN_HEIGHT-600)
        BackgroundBlocks(self.game, 75, 130, "door_open_mid")
        BackgroundBlocks(self.game, 75, 130-70, "door_open_top")
        for i in range(1,8):
           WallPlatform(self.game, 495, 70*i-20, "portal")
        for i in range(1,3):
           GroundPlatform(self.game, 70*i, 200, "half_ground")
        for i in range(1,3):
            BackgroundBlocks(self.game, 250, 70*i-20, "rope")
    def create_enemies(self):
        while len(list(self.game.enemies)) < 1:
            EnemyFly(self.game,  WIN_WIDTH-450,rd.randint(WIN_HEIGHT-750, WIN_HEIGHT-450))
    
            #GroundPlatform(self.game, 350, 535, "wood_box")
            #GroundPlatform(self.game, 350, 530-70, "wood_box")
    def update_create_bullets(self):
        if self.spawn_course_bullets:
            while len(list(self.game.course_bullets)) < 1:
                CourseBullet(self.game)
