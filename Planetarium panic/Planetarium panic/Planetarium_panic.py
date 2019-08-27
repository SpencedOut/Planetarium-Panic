

#Main Game Loop


import pygame,sys,os,random
from pygame.locals import *

#loader planetLoader ("Outer Edge.png")

#loaderObjects ("sdfsdf")





screen = pygame.display.set_mode((1280,720))#, flags = pygame.FULLSCREEN) #CREATES THE FULLSCREEN

tBack = pygame.image.load(os.getcwd()+"\\images\\Space.png")
rectBack = tBack.get_rect()



#tOuterRing = pygame.image.load(os.getcwd()+"\\images\\Outer Edge.png") #LOADS THE OUTER EDGE IMAGE
#tOuterRing = pygame.transform.scale(tOuterRing, (800,800)) #SCALES THE OUTER EDGE IMAGE
#rectOuterRing = tOuterRing.get_rect()
#rectOuterRing = rectOuterRing.move(560,680) #MOVES THE OUTER EDGE IMAGE AND SURFACE TO CENTER BOTTOM

#tInnerRing = pygame.image.load(os.getcwd()+"\\images\\Inner Circle.png") # INNER CIRCLE CODE
#tInnerRing = pygame.transform.scale(tInnerRing, (720,720))
#rectInnerRing = tInnerRing.get_rect()
#rectInnerRing = rectInnerRing.move(600,720)


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

frame = 0

tRingSeq = pygame.image.load(os.getcwd()+"\\images\\RingSpin.png")

rects = [(0,0,128,128), (128,0,128,128), (256,0,128,128), (0,128,128,128), (128,128,128,128), (256,128,128,128)]

def image_at(rectangle, colorkey = None):
    "Loads image from x,y,x+offset,y+offset"
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size).convert()
    image.blit(tRingSeq, (0, 0), rect)
    #if colorkey is not None:
    #    if colorkey is -1:
    #        colorkey = image.get_at((0,0))
    #    image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image 

def images_at(rects, colorkey = None):
    "Loads multiple images, supply a list of coordinates" 
    return [image_at(rect, colorkey) for rect in rects]

imageSequence = []
imageSequence = images_at(rects)


tBall = imageSequence[0]
rectBall = tBall.get_rect()
rectBall.x = 590
rectBall.y = 500

tRamp = pygame.image.load(os.getcwd()+"\\images\\Ramp.png")
tRamp = pygame.transform.scale(tRamp,(100,100))
rectRamp = tRamp.get_rect()
rectRamp.x = 540 + 302
rectRamp.y = 500

#tCollisionBlock = pygame.image.load(os.getcwd()+"\\images\\collisionBlock.png")
#rectCollisionBlock = tCollisionBlock.get_rect()
#widthCollisionBlock = rectCollisionBlock.width
#heightCollisionBlock = rectCollisionBlock.height
#print (widthCollisionBlock)

#rectCollisionBlock.y = 600
#rectCollisionBlock.x = 640 - (widthCollisionBlock/2)

#tCollisionBlock2 = pygame.image.load(os.getcwd()+"\\images\\collisionBlock.png")
#rectCollisionBlock2 = tCollisionBlock2.get_rect()
#widthCollisionBlock2 = rectCollisionBlock2.width
#heightCollisionBlock2 = rectCollisionBlock2.height

#rectCollisionBlock2.y = 400
#rectCollisionBlock2.x = 1500 - (widthCollisionBlock2/2)

#tRamp2 = pygame.image.load(os.getcwd()+"\\images\\Ramp.png")
#tRamp2 = pygame.transform.scale(tRamp2,(100,100))
#rectRamp2 = tRamp2.get_rect()
#rectRamp2.x = 1400 + 302
#rectRamp2.y = 300

#blocks = [rectCollisionBlock, rectCollisionBlock2]
#rampSprites = [tRamp, tRamp2]
#ramps = [rectRamp, rectRamp2]
#blockSprites = [tCollisionBlock, tCollisionBlock2]
#offsets = [0, 0]

