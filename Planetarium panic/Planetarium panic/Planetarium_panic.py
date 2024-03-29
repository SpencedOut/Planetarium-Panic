import pygame, sys, os, random, Element
from pygame.locals import *

pygame.init()

# Comment from Aidan: Added jumpVel and unlockJumping:
# jumpVel is a static variable that stores initVel on the frame the ball collides with the ramp to ensure the velocity doesn't change while the ball is in flight (fixes jittering while flying)
# unlockJumping is a boolean that checks if we should be allowed to jump again (e.g. have we been on the platform before hitting the ramp again?)
# curPlatform denotes which platform we are currently standing on and is used to reenable gravity when we roll off the back or front side of it
start_music = pygame.mixer.Sound(os.getcwd()+"\\music\\bgm2.wav")
button_music = pygame.mixer.Sound(os.getcwd()+"\\music\\Lvl Trans.wav")
bg_music = pygame.mixer.Sound(os.getcwd()+"\\music\\ingame.wav") #load BG music
jump_music = pygame.mixer.Sound(os.getcwd()+"\\music\\jump.wav") #load jump sound
land_music = pygame.mixer.Sound(os.getcwd()+"\\music\\Metal Tink Land.wav") #load land Sound
fail_music = pygame.mixer.Sound(os.getcwd()+"\\music\\Fall Fail.wav")

screen = pygame.display.set_mode((1280,720))


#We can't use sprite groups anymore as they are not ordered. We must have the platforms in order of rotation

# levelGen(): Generates the first 3 platforms of a level and adds them to each list + sprite group
def levelGen():
    rotPlatforms.append(Element.Entity((640,1350),'Mid B Lg.png',(0,-500), rotDir, (776,1005)))
    #rotPlatforms.append(Element.Entity((640,1450), 'Top Lg.png', (0, -660), rotDir, (1024,1327)))
    rotPlatforms[0].initialRot(0)
    linPlatforms.append(Element.linearEntity(0,1,1))
    ramps.append(Element.linearRamp(linPlatforms[0],1))
    
    #TODO: Implement platforms of different height, using random to select which type to add

    rotPlatforms.append(Element.Entity((640,1350), 'Mid B Lg.png', (0, -500), rotDir, (776,1005)))

    #Change this to increase or decrease rotation variance
    rotPlatforms[1].initialRot(45 + random.randint(1, 60))

    linPlatforms.append(Element.linearEntity(rotPlatforms[1].angle, 1,1))
    ramps.append(Element.linearRamp(linPlatforms[1],1))


    rotPlatforms.append(Element.Entity((640,1350), 'Mid B Sm.png', (0, -500), rotDir, (350,1006)))
    #rotPlatforms.append(Element.Entity((640,1350), 'Mid B Lg.png', (0, -500), rotDir, (776,1005)))

    #Rotation variance
    rotPlatforms[2].initialRot(rotPlatforms[1].angle + random.randint(46,90))

    linPlatforms.append(Element.linearEntity(rotPlatforms[2].angle,1,2))
    ramps.append(Element.linearRamp(linPlatforms[2],2))

    rotPlatforms[0].add(allSprites)
    rotPlatforms[1].add(allSprites)
    rotPlatforms[2].add(allSprites)



    

#levelUpdate: Called when a platform rotates to a given angle (see below)
#Culls the first platform in the list and stops drawing it, then generates a new platform and adds it to the sprite group
def levelUpdate():
    allSprites.remove(rotPlatforms[0])
    rotPlatforms.pop(0)
    linPlatforms.pop(0)
    ramps.pop(0)

    pWidth = random.randint(1,2)
    pHeight = random.randint(1,2)

    if(pWidth == 1):
        if(pHeight == 1):
            rotPlatforms.append(Element.Entity((640,1350), 'Mid B Lg.png', (0, -500), rotDir, (776,1005)))
        else:
            rotPlatforms.append(Element.Entity((640,1450), 'Top Lg.png', (0, -660), rotDir, (1024,1327)))
    else:
        if(pHeight == 1):
            rotPlatforms.append(Element.Entity((640,1350), 'Mid B Sm.png', (0, -500), rotDir, (350,1006)))
        else:
            rotPlatforms.append(Element.Entity((640,1450), 'Top Sm.png', (0, -660), rotDir, (463,1327)))
    

    #Change this random number to increase or decrease rotation variance
    randomAngle =  random.randint(60,90)
    rotPlatforms[2].initialRot(rotPlatforms[1].angle + randomAngle)

    linPlatforms.append(Element.linearEntity(rotPlatforms[2].angle, pHeight,pWidth))
    ramps.append(Element.linearRamp(linPlatforms[2],pWidth))

    rotPlatforms[2].add(allSprites)


