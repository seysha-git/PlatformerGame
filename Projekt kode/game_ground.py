import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *
from modules.weapons import CourseBullet, PlayerBullet


class GameGround:
    def __init__(self, game):
        self.spikes_time = 0
        self.game = game
        self.ground_length = 23
        self.spawn_course_bullets = False
    def update(self):
        self.player_wall_collision_x()
        self.player_wall_collision_y()
        self.player_ladder_colission()
        self.player_spike_colission()
        self.handle_checkpoint_collisions()
        self.create_bullets()
        #self.player_key_pickup()
        #self.create_enemies()
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
                    print("hello")
                    self.game.all_message_completed = True
            if event.type == pg.MOUSEBUTTONDOWN:
                x,y = pg.mouse.get_pos()
                self.player.shoot(x,y)     
    def new(self):
        self.side_field_backgrounds()
        self.start_runner_room()
        self.jump_gun_room()
        self.question_room()
        self.shoot_room()
        self.player = Player(self.game, WIN_WIDTH-200, WIN_HEIGHT//2)
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
        
    def player_key_pickup(self):
        hits = pg.sprite.spritecollide(self.player, self.game.background_sprites, True)
        if hits:
            print("key picked up")

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
            if hits[0].type == "2":
                self.player.gun_active = True
            elif hits[0].type == "3":
                self.game.quiz_active = True
            self.game.create_new_message()
    def question_room(self):
        for i in range(1,7):
            GroundPlatform(self.game, 70*i, WIN_HEIGHT-360)
        for i in range(1,5):
           WallPlatform(self.game, 495, 70*i-20)
        for i in range(1,3):
           GroundPlatform(self.game, 70*i, 200, "half_ground")
        self.key = BackgroundBlocks(self.game, 160, 180, "tresure")
        BackgroundBlocks(self.game, 75, 130, "door_mid")
        BackgroundBlocks(self.game, 75, 130-70, "door_top")
        JumpPlatform(self.game, 350, 400)
        JumpPlatform(self.game, 350, 300)
        JumpPlatform(self.game, 250, 240)
        Checkpoint(self.game, 340, WIN_HEIGHT//2+19, "3")
    def jump_gun_room(self):
        for i in range(1,6): #dør gulvet
            WallPlatform(self.game,WIN_WIDTH-380, 70*i+180)
        for i in range(1,3):
            GroundPlatform(self.game, WIN_WIDTH-520 + 70*i, 210, "half_ground")
        JumpPlatform(self.game, WIN_WIDTH-130, WIN_HEIGHT-190)
        JumpPlatform(self.game, WIN_WIDTH-240, WIN_HEIGHT-478)
        MovingJumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-320, 0, 1)
        MovingJumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-620, 0, -1)
        Checkpoint(self.game, WIN_WIDTH-390, 130, "2")
        BackgroundBlocks(self.game, WIN_WIDTH-250, 80, "cloud" )

    def start_runner_room(self):
        for i in range(1,11): # Nest nederste taket
            RoofPlatform(self.game, i*70+420, WIN_HEIGHT-360) #roof
        for i in range(1,5):
            BackgroundBlocks(self.game, 499, WIN_HEIGHT-50 - 40*i, "stairs")
        for i in range(1,8):
            GroundPlatform(self.game, 500 + 70*i, WIN_HEIGHT-200, "half_ground")
        for i in range(1,5):
            BackgroundBlocks(self.game, 1060, WIN_HEIGHT-50 - 40*i, "stairs")
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
        JumpPlatform(self.game, WIN_WIDTH//2, WIN_HEIGHT-500)
        JumpPlatform(self.game, WIN_WIDTH//2+120, WIN_HEIGHT-600)
        JumpPlatform(self.game, WIN_WIDTH//2-120, WIN_HEIGHT-650)
        JumpPlatform(self.game, WIN_WIDTH//2-120, WIN_HEIGHT-450)
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