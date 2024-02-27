import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *



class Level:
    def __init__(self, game) -> None:
        self.scroll_timer = 0
        self.scroll_duration = 1300
        self.game = game
    def handle_checkpoint_collisions(self):
        hit = pg.sprite.spritecollide(self.game.player, self.game.check_points, True)
        if hit:
            print("hit")
            self.game.check_point_active = True
            self.game.scroll_distance = 450
            # Activate the scroll timer
            self.scroll_timer = pg.time.get_ticks()

    def update(self):
        self.handle_checkpoint_collisions()
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
        




class Level1(Level):
    def __init__(self, game):
        super().__init__(game)
        self.ground_length = 10
        self.water_length = 25
    def background(self):
        BackgroundPlatform(self.game, 100, WIN_HEIGHT//2+28, "sign_left")
        for i in range(1, self.water_length):
            BackgroundPlatform(self.game, i*70- 70, WIN_HEIGHT-70, "water")
    def new(self): 
        self.scroll_time = 0
        for i in range(1,self.ground_length):
           GroundPlatform(self.game, i*70- 70, WIN_HEIGHT//2+100)
        self.check_point_1 = CheckPoint(self.game, 500, WIN_HEIGHT//2+28)
        self.background()
    def update(self):
        return super().update()

class Level2(Level):
    def __init__(self, game):
        super().__init__(game)
        self.check_point_active_2 = False
        self.start_wall_move = False
        self.hit = False
        self.portal_closed = False
        self.vel = 1
        self.jump_platform_cordinates = [
            (800,400),
            (900,500),
            (1000, 600),
            (1100, 500),
            (1200, 200),
            (1350, 100),
            (1450, 500),
            (1450, WIN_HEIGHT-200)
        ]
    def background(self):
        BackgroundPlatform(self.game, WIN_WIDTH, WIN_HEIGHT//4, "cloud")
        BackgroundPlatform(self.game, WIN_WIDTH, WIN_HEIGHT//2, "cloud")
        BackgroundPlatform(self.game, 2000, WIN_HEIGHT-140, "flag_green")
        #BackgroundPlatform(self.game, WIN_WIDTH, WIN_HEIGHT//1, "cloud")

        #self.level_1_text = LevelGuide("level_1")
        #self.level_1_text.new_message()


    def new(self):
        self.enemies_timer = 0 
        self.platform_timer = 0
        for i in range(1,6):
            GroundPlatform(self.game, 1550 + 50 + i*70, WIN_HEIGHT-70)
        for i in range(1,7):
            PortalPlatform(self.game,1650, 70*i-150)
        for pos in self.jump_platform_cordinates:
            rand = rd.randint(0,1)
            if rand:
                MovingJumpPlatform(self.game,pos[0],pos[1], self.platform_timer)
            else:
                JumpPlatform(self.game, pos[0], pos[1], self.platform_timer)
        self.background()
        self.check_point_2 = CheckPoint(self.game, 1800, WIN_HEIGHT-140)

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
            el = EnemyFly(self.game, rd.randint(900,1000), rd.randint(WIN_HEIGHT, WIN_HEIGHT + 200))
                
    def update(self):
        super().update()
        #self.move_portal_down()
        self.move_plat()

