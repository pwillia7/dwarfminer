import pygame, sys, os
from pygame.locals import *
import random
# Initialize program
pygame.init()

# Attempt to get files working with py2exe and similar programs. Have not been successfull so far
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# load and set the logo and Name
logoImg = resource_path('assets/images/32.png')
logo = pygame.image.load(logoImg)
pygame.display.set_icon(logo)
pygame.display.set_caption("Dwarf Miner")

# Set Dimensions
screenHeight = 640
screenWidth = 480

# Set Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)

# Create Screen (extra 100 is for status display needs fixing)
screen = pygame.display.set_mode((screenWidth,screenHeight+100))


# Set Play Area in blocks
playAreaX = 15
playAreaY = 20

# Set Acquifer params
acquiferMin = 5
acquiferMax = 7

# Initialize gameMap and load images
gameMap = []
DwarfF = resource_path('assets/images/dwarf.png')
DirtF = resource_path('assets/images/dirt.png')
DampF = resource_path('assets/images/damp.png')
WaterF = resource_path('assets/images/water.png')
AdamF = resource_path('assets/images/adam.png')
dirtImg = pygame.image.load(DirtF)
altDirtImg = pygame.transform.flip(dirtImg,True,True)
altAltDirtImg = pygame.transform.flip(dirtImg, True, False)
dampImg = pygame.image.load(DampF)
waterImg = pygame.image.load(WaterF)
adamImg = pygame.image.load(AdamF)

# Retrieve Tile 
def retTile(pos):
    return gameMap[pos[1]][pos[0]]

# Generate map as array of arrays
def generateMap(xLen,yLen):
    for i in range(yLen):
        newArray = []
        gameMap.append(newArray)
        for j in range(xLen):
            gameMap[i].append(0)
    gameMap[playAreaY-1][playAreaX-1] = 3

# Generate Acquifer and damp tiles
def generateAcquifer(minSize,maxSize):
    # Water Tiles are 1; Damp tiles are 2; umined 0; adamantium 3
    size = random.randint(acquiferMin,acquiferMax)
    orgCoord = []
    orgCoord.append(random.randint(3,playAreaY-(size))-1)
    orgCoord.append(random.randint(3,playAreaX-(size))-1)
    for i in range(size):
        for j in range(size):
            gmapYpos = orgCoord[0] + i
            gmapXpos = orgCoord[1] + j
            gameMap[gmapYpos][gmapXpos] = 1
    size += 2
    for k in range(size):
        for l in range(size):
            if gameMap[orgCoord[0]-1+k][orgCoord[1]-1+l] == 0: 
                gameMap[orgCoord[0]-1+k][orgCoord[1]-1+l] = 2
    
# Draw map graphics    
def drawMap():
    for i in range(playAreaY):
        for j in range(playAreaX):
            x = j * 32 
            y = i * 32
            rand = random.random()
            if rand > .3 and rand < .6:
                screen.blit(altDirtImg, (x,y))
            if rand < .3:
                screen.blit(altAltDirtImg, (x,y))
            else:
                screen.blit(dirtImg, (x,y))
                

# Detect collisions
def collision(self):
    if retTile(self.pos) == 2:
        print("damp")
        self.state = 2
        font = pygame.font.SysFont('arial', 20)
        text = font.render('Hmm. A damp block...', True,RED,BLACK)
        textRect = text.get_rect()
        textRect.center = screenWidth//2,screenHeight+50
        screen.blit(text,textRect)
    elif retTile(self.pos) == 1:
        print("dead")
        self.state = 1
        font = pygame.font.SysFont('arial', 20)
        text = font.render('You drowned... Try again', True,RED,BLACK)
        textRect = text.get_rect()
        textRect.center = screenWidth//2,screenHeight+50
        screen.blit(text,textRect)
    elif retTile(self.pos) == 3:
        self.state = 3
        font = pygame.font.SysFont('arial', 20)
        text = font.render('ADAMANTIUM! YOU WIN', True,RED,BLACK)
        textRect = text.get_rect()
        textRect.center = screenWidth//2,screenHeight+50
        screen.blit(text,textRect)
    else:
        self.state = 0
        pygame.draw.rect(screen,BLACK,pygame.Rect(0,screenHeight,screenWidth,100))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.pos = [0,0]
        self.state = 0
        self.image = pygame.image.load(DwarfF)
        self.rect = self.image.get_rect()
        self.rect.bottom = screenHeight
        self.oldRect = self.image.get_rect()
        screen.fill(BLACK,self.rect)
        screen.blit(self.image,self.rect)

    def update(self):
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            self.oldRect = self.rect.copy()
            if self.rect.left > 0:
                if event.key == pygame.K_LEFT:
                    self.rect.move_ip(-32, 0)
                    self.pos[0] -= 1
                    collision(self)
            if self.rect.right < screenWidth:
                if event.key == pygame.K_RIGHT:
                    self.rect.move_ip(32, 0)
                    self.pos[0] += 1
                    collision(self)
            if self.rect.top > 0:
                if event.key == pygame.K_UP:
                    self.rect.move_ip(0, -32)
                    self.pos[1] += 1
                    collision(self)
            if self.rect.bottom < screenHeight:
                if event.key == pygame.K_DOWN:
                    self.rect.move_ip(0,32)
                    self.pos[1] -=1
                    collision(self)
            print(self.pos)

    def draw(self, surface):
        if self.oldRect != self.rect:
            if self.state == 0:
                screen.fill(BLACK,self.rect)
                surface.blit(self.image, self.rect)
                screen.fill(BLACK,self.oldRect)
            if self.state == 2:
                screen.fill(BLACK,self.rect)
                surface.blit(self.image, self.rect)
                screen.fill(BLACK,self.oldRect)
            if self.state == 1:
                screen.blit(waterImg,self.rect)
                surface.blit(self.image, self.rect)
                screen.fill(BLACK,self.oldRect)
            if self.state == 3:
                screen.blit(adamImg,self.rect)
                surface.blit(self.image, self.rect)
                screen.fill(BLACK,self.oldRect)
                

generateMap(playAreaX,playAreaY)
generateAcquifer(acquiferMin,acquiferMax)
drawMap()
p1 = Player()
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if p1.state != 1:
        p1.update()
        p1.draw(screen)
        pygame.display.update()
  