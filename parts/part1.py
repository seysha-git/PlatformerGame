import pygame as pg
from settings import *
from modules.items import *
from modules.platforms import *
from modules.characters import *
from modules.guide_items import *
from parts.levels import Level


class Part1(Level):
    def __init__(self, game):
        super().__init__(game)
        self.water_length = 14
        self.check_point_active_2 = False
        self.start_wall_move = False
    def background(self):
        for i in range(1,7):
            GroundPlatform(self.game, 70*i, WIN_HEIGHT-320)
        for i in range(1,11): # Nest nederste taket
            RoofPlatform(self.game, i*70+420, WIN_HEIGHT-320) #roof
        for i in range(1,5): #dør gulvet
            WallPlatform(self.game,WIN_WIDTH-380, 70*i+270)
        for i in range(1,3):
            GroundPlatform(self.game, WIN_WIDTH-520 + 70*i, WIN_HEIGHT//4+50)
        for i in range(1,5):
            WallPlatform(self.game, 420, 70*i-20)
        RoofPlatform(self.game,420, 330)
        for i in range(1,5):
           GroundPlatform(self.game, 70*i, 330)
        #for i in range(1,10):
        #    GroundPlatform(self.game, 490 + 70*i-70, WIN_HEIGHT-380, "lava")

        JumpPlatform(self.game, WIN_WIDTH-130, WIN_HEIGHT-350, 0)
        JumpPlatform(self.game, WIN_WIDTH-130, WIN_HEIGHT-150, 0)
        JumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-290, 0)
        JumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-450, 0)
        JumpPlatform(self.game, WIN_WIDTH-130, WIN_HEIGHT-520, 0)
        JumpPlatform(self.game, WIN_WIDTH-310, WIN_HEIGHT-620, 0)

        BackgroundPlatform(self.game, 70, 260, "door_mid")
        BackgroundPlatform(self.game, 70, 260-70, "door_top")
        
        Switch(self.game, 75, 510)

        JumpPlatform(self.game, WIN_WIDTH//2, WIN_HEIGHT-400, 0)
        JumpPlatform(self.game, WIN_WIDTH//2+120, WIN_HEIGHT-500, 0)
        JumpPlatform(self.game, WIN_WIDTH//2-120, WIN_HEIGHT-500, 0)
        JumpPlatform(self.game, WIN_WIDTH//3, WIN_HEIGHT-400, 0)

        GroundPlatform(self.game, 350, 330, "wood_box")
        #GroundPlatform(self.game, 350, 330-70, "wood_box")
        #print(f"Lenght of game enemies: {self.game.enemies}")

    def new(self): 
        super().new()
        self.background()
    def enter_door(self):
        hits = pg.sprite.spritecollide(self.game.player, self.game.background_sprites, False)
        if hits:
            if hits[0].type == "door_mid":
                print("move up")
                self.game.player.pos.y -= 400
                self.game.top_scroll = 400
                #self.game.scroll_page(400)
    def update(self):
        super().update()
        self.enter_door()
        #self.create_enemies()
        #self.check_colission()
    def create_enemies(self):
        while len(list(self.game.enemies)) < 2:
            EnemyFly(self.game,  WIN_WIDTH-450,rd.randint(WIN_HEIGHT-600, WIN_HEIGHT-400))
    
            #GroundPlatform(self.game, 350, 535, "wood_box")
            #GroundPlatform(self.game, 350, 530-70, "wood_box")


    
    
        

