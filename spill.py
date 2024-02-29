import pygame as pg
import sys
import random as rd

# Initierer pygame
pg.init()

font = pg.font.SysFont('Arial', 25)
tekst = "Poeng:"
poeng= 0

# Konstanter
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTYELLOW = (253, 250, 114)
BABYBLUE = (137, 207, 240)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

#Bakgrunn
background_img1 = pg.image.load('stein.png')
background_img1 = pg.transform.scale(background_img1, (300, 300))
background_img2 = pg.image.load('stein.png')
background_img2 = pg.transform.scale(background_img2, (300, 300))
background_img3 = pg.image.load('stein.png')
background_img3 = pg.transform.scale(background_img3, (300, 300))
background_img4 = pg.image.load('stein.png')
background_img4 = pg.transform.scale(background_img4, (300, 300))
green_img = pg.image.load('green.png')
green_img = pg.transform.scale(green_img, (100, 600))

ghost_img = pg.image.load('ghost.png')
ghost_img = pg.transform.scale(ghost_img, (30, 30))

sau_img = pg.image.load('sau.png')
sau_img = pg.transform.scale(sau_img, (30, 30))

gjerde_img = pg.image.load('gjerde.png')
gjerde_img = pg.transform.scale(gjerde_img, (25, 75))

menneske_img = pg.image.load('menneske.png')
menneske_img = pg.transform.scale(menneske_img, (30, 30))


# Lager en overflate vi kan tegne pa
surface = pg.display.set_mode(SIZE)

# Lager klokke
clock = pg.time.Clock()

# Variabel som styrer om spillet skal kjores
run = True

# Klasser
class Spillbrett:
    spokelser = [] # Liste av Spøkelse. List<Spøkelse>
    hindringer = [] # Liste av Hindring. List<Hindring>
    sauer = [] # Liste av Sau. 

    def leggTilSpillObjekt(self,spillobjekt): 
        if isinstance(spillobjekt, Spokelse):
            self.spokelser.append(spillobjekt)
            
        
        elif isinstance(spillobjekt, Hindring):
            self.hindringer.append(spillobjekt)
            

        else:
            self.sauer.append(spillobjekt)
            
    def fjernSpillObjekt(self, spillobjekt):
        if isinstance(spillobjekt, Spokelse):
            spokelse.pop(spillobjekt)
        
        elif isinstance(spillobjekt, Hindring):
            hindringer.pop(spillobjekt)

        else:
            self.sau.remove(spillobjekt)

    def antallPoeng(self):
        text_img = font.render(f"{tekst} {poeng}", True, BLACK)
        surface.blit(text_img, (0, 50))


class Spillobjekt:
    def __init__(self, xPosisjon, yPosisjon):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon

    def settPosisjon(self, x, y):
        self.xPosisjon = x
        self.yPosisjon = y


    def hentPosisjon(self):
        return (self.xPosisjon, self.yPosisjon)


class Spokelse(Spillobjekt):
    def __init__(self):
        super().__init__(rd.randint(100, WIDTH - 200), rd.randint(0, HEIGHT - 25))
        self.vx = 3
        self.vy = 3

    def tegnSpokelse(self):
        #pg.draw.rect(surface, BLUE, [self.xPosisjon, self.yPosisjon, 25, 25])
        surface.blit(ghost_img,(self.xPosisjon, self.yPosisjon))
        self.yPosisjon += self.vy
    
    def endreRetning(self):
        self.xPosisjon += self.vx
        self.yPosisjon += self.vy
        
        if self.xPosisjon <= 100 or self.xPosisjon > WIDTH - 125:
            self.vx *= -1

        if self.yPosisjon > HEIGHT - 25 or self.yPosisjon < 0:
            self.vy *= -1

    def hentRektangel(self):
        return pg.Rect(self.xPosisjon, self.yPosisjon, 25, 25)

    def frys(self):
        self.vx = 0
        self.vy = 0

class Menneske(Spillobjekt):
    
    def __init__(self, fart, poeng, holderSau):
        super().__init__(rd.randint(0, 100 - 25), rd.randint(0, HEIGHT - 25))
        self.fart = fart
        self.poeng = poeng
        self.holderSau = False
        self.sauSomErHoldt = None 

    def hentRektangel(self):
        return pg.Rect(self.xPosisjon, self.yPosisjon, 25, 25)

    #Liten "sikkerhets rektangel foran det faktiske rektangelet. Forhindrer at kollisjon alltid er True, slik at man aldri kommer seg vekk fra hindringen."
    def hentNesteRektangel(self, dx, dy):
        return pg.Rect(self.xPosisjon + dx, self.yPosisjon + dy, 25, 25)

    def settHastighet(self, vx,vy):
        self.vx = vx
        self.vy = vy

    def beveg(self, hindringer):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            if not any(self.hentNesteRektangel(-5,0).colliderect(hindring.hentRektangel()) for hindring in hindringer) and self.xPosisjon >= 0:
                self.xPosisjon -= self.vx
        if keys[pg.K_RIGHT]:
            if not any(self.hentNesteRektangel(5,0).colliderect(hindring.hentRektangel()) for hindring in hindringer) and self.xPosisjon <= WIDTH - W:
                self.xPosisjon += self.vx
        if keys[pg.K_DOWN]:
            if not any(self.hentNesteRektangel(0,2).colliderect(hindring.hentRektangel()) for hindring in hindringer) and self.yPosisjon <= HEIGHT - H:
                self.yPosisjon += self.vy
        if keys[pg.K_UP]:
            if not any(self.hentNesteRektangel(0,-2).colliderect(hindring.hentRektangel()) for hindring in hindringer) and self.yPosisjon >= 0:
                self.yPosisjon -= self.vy

