import pygame as pg
from settings import *
from modules.platforms import MovingJumpPlatform
import random as rd
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False 
        self.jumping = False 
        self.not_hit_portal = True
        self.on_moving_plat = False

        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]

        self.rect = self.image.get_rect()
        self.rect.center = (WIN_WIDTH//2, WIN_HEIGHT-MAIN_CHAR_HEIGHT/2)
        self.collision_rect = self.collision_box()
        self.pos = vec(WIN_WIDTH//2-300, WIN_HEIGHT//2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
        self.max_health = 100
    def load_images(self):
        self.standing_frames = [
            self.game.spritesheet_char.get_image(0, 196, 66, 92),
            self.game.spritesheet_char.get_image(67, 196, 66, 92),
        ]
        for frame in self.standing_frames:
            frame.set_colorkey("black")
        self.walk_frames_r = [
            self.game.spritesheet_char.get_image(0, 0, 72, 97),
            self.game.spritesheet_char.get_image(73, 0, 72, 97),
        ]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey("black")
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
            
        self.jump_frame = self.game.spritesheet_char.get_image(438,93,67,94)
        self.jump_frame.set_colorkey("black")

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.jump_platforms, False) or pg.sprite.spritecollide(self, self.game.ground_platforms, False)
        self.rect.x -= 1
        if hits and not self.jumping:
            self.vel.y = -MAIN_JUMP_VEL
            self.jumping = True
            self.game.jump_sound.play()
    def collide_with_check_point(self):
        ...
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def enemies_collision(self):
        enemies = pg.sprite.spritecollide(self, self.game.enemies, True, pg.sprite.collide_mask)
        if enemies:
            self.health -= 20
    def check_alive(self):
        if self.health < 10:
            print("dead")
            self.game.playing = False
    def update(self):
        #player_portal_collide = self.collsion_rect.colliderect(portal.rect for portal in self.game.portals) 
        self.animate()
        self.enemies_collision()
        self.move()
        self.check_alive()
        if pg.sprite.spritecollide(self, self.game.portals, False):
            self.pos.x -= 70
        self.acc.x += self.vel.x * -MAIN_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0 
        
        self.pos += self.vel + 0.5*self.acc
        self.rect.midbottom = self.pos
        if self.vel.y > 0:
            self.ground_plat_collission()
            self.jump_plat_colission()
            self.powerup_collision()
    def ground_plat_collission(self):
        hits = pg.sprite.spritecollide(self, self.game.ground_platforms, False)
        if hits:
            if self.pos.y < hits[0].rect.bottom:
                self.pos.y = hits[0].rect.top
                self.vel.y = 0
                self.jumping = False
    def jump_plat_colission(self):
        jump_plat_hit = pg.sprite.spritecollide(self, self.game.jump_platforms, False)
        if jump_plat_hit:
            lowest = jump_plat_hit[0]
            for hit in jump_plat_hit:
                if hit.rect.bottom > lowest.rect.bottom:
                    lowest = jump_plat_hit
                if isinstance(hit,MovingJumpPlatform):
                    self.on_moving_plat = True
            if self.pos.y < lowest.rect.centery:
                self.pos.y = lowest.rect.top
                self.vel.y = 0
                self.jumping = False


    def powerup_collision(self):
        pow_hits = pg.sprite.spritecollide(self, self.game.powerups, True)
        for pow in pow_hits:
            if pow.type == "gems":
                self.game.gems_sound.play()
    def move(self):
        self.acc = vec(0,MAIN_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            a = False
            for portal in self.game.portals:
                if self.collision_rect.colliderect(portal.rect):
                    a = True
            if a == False:
                self.acc.x = MAIN_ACC
        if keys[pg.K_a]:
            self.acc.x = -MAIN_ACC

            
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x !=0:
            self.walking = True 
        else:
            self.walking = False 
        if self.walking:
            if now -self.last_update > 300:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)
    def draw_healthbar(self):
        pg.draw.rect(self.game.screen, (255, 0,0), (self.rect.x, self.rect.y - 20, self.rect.width, 10 ))
        pg.draw.rect(self.game.screen, (00, 255,0), (self.rect.x, self.rect.y - 20, self.rect.width * (1-((self.max_health - self.health))/self.max_health), 10 ))
    def collision_box(self):
        vel = 20
        return pg.Rect(self.rect.x + vel, self.rect.y + vel, self.rect.width, self.rect.height)
        


class EnemyFly(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = ENEMIES_LAYER
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet_enemies.get_image(0, 32, 72, 36)
        self.image_down = self.game.spritesheet_enemies.get_image(0,0,75,31)
        self.image_up.set_colorkey("black")
        self.image_down.set_colorkey("black")
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = rd.randint(WIN_WIDTH//2 + 300, WIN_WIDTH//2 + 400)
        self.rect.centery = rd.randint(WIN_HEIGHT, WIN_HEIGHT+50)
        self.vy = rd.randrange(2,4)

        #if self.rect.centery > WIN_HEIGHT:
         #   self.vy *= -1
        self.rect.y = 600
        #self.vx = 0
        self.dx = 0.5

    def update(self):
        self.rect.y -= self.vy 
        self.mask = pg.mask.from_surface(self.image)
