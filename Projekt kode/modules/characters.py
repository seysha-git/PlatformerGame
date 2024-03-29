import pygame as pg
from settings import *
import math
from modules.weapons import PlayerBullet
from modules.platforms import MovingJumpPlatform
from modules.items import Key
import random as rd

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game:object, start_pos_x:int, start_pos_y:int):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.walking = False 
        self.jumping = False 
        self.on_stairs = False
        self.not_hit_portal = True
        self.on_moving_plat = False
        self.gun_active = False

        self.current_frame = 0
        self.last_update = 0
        self.keys = 0
        self.health = 100
        self.max_health = 100
        self.shots = 0
        self.hits = 0

        self.load_images()
        self.image = self.standing_frames[0]
        
        self.rect = self.image.get_rect()
        self.rect.center = (WIN_WIDTH//2, WIN_HEIGHT-MAIN_CHAR_HEIGHT/2)
        self.pos = vec(start_pos_x, start_pos_y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    def load_images(self):
        self.gun_index = 0
        self.gun_frames = [
            pg.transform.scale(pg.image.load("./images/raygun.png").convert_alpha(), (100,100)),
            pg.transform.flip(pg.transform.scale(pg.image.load("./images/raygun.png").convert_alpha(), (100,100)), True, False)
        ]
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
    def update(self):
        self.animate()
        self.move()
        self.update_gun_animation()
        """
        #if self.vel.y > 0:
         #  self.ground_plat_collission()
          # self.jump_plat_colission()
        """
        
    def move(self):
        self.acc = vec(0,MAIN_GRAVITY)
        self.vel.x = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_s]:
            self.duck()
        if keys[pg.K_d]:
            self.acc.x = MAIN_ACC
        if keys[pg.K_a]:
            self.acc.x = -MAIN_ACC
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        self.rect.midbottom = self.pos
    def jump(self): 
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.jump_platforms, False) or pg.sprite.spritecollide(self, self.game.ground_platforms, False)
        self.rect.x -= 1
        if hits and not self.jumping and self.on_stairs == False:
            self.vel.y = -MAIN_JUMP_VEL
            self.jumping = True
            #self.game.jump_sound.play()
    def duck(self):
        self.pos.y += 20
        self.image = self.duck_frame[0]
        self.image.set_colorkey("black")
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
                    self.gun_image = self.gun_frames[1]
                    self.image = self.walk_frames_l[self.current_frame]
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
    def update_gun_animation(self):
        x,y = pg.mouse.get_pos()
        if x > self.rect.x:
            self.gun_index = 0
        if x < self.rect.x:
            self.gun_index = 1 
    def get_hit_ratio(self):
         if self.hits == 0:
             return 0
         return round((self.hits/self.shots), 2)*100                   
    def draw(self):
         self.draw_healthbar() 
         self.draw_gun()
    def shoot(self, x:int,y:int):
        self.shots += 1
        if self.gun_index == 0:
            PlayerBullet(self.game, self.rect.right, self.rect.centery, 6, x,y)
        if self.gun_index == 1:
             PlayerBullet(self.game, self.rect.left, self.rect.centery, 6, x,y)      
    def draw_gun(self):
        x,y = pg.mouse.get_pos()
        angle = math.degrees(math.atan2(y - self.rect.centery, x - self.rect.centerx))
        if self.gun_index == 1:   
            angle = max(-30, min(30, angle))
            self.gun_image = self.gun_frames[self.gun_index]
            rotated_image = pg.transform.rotate(self.gun_image, angle)
            gun_rect = rotated_image.get_rect()
            blit_pos = (self.rect.left - gun_rect.width + 70, self.rect.centery - gun_rect.height // 2.5)
            self.game.screen.blit(rotated_image, blit_pos)
        if self.gun_index == 0:
            angle = max(-60, min(60, angle))
            self.gun_image = self.gun_frames[self.gun_index]
            rotated_image = pg.transform.rotate(self.gun_image, -angle) 
            self.game.screen.blit(rotated_image, (self.rect.right-50, self.rect.centery-50))
    def draw_healthbar(self):
        pg.draw.rect(self.game.screen, (255, 0,0), (self.rect.x, self.rect.y - 20, self.rect.width, 10 ))
        pg.draw.rect(self.game.screen, (00, 255,0), (self.rect.x, self.rect.y - 20, self.rect.width * (1-((self.max_health - self.health))/self.max_health), 10 ))



class Princess(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.princesses
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.spritesheet_princess.get_image( 0, 196, 66, 92)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = WIN_HEIGHT//2

        

class EnemyFly(pg.sprite.Sprite):
    def __init__(self, game:object, x:int,y:int):
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
        if self.rect.x < WIN_WIDTH-900:
            self.kill()

        self.vy += self.dy
        if self.vy > 5 or self.vy < -5:
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
        hit = pg.sprite.spritecollide(self, self.game.player_bullets, True)
        if hit:
            self.game.game_ground.player.hits += 1
            self.kill()
            if rd.randrange(2) == 1:
                Key(self.game, self.rect.x, self.rect.y)






