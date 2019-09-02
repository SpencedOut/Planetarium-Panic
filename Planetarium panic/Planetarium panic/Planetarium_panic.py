import pygame, sys, os, random, Element
from pygame.locals import *

pygame.init()

# Comment from Aidan: Added jumpVel and unlockJumping:
# jumpVel is a static variable that stores initVel on the frame the ball collides with the ramp to ensure the velocity doesn't change while the ball is in flight (fixes jittering while flying)
# unlockJumping is a boolean that checks if we should be allowed to jump again (e.g. have we been on the platform before hitting the ramp again?)
# curPlatform denotes which platform we are currently standing on and is used to reenable gravity when we roll off the back or front side of it
velocity = 2.5 
initVel= 2.5
g = 10
getTicksLastFrame = 0
jump = False
unlockJumping = False
deltaT= 1.0/30.0
curPlatform = 0
speed = 0
rotDir = -1 #speed and rotation of the platforms
temp = 0
i = 1
ringBasePos = 0
jumpVel = 0
score = 0  # Used to store the score of the player

bg_music = pygame.mixer.Sound(os.getcwd()+"\\music\\ingame.wav") #load BG music
jump_music = pygame.mixer.Sound(os.getcwd()+"\\music\\jump.wav") #load jump sound
land_music = pygame.mixer.Sound(os.getcwd()+"\\music\\Metal Tink Land.wav") #load land Sound

bg_music.play(-1) #play BG music

screen = pygame.display.set_mode((1280,720))

background = Element.Entity((640,360), 'space.png', (0,0), -1, (1280,720))

tGO = pygame.image.load(os.getcwd() + "\\images\\Game_Over.png")
tGO = pygame.transform.scale(tGO, (1280,720))
rectGO = tGO.get_rect()

planetOut = Element.Entity ((640,800),'Outer_Edge.png', (0,0), -3, (640,640))
planetIn = Element.Entity ((640,800),'Inner Circle.png', (0,0), 3, (550,550))
ball = Element.Entity ((640,320), 'ring.png', (0,0), 10, (50,50))
#midPlatform = Element.Entity((640,900),'Mid B Lg.png',(0,-200), rotDir, (500,700))
#midPlatform1 = Element.Entity((640,900),'Mid B Lg.png',(0,-200), rotDir, (500,700))
#midPlatform1.initialRot(90)
#midPlatform2 = Element.Entity((640,900),'Mid B Lg.png',(0,-200), rotDir, (500,700))
#midPlatform2.initialRot(180)
#platform1 = Element.Entity((640,1350),'Mid B Lg.png',(0,-500), rotDir, (776,1005))
#platform1.initialRot(0)
#platform2 = Element.Entity((640,1350),'Mid B Lg.png',(0,-500), rotDir, (776,1005))
#platform2.initialRot(90)
#platform3 = Element.Entity((640,1350),'mid b lg.png',(0,-600), rotDir, (776,1005))
#platform3.initialRot(180)
#platform4 = Element.Entity((640,1350),'mid b lg.png',(0,-500), rotDir, (776,1005))
#platform4.initialRot(270)

#Adding Ramp
#box1 = Element.linearEntity(0,1)
#box2 = Element.linearEntity(90,1)
#box3 = Element.linearEntity(180,1)
#box4 = Element.linearEntity(270,1)
#ramp1 = Element.linearRamp(box1)
#ramp2 = Element.linearRamp(box2)
#ramp3 = Element.linearRamp(box3)
#ramp4 = Element.linearRamp(box4)
#ramp1 = 


#ramp = Element.Entity((840,490),'Ramp.png', (0,0), rotDir, (50,50))
#tempOffset = 0



#We can't use sprite groups anymore as they are not ordered. We must have the platforms in order of rotation
allSprites = pygame.sprite.Group(planetOut, planetIn)
planetSprites = pygame.sprite.Group(planetOut,planetIn)  # sprites for the planet rings and planets
#platformSprites = pygame.sprite.Group()
backgroundSprite = pygame.sprite.Group(background)
ringSprite = pygame.sprite.Group(ball)
#horRects = [box1, box2, box3, box4]
#horRamps = [ramp1, ramp2, ramp3, ramp4]

rotPlatforms = []
linPlatforms = []
ramps = []

# levelGen(): Generates the first 3 platforms of a level and adds them to each list + sprite group
def levelGen():
    rotPlatforms.append(Element.Entity((640,1350),'Mid B Lg.png',(0,-500), rotDir, (776,1005)))
    rotPlatforms[0].initialRot(0)
    linPlatforms.append(Element.linearEntity(0,1))
    ramps.append(Element.linearRamp(linPlatforms[0]))
    
    #TODO: Implement platforms of different height, using random to select which type to add

    rotPlatforms.append(Element.Entity((640,1350), 'Mid B Lg.png', (0, -500), rotDir, (776,1005)))

    #Change this to increase or decrease rotation variance
    rotPlatforms[1].initialRot(45 + random.randint(1, 60))

    linPlatforms.append(Element.linearEntity(rotPlatforms[1].angle, 1))
    ramps.append(Element.linearRamp(linPlatforms[1]))

    rotPlatforms.append(Element.Entity((640,1350), 'Mid B Lg.png', (0, -500), rotDir, (776,1005)))

    #Rotation variance
    rotPlatforms[2].initialRot(rotPlatforms[1].angle + random.randint(46,90))

    linPlatforms.append(Element.linearEntity(rotPlatforms[2].angle, 1))
    ramps.append(Element.linearRamp(linPlatforms[2]))

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

    rotPlatforms.append(Element.Entity((640,1350), 'Mid B Lg.png', (0, -500), rotDir, (776,1005)))

    #Change this random number to increase or decrease rotation variance
    rotPlatforms[2].initialRot(rotPlatforms[1].angle + random.randint(60,90))

    linPlatforms.append(Element.linearEntity(rotPlatforms[2].angle, 1))
    ramps.append(Element.linearRamp(linPlatforms[2]))

    rotPlatforms[2].add(allSprites)


