import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False 
        self.jumping = False 
        self.not_hit_portal = True

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
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
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


    def update(self):
        #player_portal_collide = self.collsion_rect.colliderect(portal.rect for portal in self.game.portals) 
        self.animate()
       
        self.move()
        self.acc.x += self.vel.x * -MAIN_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0 
        
        self.pos += self.vel + 0.5*self.acc
        self.rect.midbottom = self.pos
        if self.vel.y > 0:
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit

                if self.pos.y < lowest.rect.centery:
                    self.pos.y = lowest.rect.top
                    self.vel.y = 0
                    self.jumping = False
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
    def draw_healthbar(self):
        pg.draw.rect(self.game.screen, (255, 0,0), (self.rect.x, self.rect.y - 20, self.rect.width, 10 ))
        pg.draw.rect(self.game.screen, (00, 255,0), (self.rect.x, self.rect.y - 20, self.rect.width * (1-((self.max_health - self.health))/self.max_health), 10 ))
    def collision_box(self):
        vel = 20
        return pg.Rect(self.rect.x + vel, self.rect.y + vel, self.rect.width, self.rect.height)
        

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x,y, type="ground"):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = {
             "ground":self.game.spritesheet_platform.get_image(792, 0,70,70),
             "sign_left": self.game.spritesheet_platform.get_image(288, 216,70,70),
             "cloud": self.game.spritesheet_items.get_image(0, 146,128,71), 
             "green_flag":self.game.spritesheet_items.get_image(216,432,70,70),
             "button_green":self.game.spritesheet_items.get_image(419, 0,70,70),
             "button_green_pressed":self.game.spritesheet_items.get_image(418, 144,70,70),
             "lava": self.game.spritesheet_platform.get_image(504,0,70,70),
             "stone_wall": self.game.spritesheet_platform.get_image(72,288,70,70),
             "stone_jump": self.game.spritesheet_platform.get_image(144,144,70,70),
             


        }
        self.image = self.images[type]
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet_enemies.get_image(0, 32, 72, 36)
        self.image_down = self.game.spritesheet_enemies.get_image(0,0,75,31)
        self.image_up.set_colorkey("black")
        self.image_down.set_colorkey("black")
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = rd.randint(1750, 2200)
        self.rect.centery = WIN_WIDTH//2 #rd.randint(WIN_HEIGHT//2)
        self.vy = rd.randrange(1,4)

        if self.rect.centery > WIN_HEIGHT:
            self.vy *= -1
        self.rect.y = rd.randrange(WIN_HEIGHT//2)
        self.vx = 0
        self.dx = 0.5

    def update(self):
        self.rect.y -= self.vy 

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat,type="ground"):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.image = self.game.spritesheet_items.get_image(144,362,70,70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()