class Hindring(Spillobjekt):
    def __init__(self):
        super().__init__(rd.randint(100, WIDTH - 125), rd.randint(0, HEIGHT - 25))

    def tegnHindring(self):
        #pg.draw.rect(surface, BLACK, [self.xPosisjon, self.yPosisjon, 25, 75])
        surface.blit(gjerde_img,(self.xPosisjon, self.yPosisjon))
    def hentRektangel(self):
        return pg.Rect(self.xPosisjon, self.yPosisjon, 25, 75)


class Sau(Spillobjekt):
    def __init__(self):
        super().__init__(rd.randint(WIDTH - 100, WIDTH-25), rd.randint(0,HEIGHT - 25))

    def tegnSau(self):
        #pg.draw.rect(surface, GREEN, [self.xPosisjon, self.yPosisjon, 25, 25])
        surface.blit(sau_img,(self.xPosisjon, self.yPosisjon))

    def hentRektangel(self):
        return pg.Rect(self.xPosisjon, self.yPosisjon, 25, 25)

# Oppretter menneskeobjektet
menneske = Menneske(0, 0, False)
menneske.settHastighet(5,5)

W = 25
H = 25

spillbrett = Spillbrett()

# Lager 3 sauer som skal være der fra start
for i in range(0,3):
    hindring = Hindring()
    spillbrett.leggTilSpillObjekt(hindring)
    sau = Sau()
    spillbrett.leggTilSpillObjekt(sau)

spokelse = Spokelse()
spillbrett.leggTilSpillObjekt(spokelse)

# Spill-lokken
while run:
    # Sorger for at lokken kjores i korrekt hastighet
    clock.tick(FPS)

    # Gar gjennom hendelser (events)
    for event in pg.event.get():
        # Sjekker om vi onsker a lukke vinduet
        if event.type == pg.QUIT:
            run = False  # Spillet skal avsluttes

    # Kaller menneske bevegmetoden
    menneske.beveg(spillbrett.hindringer)

    if any(menneske.hentRektangel().colliderect(spokelse.hentRektangel()) for spokelse in spillbrett.spokelser):
        for spokelse in spillbrett.spokelser:
            spokelse.frys()
            font = pg.font.SysFont('Arial', 160)
            tekst = "game over"
            poeng = ""
            
        menneske.settHastighet(0,0)
  
    for sau in spillbrett.sauer:
        if not menneske.holderSau:
            if menneske.hentRektangel().colliderect(sau.hentRektangel()):
                menneske.holderSau = True
                menneske.sauSomErHoldt = sau
                menneske.settHastighet(3, 3)

    if menneske.holderSau and 30 < menneske.sauSomErHoldt.hentPosisjon()[0] < 100:
        menneske.sauSomErHoldt.settPosisjon(-100,-100)
        spillbrett.leggTilSpillObjekt(Sau())
        spillbrett.leggTilSpillObjekt(Spokelse())
        spillbrett.leggTilSpillObjekt(Hindring())
        poeng += 1
        menneske.settHastighet(5, 5)
        menneske.sauSomErHoldt = None
        menneske.holderSau = False

    for sau in spillbrett.sauer:
        if menneske.holderSau and sau is menneske.sauSomErHoldt:
            sau.settPosisjon(menneske.hentPosisjon()[0]+5, menneske.hentPosisjon()[1])
        sau.tegnSau()

    #pg.draw.rect(surface, LIGHTYELLOW, [0, 0, 100, HEIGHT])
    surface.blit(green_img,(0, 0))
    
    #pg.draw.rect(surface, LIGHTYELLOW, [WIDTH - 100, 0, 100, HEIGHT])
    surface.blit(green_img,(WIDTH-100, 0))
    
    #pg.draw.rect(surface, BABYBLUE, [100, 0, WIDTH - 200, HEIGHT])
    
    surface.blit(background_img1, (100, 0))
    surface.blit(background_img1, (400, 0))
    surface.blit(background_img1, (100, 300))
    surface.blit(background_img1, (400, 300))

    # Tegner Menneske
    #pg.draw.rect(surface, RED, [menneske.xPosisjon, menneske.yPosisjon, W, H])
    surface.blit(menneske_img,(menneske.xPosisjon, menneske.yPosisjon))
    
    # Tegner spokelsene
    for spokelse in spillbrett.spokelser:
        spokelse.tegnSpokelse()
        spokelse.endreRetning()

    for hindring in spillbrett.hindringer:
        hindring.tegnHindring()

    for sau in spillbrett.sauer:
        sau.tegnSau()
      

    spillbrett.antallPoeng()
        
    # "Flipper" displayet for a vise hva vi har tegnet
    pg.display.flip()

# Avslutter pygame
pg.quit()
sys.exit()