#rampSprites = pygame.sprite.Group(ramp)

#TODOs for prototype:

#TODO: Implement winstate!
#TODO: Implement obstacles!

#The above TODOs should be completed, in the order they are listed, such that we can show off our prototype

#TODOs for bug fixing/polish:
#TODO: Fix passive movement after releasing mouse button
#TODO: Fullscreen mode/lock mouse to window

#This set of TODOs are more complicated and are not necessary to show off our game and should only be attempted after the first set of TODOs are completed

def jumping():
    global jump
    jump = False

#def checkForCollision():
#    global unlockJumping
#    global jump
#    #Please check to make sure this works, but it should work right out of the box
#    for rect in linPlatforms:
#        if ball.rect.colliderect(rect.rect) == 1:
#            if unlockJumping == False: # and jump == False: # if the ball lands and is not in the ramp collision area
#                global score
#                score += 1
#                print("Collision with the horizontal rect")
#                unlockJumping = True
#            break

#    for ramp in ramps:
#        if ball.rect.colliderect(ramp.rect) == 1 :
#            if unlockJumping == True:# and jump == False:
#                print("Collision with horizontal ramp")
#                jump = True
#                unlockJumping = False
#            break

    #hit = pygame.sprite.spritecollide(ball, platformSprites, False, pygame.sprite.collide_mask(ball, platformSprites[]))
    #if hit != None:
    #    initJump = 1
    #    jumpVel = 0
    #    jump = False
    #    ball.updatePos(jumpVel,jump,ringBasePos)
  
    #else:
    #    if initJump == 1:
    #        jump = True
    #        jumpVel = initVel
    #        initJump = 0
    #    ball.updatePos(jumpVel,jump,ringBasePos)

def activateLoop():
    return

def redraw():    
    backgroundSprite.draw(screen)
    #screen.fill((0,0,0))
    ringSprite.draw(screen)

    allSprites.draw(screen)
    for rect in linPlatforms:
        rect.move(velocity)
        pygame.draw.rect(screen, (255, 255, 255), rect.rect, 1)

    for ramp in ramps:
        ramp.move(velocity)
        pygame.draw.rect(screen, (255, 255, 255), ramp.rect, 1)

    scoreFont = pygame.font.Font('freesansbold.ttf', 75) 
    textSurf = scoreFont.render(('Score = ' + str(score)), False, (255, 255, 255))
    textRect = textSurf.get_rect()
    textRect.x = 0
    textRect.y = 0
    screen.blit(textSurf, textRect)
    #box1.move() #moving ramp
    #pygame.draw.rect(screen,(255,255,255), box1.rect, 1) #drawing debug rectan

def fadetoScreen(scene,rectScene):
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
    pygame.time.delay(100)

#def genPlatform():
#backgroundSprite.draw(screen)
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

    elif pressed[pygame.K_d]:
        velocity = initVel - 2.0
    else:
        velocity = initVel

    #Gravity workings

    collisionCheck = False
    for rect in linPlatforms:
        if ball.rect.colliderect(rect.rect) == 1:
            collisionCheck = True
            break

    if(collisionCheck == False):
        unlockJumping = True

    #for ramp in ramps:
    #    if(ball.rect.colliderect(ramp.rect)==1):
    #        jump = True
    #        jumpVel = velocity + 2
    #        break

    if(ball.rect.x > linPlatforms[curPlatform].rect.x + linPlatforms[curPlatform].rect.width and jump == False):
        jump = True
        jumpVel = velocity + 2
        

    if jump == True:
        collisionCheck = False;
        index = 0
        for ramp in ramps:
            if(ball.rect.colliderect(linPlatforms[index].rect) == 1):
                if ball.rect.y < linPlatforms[index].rect.y - 30:
                    ball.pos.y = ramps[index].y + 25
                    collisionCheck = True
                    curPlatform = index
                    jump = False
                    deltaT = 1.0/30.0
                    land_music.play(0,0,0)
                jumpVel = 0
                break
            index+=1

        if(collisionCheck == True):
            unlockJumping = False
        else:
            unlockJumping = True

        if(collisionCheck == False):
            ball.pos.y -= jumpVel - g*deltaT*deltaT*0.5
            deltaT += 1.0/30.0

        if(ball.rect.y > 620):
            #Death
            fadetoScreen(tGO, rectGO)
            break

    #This is the new platform update method.
    for platform in rotPlatforms:
        platform.updateDir(-velocity)
        platform.update()

    #platform1.updateDir(-velocity)
    #platform2.updateDir(-velocity)
    #platform3.updateDir(-velocity)
    #platform4.updateDir(-velocity)

    #screen.blit(tRamp, rectRamp)    
    #pygame.draw.rect(screen, (255,255,255), rectRamp, 2)


    #for platform in platformSprites:
        #pygame.draw.rect(screen,(255,255,255), platform.rect, 3)
    
    #platformSprites.update()

    planetSprites.update()
    ringSprite.update()
    redraw()
    pygame.display.update()
