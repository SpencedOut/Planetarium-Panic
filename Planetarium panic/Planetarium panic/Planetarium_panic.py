#Main Game Loop

import pygame, sys, os, random, Element
from pygame.locals import *

pygame.init()

# Comment from Aidan: Added jumpVel and unlockJumping:
# jumpVel is a static variable that stores initVel on the frame the ball collides with the ramp to ensure the velocity doesn't change while the ball is in flight (fixes jittering while flying)
# unlockJumping is a boolean that checks if we should be allowed to jump again (e.g. have we been on the platform before hitting the ramp again?)
# curPlatform denotes which platform we are currently standing on and is used to reenable gravity when we roll off the back or front side of it
initVel = 0
jumpVel = 10
g = 9.8
getTicksLastFrame = 0
jump = False
unlockJumping = True
deltaT= 1.0/30.0
curPlatform = 0
m_drag= False
speed = 0
rotDir = -3
temp = 0
tempi = 0
ringBasePos = 0

bg_music = pygame.mixer.Sound(os.getcwd()+"\\music\\ingame.wav") #load BG music
jump_music = pygame.mixer.Sound(os.getcwd()+"\\music\\jump.wav") #load jump sound
land_music = pygame.mixer.Sound(os.getcwd()+"\\music\\Metal Tink Land.wav") #load land Sound

bg_music.play(-1) #play BG music

screen = pygame.display.set_mode((1280,720))#, flags = pygame.FULLSCREEN) #CREATES THE FULLSCREEN

background = Element.Entity((640,360), 'space.png', (0,0), -1, (2275,1280))

tGO = pygame.image.load(os.getcwd() + "\\images\\Game_Over.png")
tGO = pygame.transform.scale(tGO, (1280,720))
rectGO = tGO.get_rect()



planetOut = Element.Entity ((640,800),'Outer_Edge.png', (0,0), -1, (640,640))
planetIn = Element.Entity ((640,800),'Inner Circle.png', (0,0), 1, (550,550))
ball = Element.Entity ((590,325), 'ring.png', (0,0), 3, (50,50))
midPlatform = Element.Entity((640,900),'Mid B Lg.png',(0,-200), rotDir, (517,700))
midPlatform1 = Element.Entity((640,900),'Mid B Lg.png',(0,-200), rotDir, (500,700))
midPlatform1.initialRot(90)
midPlatform2 = Element.Entity((640,900),'Mid B Lg.png',(0,-200), rotDir, (500,700))
midPlatform2.initialRot(180)
highPlatform = Element.Entity((640,900),'Top Sm.png',(0,-250), rotDir, (300,900))
highPlatform.initialRot(270)

ringBasePos = ball.pos.y


planetSprites = pygame.sprite.Group(planetOut,planetIn)  # sprites for the planet rings and planets
platformSprites = pygame.sprite.Group(midPlatform, midPlatform1, midPlatform2, highPlatform)
backgroundSprite = pygame.sprite.Group(background)
ringSprite = pygame.sprite.Group(ball)

#Lists of objects that are used for blitting and updating positions later on. DO NOT ALTER.
blocks = []
ramps = []
offsets = []
blockSprites = []
rampSprites = []


#Level generation code for randomly generating test levels. Currently generates levels with 20 platforms, but could go up to 50 with no issues.
#Feel free to modify this to better fit the prototype.
#DO NOT MODIFY THE INDEX OR INITIAL VALUES, THESE MUST REMAIN CONSTANT

#def genPad():


