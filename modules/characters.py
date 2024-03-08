import pygame as pg
from settings import *
import sys
from modules.platforms import MovingJumpPlatform
#from modules.weapons import Bullet
import random as rd
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False 
        self.ducking = False
        self.jumping = False 
        self.not_hit_portal = True
        self.on_moving_plat = False

        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]

        self.rect = self.image.get_rect()
        self.rect.center = (WIN_WIDTH//2, WIN_HEIGHT-MAIN_CHAR_HEIGHT/2)
        self.pos = vec(199, WIN_HEIGHT-70) #WIN_WIDTH+400
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
            self.game.spritesheet_char.get_image(146, 0, 72, 97),
        ]

        self.duck_frame =  [
            self.game.spritesheet_char.get_image(365, 98, 69, 71),
            pg.transform.flip(self.game.spritesheet_char.get_image(365, 98, 69, 71), True, False)
        ]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey("black")
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
            
        self.jump_frame = [
            self.game.spritesheet_char.get_image(438,93,67,94),
            pg.transform.flip(self.game.spritesheet_char.get_image(438,93,67,94), True, False)
            
        ]


    def jump(self): 
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.jump_platforms, False) or pg.sprite.spritecollide(self, self.game.ground_platforms, False)
        self.rect.x -= 1
        if hits and not self.jumping:
            self.vel.y = -MAIN_JUMP_VEL
            self.jumping = True
            #self.game.jump_sound.play()
    def collide_with_check_point(self):
        ...
    def enemies_collision(self):
        enemies = pg.sprite.spritecollide(self, self.game.enemies, True, pg.sprite.collide_mask)
        if enemies:
            self.health -= 20
    def check_alive(self):
        if self.health < 10:
            print("dead")
            self.game.playing = False
    def shoot_bullets(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                x,y = pg.mouse.get_pos()     
                print(x,y)
    def hit_lava(self):
        hit = pg.sprite.spritecollide(self, self.game.ground_platforms, False)

        if hit:
            for i in hit:
                if i.type == "lava":
                    print("dead")
    def update(self):
        #player_portal_collide = self.collsion_rect.colliderect(portal.rect for portal in self.game.portals) 
        self.animate()
        self.enemies_collision()
        self.move()
        self.hit_lava()
        self.check_alive()
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
                    lowest = jump_plat_hit[0]
                if isinstance(hit,MovingJumpPlatform):
                    self.on_moving_plat = True
                    self.pos.x=  hit.rect.centerx
            if self.pos.x < lowest.rect.right + 10 \
                and self.pos.x > lowest.rect.left - 10:
                    if self.pos.y < lowest.rect.centery:
                        self.pos.y = lowest.rect.top
                        self.vel.y = 0
                        self.jumping = False
                     

    def powerup_collision(self):
        pow_hits = pg.sprite.spritecollide(self, self.game.powerups, True)
        for pow in pow_hits:
            if pow.type == "gems":
                pass
                #self.game.gems_sound.play()
    def move(self):
        self.acc = vec(0,MAIN_GRAVITY)
        self.vel.x = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_s]:
            self.duck("right")
            self.ducking = True
        if keys[pg.K_d]:
            self.acc.x = MAIN_ACC
        if keys[pg.K_a]:
            self.acc.x = -MAIN_ACC
        
        #self.acc.x += self.vel.x# * -MAIN_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0 
        self.pos += self.vel + 0.5*self.acc
        self.rect.midbottom = self.pos
            
    def animate(self):
        now = pg.time.get_ticks()
        if self.jumping:
            if self.vel.x> 0:
                self.image = self.jump_frame[0]
                self.image.set_colorkey("black")
                
            elif self.vel.x < 0:
                self.image = self.jump_frame[-1]
                self.image.set_colorkey("black")
        if self.vel.x !=0:
            self.walking = True 
        else:
            self.walking = False 
        if self.walking:
            if now -self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                    #if self.ducking:
                     #   self.duck("left")
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if not self.jumping and not self.walking:
            if now - self.last_update > 200:
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
    def duck(self, dir="right"):
        self.pos.y += 20
        if dir == "right":
            self.image = self.duck_frame[0]
            self.image.set_colorkey("black")
        elif dir == "left":
            self.image = self.duck_frame[1]
            self.image.set_colorkey("black")
        else:
            self.image = self.duck_frame[0]
            self.image.set_colorkey("black")








class EnemyFly(pg.sprite.Sprite):
    def __init__(self, game, x,y):
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
        self.rect.x = x
        self.rect.y = y
        self.vx = rd.randrange(4,8)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.bullet_colission()
        self.rect.x -= self.vx 
        self.mask = pg.mask.from_surface(self.image)
        if self.rect.x < WIN_WIDTH-1000:
            self.kill()
            print("kill")

        self.vy += self.dy
        if self.vy > 4 or self.vy < -5:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
    def bullet_colission(self):
        hit = pg.sprite.spritecollide(self, self.game.bullets, True)
        if hit:
            self.kill()