def redraw():    
    backgroundSprite.draw(screen)
    #screen.fill((0,0,0))
    ringSprite.draw(screen)

    allSprites.draw(screen)
    for rect in linPlatforms:
        rect.move(velocity)
        #pygame.draw.rect(screen, (255, 255, 255), rect.rect, 1)

    for ramp in ramps:
        ramp.move(velocity)
        #pygame.draw.rect(screen, (255, 255, 255), ramp.rect, 1)

    scoreFont = pygame.font.Font('freesansbold.ttf', 52) 
    textSurf = scoreFont.render(('Distance Travelled: ' + str(distTravelled)), False, (255, 255, 255))
    textRect = textSurf.get_rect()
    textRect.x = 0
    textRect.y = 0
    screen.blit(textSurf, textRect)

    infoFont = pygame.font.Font('freesansbold.ttf',48)
    infoSurf = infoFont.render('Large Jump',False,(255,255,255))
    infoRect = infoSurf.get_rect()
    infoRect.x = 950
    infoRect.y = 0
    if rotPlatforms[2].angle - rotPlatforms[1].angle > 85:
        screen.blit(infoSurf,infoRect)
    #box1.move() #moving ramp
    #pygame.draw.rect(screen,(255,255,255), box1.rect, 1) #drawing debug rectan

def fadetoScreen(prevScene,prevRect,scene,rectScene):
    fade = pygame.Surface((1280,720))
    fade.fill((0,0,0))
    alpha = 0
    while alpha < 300 :
        fade.set_alpha(alpha)
        screen.blit(prevScene,prevRect)
        screen.blit(fade, (0,0))
        alpha+=10
        pygame.display.update()
    alpha = 0
    while alpha < 300 :
        scene.set_alpha(alpha)   
        screen.blit(scene,rectScene)
        alpha+=10
        pygame.display.update()
    pygame.time.delay(100)



def fadetoScreenMain(scene,rectScene):
    fade = pygame.Surface((1280,720))
    fade.fill((0,0,0))
    alpha = 0
    while alpha < 300 :
        fade.set_alpha(alpha)
        redraw()
        screen.blit(fade, (0,0))
        alpha+=10
        pygame.display.update()
    alpha = 0
    while alpha < 300 :
        scene.set_alpha(alpha)   
        screen.blit(scene,rectScene)
        alpha+=10
        pygame.display.update()
    scoreFont = pygame.font.Font('freesansbold.ttf', 50)
    textSurf = scoreFont.render(('Time on Platform: ' + str(score)), False, (255, 255, 255))
    textRect = textSurf.get_rect()
    textRect.x = 400
    textRect.y = 400
    screen.blit(textSurf, textRect)

    infoFont = pygame.font.Font('freesansbold.ttf',50)
    textSurf2 = infoFont.render(('Distance Travelled: ' + str(distTravelled)), False, (255, 255, 255))
    textRect2 = textSurf.get_rect()
    textRect2.x = 400
    textRect2.y = 500
    screen.blit(textSurf2, textRect2)
    pygame.display.update()
    pygame.time.delay(100)