#Lists of objects that are used for blitting and updating positions later on. DO NOT ALTER.
blocks = []
ramps = []
offsets = []
blockSprites = []
rampSprites = []

#Level generation code for randomly generating test levels. Currently generates levels with 20 platforms, but could go up to 50 with no issues.
#Feel free to modify this to better fit the prototype.
#DO NOT MODIFY THE INDEX OR INITIAL VALUES, THESE MUST REMAIN CONSTANT
index = 0
initialX = 338.0
initialY = 600
while index < 50:
    if index == 0:
        tRamp = pygame.image.load(os.getcwd()+"\\images\\Ramp.png")
        tRamp = pygame.transform.scale(tRamp,(100,100))
        rectRamp = tRamp.get_rect()
        rectRamp.x = 540.0 + 302.0
        rectRamp.y = 500

        ramps.append(rectRamp)
        rampSprites.append(tRamp)

        tCollisionBlock = pygame.image.load(os.getcwd()+"\\images\\collisionBlock.png")
        rectCollisionBlock = tCollisionBlock.get_rect()
        widthCollisionBlock = rectCollisionBlock.width
        heightCollisionBlock = rectCollisionBlock.height

        rectCollisionBlock.y = 600
        rectCollisionBlock.x = 640.0 - (widthCollisionBlock/2)

        blocks.append(rectCollisionBlock)
        blockSprites.append(tCollisionBlock)
        offsets.append(0)
    else:
        tRamp = pygame.image.load(os.getcwd()+"\\images\\Ramp.png")
        tRamp = pygame.transform.scale(tRamp,(100,100))
        rectRamp = tRamp.get_rect()
       

        tCollisionBlock = pygame.image.load(os.getcwd()+"\\images\\collisionBlock.png")
        rectCollisionBlock = tCollisionBlock.get_rect()
        widthCollisionBlock = rectCollisionBlock.width
        heightCollisionBlock = rectCollisionBlock.height

        #Determine the position of the new platform:
        rectCollisionBlock.y = random.randint(200, 600)
        rectCollisionBlock.x = initialX + (1200.0 * index) + random.randint(-200, 400)

        rectRamp.y = rectCollisionBlock.y - 100
        rectRamp.x = rectCollisionBlock.x + 402.0

        blocks.append(rectCollisionBlock)
        blockSprites.append(tCollisionBlock)
        offsets.append(0)
        ramps.append(rectRamp)
        rampSprites.append(tRamp)
    index = index + 1



#rampSprites = pygame.sprite.Group()
#rampSprites.add(rectRamp)

                              
#outerRing = screen.blit(tOuterRing, rectOuterRing) #JOINING THE CIRCLE TEXTURES WITH THEIR RECT SURFACES
#innerRing = screen.blit(tInnerRing, rectInnerRing)

#planet = screen.blit(innerRing, outerRing)

m_drag= False
speed = 0


def frameChange(frm):
    
    if frm == 5:
        frm=0
    else:
        frm += 1
    tBall = imageSequence[frm]
    return frm
    
#TODOs for prototype:
#TODO: Replace the ball with the Ring
#TODO: Implement dying!
#TODO: Implement winstate!
#TODO: Implement obstacles!

#The above TODOs should be completed, in the order they are listed, such that we can show off our prototype
#TODOs for bug fixing/polish:
#TODO: Fix passive movement after releasing mouse button
#TODO: Fullscreen mode/lock mouse to window

#This set of TODOs are more complicated and are not necessary to show off our game and should only be attempted after the first set of TODOs are completed