def genLevel():
    index = 0
    initialX = 338
    initialY = 700

    while index < 50:
        if index == 0:
            tRamp = pygame.image.load(os.getcwd()+"\\images\\Ramp.png")
            tRamp = pygame.transform.scale(tRamp,(100,100))
            rectRamp = tRamp.get_rect()
            rectRamp.x = 740
            rectRamp.y = 400

            ramps.append(rectRamp)
            rampSprites.append(tRamp)

            tCollisionBlock = pygame.image.load(os.getcwd()+"\\images\\collisionBlock.png")
            tCollisionBlock = pygame.transform.scale(tCollisionBlock,(400,40))
            rectCollisionBlock = tCollisionBlock.get_rect()
            widthCollisionBlock = rectCollisionBlock.width
            heightCollisionBlock = rectCollisionBlock.height

            rectCollisionBlock.y = 500
            rectCollisionBlock.x = 440

            blocks.append(rectCollisionBlock)
            blockSprites.append(tCollisionBlock)
            offsets.append(0)
        else:
            tRamp = pygame.image.load(os.getcwd()+"\\images\\Ramp.png")
            tRamp = pygame.transform.scale(tRamp,(100,100))
            rectRamp = tRamp.get_rect()

            tCollisionBlock = pygame.image.load(os.getcwd()+"\\images\\collisionBlock.png")
            tCollisionBlock = pygame.transform.scale(tCollisionBlock,(400,40))
            rectCollisionBlock = tCollisionBlock.get_rect()
            widthCollisionBlock = rectCollisionBlock.width
            heightCollisionBlock = rectCollisionBlock.height

                #Determine the position of the new platform:
            rectCollisionBlock.y = random.randint(300, 700)
            rectCollisionBlock.x = initialX + (1200 * index) + random.randint(-200, 400)

            rectRamp.y = rectCollisionBlock.y - 100
            rectRamp.x = rectCollisionBlock.x + 300

            blocks.append(rectCollisionBlock)
            blockSprites.append(tCollisionBlock)
            offsets.append(0)
            ramps.append(rectRamp)
            rampSprites.append(tRamp)
        index = index + 1 #Refactored levelGenerator(update: not using right now)
    




#TODOs for prototype:

#TODO: Implement winstate!
#TODO: Implement obstacles!

#The above TODOs should be completed, in the order they are listed, such that we can show off our prototype

#TODOs for bug fixing/polish:
#TODO: Fix passive movement after releasing mouse button
#TODO: Fullscreen mode/lock mouse to window

#This set of TODOs are more complicated and are not necessary to show off our game and should only be attempted after the first set of TODOs are completed
def ActivateJump():
    return

def checkForCollision():
    initJump =1
    hit = pygame.sprite.spritecollide(ball, platformSprites, False, pygame.sprite.collide_mask)
    if hit:
        initJump = 1
        jumpVel = 0
        jump = False
        ball.updatePos(jumpVel,jump,ringBasePos)
    else:
        jump = True
        if initJump == 1:
            jumpVel = initVel
            initJump-=1
        ball.updatePos(jumpVel,jump,ringBasePos)

def redraw():    #Refactored all the bliting to one function
    ringSprite.update()
    index = 0
    backgroundSprite.draw(screen)
    #ringSprite.draw(screen)
    screen.blit(ball.image,ball.rect)
    planetSprites.draw(screen)
    #platformSprites.draw(screen)
    screen.blit(midPlatform.image, midPlatform.rect)
    for i in blocks: #blit all sprites to the screen
        screen.blit(rampSprites[index],(ramps[index].x, ramps[index].y))
        screen.blit(blockSprites[index],(blocks[index].x, blocks[index].y))
        index = index + 1

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


#genLevel()

while True:
    #First, check if we can allow the player to jump again (e.g. are they no longer colliding with a ramp)
    

    if(ball.rect.y > 720):
                #Death
        fadetoScreen(tGO, rectGO)
        break
    
    checkForCollision()

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                m_drag=True
                mouse_x, mouse_y = event.pos
                index = 0
                for i in blocks: #Set all block offsets on click
                    offsets[index] = i.x - mouse_x
                    index = index + 1
                
               
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:    
                m_drag = False
                speed = abs(pygame.mouse.get_rel()[0])
                speed = speed/5

        elif event.type == pygame.MOUSEMOTION:
            if m_drag:
                mouse_x, mouse_y = event.pos
                index = 0
                for i in blocks: #Move all blocks and ramps in unison.
                    i.x = mouse_x + offsets[index]
                    ramps[index].x = i.x + 300
                    index = index + 1
                temp = pygame.mouse.get_rel()[0]
                initVel = abs(temp)
                initVel = max(min(initVel,60),5)
                if temp > 0:
                    rotDir = initVel
                elif temp < 0:
                    rotDir = -initVel
                midPlatform.updateDir(rotDir)
                midPlatform1.updateDir(rotDir)
                midPlatform2.updateDir(rotDir)
                highPlatform.updateDir(rotDir)
                platformSprites.update()


    if tempi == 0:                                          #Temporary thing to make sure platform is in place
        platformSprites.update()
        tempi = 1

    planetSprites.update()
    
    
    redraw()

    
    pygame.display.update()