#def genPlatform():
#backgroundSprite.draw(screen)
#Game code starts here
while True:
    velocity = 2.5 
    initVel= 2.5
    g = 98
    getTicksLastFrame = 0
    jump = False
    unlockJumping = False
    deltaT= 0.0
    curPlatform = 0
    speed = 0
    rotDir = -1 #speed and rotation of the platforms
    temp = 0
    i = 0
    ringBasePos = 0
    jumpVel = 0
    score = 0  # Used to store the score of the player
    isPressed = False
    distTravelled = 0
    background = Element.Entity((640,360), 'space.png', (0,0), -1, (1280,720))

    startButton = pygame.image.load(os.getcwd() + "\\images\\Highlight.png")
    rectButton = startButton.get_rect()
    rectButton.x = 780
    rectButton.y = 460

    tStart = pygame.image.load(os.getcwd() + "\\images\\Main menu.png")
    tStart = pygame.transform.scale(tStart,(1280,720))
    rectStart = tStart.get_rect()

    tArrow = pygame.image.load(os.getcwd() + "\\images\\Arrow Up.png")
    tArrow = pygame.transform.scale(tArrow, (100, 100))
    rectArrow = tArrow.get_rect()

    tControl = pygame.image.load(os.getcwd() + "\\images\\Controls.png")
    tControl = pygame.transform.scale(tControl,(1280,720))
    rectControl = tControl.get_rect()

    tGO = pygame.image.load(os.getcwd() + "\\images\\Game_Over.png")
    tGO = pygame.transform.scale(tGO, (1280,720))
    rectGO = tGO.get_rect()

    planetOut = Element.Entity ((640,800),'Outer_Edge.png', (0,0), -3, (640,640))
    planetIn = Element.Entity ((640,800),'Inner Circle.png', (0,0), 3, (550,550))
    ball = Element.Entity ((640,320), 'ring.png', (0,0), 10, (50,50))
    allSprites = pygame.sprite.Group(planetOut, planetIn)
    planetSprites = pygame.sprite.Group(planetOut,planetIn)  # sprites for the planet rings and planets
    backgroundSprite = pygame.sprite.Group(background)
    ringSprite = pygame.sprite.Group(ball)

    rotPlatforms = []
    linPlatforms = []
    ramps = []

    start_music.play(-1)

    while(True):
    
        screen.blit(tStart,rectStart)
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                isPressed = True
        mousePos = pygame.mouse.get_pos()
        if(((mousePos[0]>= rectButton.x) and (mousePos[0]<= rectButton.x + rectButton.width))
               and ((mousePos[1]>= rectButton.y) and (mousePos[1]<= rectButton.y + rectButton.height))):
            screen.blit(startButton,rectButton)
            if isPressed:
                button_music.play(0,0,0)
                start_music.stop()
                break;
        
        #pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(780,460,343,119), 1)
        pygame.display.update()

    fadetoScreen(tStart,rectStart,tControl,rectControl)
    bg_music.play(-1) #play BG music
    pygame.time.delay(5000)
    levelGen()

    while True: #Main game loop
        #First, check if we can allow the player to jump again (e.g. are they no longer colliding with a ramp)

        canJump = False

        #Change this angle to change where platforms are getting culled- It's so high now just to demonstrate that platforms are in fact culled
        if(rotPlatforms[0].angle < -90):
            levelUpdate()

        #if(ball.rect.y > 720):
        #            #Death
        #    fadetoScreen(tGO, rectGO)
        #    break

        #checkForCollision()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            velocity = initVel + 2.5
            distTravelled += initVel + 2.5

        elif pressed[pygame.K_d]:
            velocity = initVel - 2.0
            distTravelled += initVel - 2.0
        else:
            velocity = initVel
            distTravelled += initVel

        #Gravity workings

        collisionCheck = False
        for rect in linPlatforms:
            if ball.rect.colliderect(rect.rect) == 1:
                score += 1
                collisionCheck = True
                break

        if(collisionCheck == False):
            unlockJumping = True


        if(ball.rect.x > linPlatforms[curPlatform].rect.x + linPlatforms[curPlatform].rect.width and jump == False):
            jump = True
            if velocity > 2:
                jumpVel = velocity + 12
            else:
                jumpVel = 25

        if jump == True:
            collisionCheck = False;
            index = 0
            for ramp in ramps:
                if(ball.rect.colliderect(linPlatforms[index].rect) == 1):
                    if ball.rect.y < linPlatforms[index].rect.y - 30 or jumpVel - (g*deltaT*deltaT*0.5) < 0:
                        i=0
                        ball.pos.y = ramps[index].y + 25
                        collisionCheck = True
                        #curPlatform = index
                        jump = False
                        deltaT = 1.0/60.0
                        land_music.play(0,0,0)
                    jumpVel = 0
                    break
                index+=1

            if(collisionCheck == True):
                unlockJumping = False
            else:
                unlockJumping = True

            if(collisionCheck == False):
                if(jumpVel == 25):
                    ball.pos.y -= jumpVel - (g*deltaT*deltaT*0.5)
                    deltaT += 3.0/60.0
                else:
                    ball.pos.y -= jumpVel - g*deltaT*deltaT*0.5
                    deltaT += 5.0/60.0

            if(ball.rect.y > 620):
                bg_music.stop()
                fail_music.play(0,0,0)
                fadetoScreenMain(tGO, rectGO)
                pygame.time.delay(3000)
                break

        #This is the new platform update method.
        for platform in rotPlatforms:
            platform.updateDir(-velocity)
            platform.update()


        planetSprites.update()
        ringSprite.update()
        redraw()
        pygame.display.update()