while True:

    frame = frameChange(frame)

    #First, check if we can allow the player to jump again (e.g. are they no longer colliding with a ramp)
    collisionCheck = False
    for i in ramps:
        if(rectBall.colliderect(i) == 1):
            collisionCheck = True
            break

    if(collisionCheck == False):
        unlockJumping = True

    #Check if the player has rolled off the front or back of a platform, and if they have, fall (back) or jump (front)
    if(rectBall.x + (rectBall.width/2) < blocks[curPlatform].x):
        jump = True
        jumpVel = 0
    elif(rectBall.x > blocks[curPlatform].x + blocks[curPlatform].width and jump == False):
        jump = True
        jumpVel = initVel

    #if speed!=0:
         # MOVE ALL OTHER SPRITES TO THE LEFT
        #rectCollisionBlock.x = rectCollisionBlock.x - speed
        #rectRamp.x = rectCollisionBlock.x + 504
       # index = 0
        #for i in blocks:
          #  i.x = i.x - speed
        #    ramps[index].x = i.x + 504
       #     index = index + 1
       # speed /= 1.5

    #if(rectBall.x + (rectBall.width/2) < rectCollisionBlock.x and rectBall.y >= 500):
       # print("Killed!")


    if jump == True: # GRAVITY
        #First, check if we've hit a platform:
        collisionCheck = False
        index = 0
        for i in ramps: #idk why I used ramps here, but it works regardless lmao
            if(rectBall.colliderect(blocks[index]) == 1): ##if we've collided with a block, check if we hit the bottom
                if rectBall.y < blocks[index].y - 50: #if we hit the top, we move the ball to its position and turn off gravity
                    rectBall.y = blocks[index].y - 128
                    collisionCheck = True
                    curPlatform = index
                    jump = False
                    deltaT = 1.0/30.0
                jumpVel = 0 #if we haven't hit the top, we'll still remove our jump velocity and begin falling to the ground
                break
            index = index + 1

        if(collisionCheck == True):
            unlockJumping = False
        else:
            unlockJumping = True #This probably isn't needed? unsure

        if(collisionCheck == False):
            rectBall.y -= jumpVel - g*deltaT*deltaT*0.5 #Fixed gravity, for some reason we scaled initial velocity by deltaT? kinematic equation is v0 - gt^2
            deltaT += 1.0/30.0 # /GRAVITY

        if(rectBall.y > 620):
            print("Killed!") #IMPLEMENT DYING HERE

        #if rectBall.y > 500:
           # rectBall.y = 500
           # deltaT = 1.0/30.0
           # jump = False
            #if(rectBall.colliderect(rectCollisionBlock) == 0):
               # print("Killed!")
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
               # offsetCollisionRamp_x = rectCollisionBlock.x - mouse_x
              #  offsetRamp_x = rectCollisionBlock.x + 504 - mouse_x
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:    
                m_drag = False
                speed = abs(pygame.mouse.get_rel()[0])
                speed = speed/2

        elif event.type == pygame.MOUSEMOTION:
            if m_drag:
                mouse_x, mouse_y = event.pos
                index = 0
                for i in blocks: #Move all blocks and ramps in unison.
                    i.x = mouse_x + offsets[index]
                    ramps[index].x = i.x + 504
                    index = index + 1
                #rectCollisionBlock.x = mouse_x + offsetCollisionRamp_x
                #rectRamp.x = rectCollisionBlock.x + 504
                initVel = abs(pygame.mouse.get_rel()[0])
                initVel = max(min(initVel,15),7)



    ##hits = rectBall.colliderect(rectRamp)

   # print(hits)
    #if hits == 1 and jump == False:
     #    jump = True

    #Check if we should be jumping
    for i in ramps:
        if(rectBall.colliderect(i) == 1 and jump == False and unlockJumping == True):
            jump = True
            jumpVel = initVel
            unlockJumping = False

    #if(rectBall.colliderect(rectRamp) == 1 and jump == False and unlockJumping == True):
        #jump = True
        #jumpVel = initVel
        #unlockJumping = False

    screen.fill((0,0,0))
    screen.blit(tBack,rectBack)
    screen.blit(tBall,rectBall)
    index = 0
    for i in blocks: #blit all sprites to the screen
        screen.blit(rampSprites[index],(ramps[index].x, ramps[index].y))
        screen.blit(blockSprites[index],(blocks[index].x, blocks[index].y))
        index = index + 1

    #screen.blit(tRamp,(rectRamp.x,rectRamp.y))
    #screen.blit(tCollisionBlock,(rectCollisionBlock.x, rectCollisionBlock.y))

    pygame.display.update()
       # if event.type == 
    #pygame.surface.convert(texture, textureScreen)
    

