#Main Game Loop

import pygame, sys, os, random, Element
from pygame.locals import *

pygame.init()

# Comment from Aidan: Added jumpVel and unlockJumping:
# jumpVel is a static variable that stores initVel on the frame the ball collides with the ramp to ensure the velocity doesn't change while the ball is in flight (fixes jittering while flying)
# unlockJumping is a boolean that checks if we should be allowed to jump again (e.g. have we been on the platform before hitting the ramp again?)
# curPlatform denotes which platform we are currently standing on and is used to reenable gravity when we roll off the back or front side of it
initVel = 0
jumpVel = 0
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

screen = pygame.display.set_mode((1280,720))#, flags = pygame.FULLSCREEN) #CREATES THE FULLSCREEN

background = Element.Entity((640,360), 'space.png', (0,0), -1, (2275,1280))

tGO = pygame.image.load(os.getcwd() + "\\images\\Game_Over.png")
tGO = pygame.transform.scale(tGO, (1280,720))
rectGO = tGO.get_rect()

#tBall = pygame.image.load(os.getcwd() + '\\images\\Ring.png')
#tBall = pygame.transform.scale(tBall, (50,50))
#rectBall = tBall.get_rect()
#rectBall.x = 590
#rectBall.y = 450

planetOut = Element.Entity ((640,800),'Outer_Edge.png', (0,0), -1, (640,640))
planetIn = Element.Entity ((640,800),'Inner Circle.png', (0,0), 1, (550,550))
ball = Element.Entity ((590,450), 'ring.png', (0,0), 3, (50,50))
midPlatform = Element.Entity((640,900),'Mid B Lg.png',(0,-200), rotDir, (517,700))
tempOffset = 0

planetSprites = pygame.sprite.Group(planetOut,planetIn)  # sprites for the planet rings and planets
platformSprites = pygame.sprite.Group(midPlatform)
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
        index = index + 1 #Refactored levelGenerator
    




#TODOs for prototype:

#TODO: Implement winstate!
#TODO: Implement obstacles!

#The above TODOs should be completed, in the order they are listed, such that we can show off our prototype

#TODOs for bug fixing/polish:
#TODO: Fix passive movement after releasing mouse button
#TODO: Fullscreen mode/lock mouse to window

#This set of TODOs are more complicated and are not necessary to show off our game and should only be attempted after the first set of TODOs are completed

def redraw():    #Refactored all the bliting to one function
    #screen.blit(background.image, background.rect)
    #screen.blit(ball.image, ball.rect)
    index = 0
    backgroundSprite.draw(screen)
    ringSprite.draw(screen)
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


genLevel()

while True:
    #First, check if we can allow the player to jump again (e.g. are they no longer colliding with a ramp)

    canJump = False
    mouseMov = 0
    
    for i in ramps:
        if(ball.rect.colliderect(i) == 1):
            canJump = True
            break

    if(canJump == False):
        unlockJumping = True

    #Check if the player has rolled off the front or back of a platform, and if they have, fall (back) or jump (front)
    if(ball.rect.x + (ball.rect.width/2) < blocks[curPlatform].x):
        jump = True
        jumpVel = 0
    elif(ball.rect.x > blocks[curPlatform].x + blocks[curPlatform].width and jump == False):
        jump = True
        jumpVel = initVel

    if jump == True: # GRAVITY
        #First, check if we've hit a platform:
        canJump = False
        index = 0
        for i in blocks: #idk why I used ramps here, but it works regardless lmao
            if(ball.rect.colliderect(blocks[index]) == 1): ##if we've collided with a block, check if we hit the bottom
                if ball.rect.y < blocks[index].y - 50: #if we hit the top, we move the ball to its position and turn off gravity
                    ball.rect.y = blocks[index].y - 50
                    canJump = True
                    curPlatform = index
                    jump = False
                    deltaT = 1.0/30.0
                else:
                    jumpVel = 0 #if we haven't hit the top, we'll still remove our jump velocity and begin falling to the ground
                break
            index = index + 1

        if(canJump == True):
            unlockJumping = False
        else:
            unlockJumping = True #This probably isn't needed? unsure

        if(canJump == False):
            ball.rect.y -= jumpVel - g*deltaT*deltaT*0.5 #Fixed gravity, for some reason we scaled initial velocity by deltaT? kinematic equation is v0 - gt^2
            deltaT += 1.0/30.0 # /GRAVITY

    if(ball.rect.y > 720):
                #Death
        fadetoScreen(tGO, rectGO)
        break


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
                
                tempOffset = midPlatform.rect.x - mouse_x
                    

                # offsetCollisionRamp_x = rectCollisionBlock.x - mouse_x
                # offsetRamp_x = rectCollisionBlock.x + 504 - mouse_x
        
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
                #midPlatform.rect.x = mouse_x + tempOffset
                temp = pygame.mouse.get_rel()[0]
                print(temp)
                initVel = abs(temp)
                initVel = max(min(initVel,10),5)
                if temp > 0:
                    rotDir = 4
                elif temp < 0:
                    rotDir = -4
                midPlatform.updateDir(rotDir)
                platformSprites.update()


    for i in ramps:
            if(ball.rect.colliderect(i) == 1 and jump == False and unlockJumping == True):
                jump = True
                jumpVel = initVel
                unlockJumping = False

    planetSprites.update()
    ringSprite.update()
    
    redraw()

    
    pygame.display.update()
