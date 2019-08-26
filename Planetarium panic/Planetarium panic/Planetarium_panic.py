
#Main Game Loop


import pygame,sys,os
from pygame.locals import *
import Loader, Player

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

initVel = 0
g = 9.8
getTicksLastFrame = 0
jump = False
deltaT= 1.0/30.0

tBall = pygame.image.load(os.getcwd()+"\\images\\ball.gif")
tBall = pygame.transform.scale(tBall, (100,100))
rectBall = tBall.get_rect()
rectBall.x = 590
rectBall.y = 500

tRamp = pygame.image.load(os.getcwd()+"\\images\\Ramp.png")
tRamp = pygame.transform.scale(tRamp,(100,100))
rectRamp = tRamp.get_rect()
rectRamp.x = 540 + 302
rectRamp.y = 500

tCollisionBlock = pygame.image.load(os.getcwd()+"\\images\\collisionBlock.png")
rectCollisionBlock = tCollisionBlock.get_rect()
widthCollisionBlock = rectCollisionBlock.width
heightCollisionBlock = rectCollisionBlock.height
print (widthCollisionBlock)

rectCollisionBlock.y = 600
rectCollisionBlock.x = 640 - (widthCollisionBlock/2)

#rampSprites = pygame.sprite.Group()
#rampSprites.add(rectRamp)

                              
#outerRing = screen.blit(tOuterRing, rectOuterRing) #JOINING THE CIRCLE TEXTURES WITH THEIR RECT SURFACES
#innerRing = screen.blit(tInnerRing, rectInnerRing)

#planet = screen.blit(innerRing, outerRing)

m_drag= False
speed = 0


while True:
    screen.fill((0,0,0))
    screen.blit(tBack,rectBack)
    screen.blit(tBall,rectBall)
    screen.blit(tRamp,(rectRamp.x,rectRamp.y))
    screen.blit(tCollisionBlock,(rectCollisionBlock.x, rectCollisionBlock.y))
    jump == False
    
    if speed!=0:
        
         # MOVE ALL OTHER SPRITES TO THE LEFT

        rectCollisionBlock.x -= speed
        rectRamp.x-= speed
        speed /= 1.5


    if jump == True: # GRAVITY
        if rectBall.y > 500:
            rectBall.y = 500
            deltaT = 1.0/30.0
            jump = False
        else:
            rectBall.y -= initVel*deltaT - g*deltaT*deltaT*0.5
            deltaT+= 1.0/30.0 # /GRAVITY

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                m_drag=True
                mouse_x, mouse_y = event.pos
                offsetCollisionRamp_x = rectCollisionBlock.x - mouse_x
              #  offsetRamp_x = rectCollisionBlock.x + 504 - mouse_x
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:    
                m_drag = False
                speed = abs(pygame.mouse.get_rel()[0])
                speed = speed/2

        elif event.type == pygame.MOUSEMOTION:
            if m_drag:
                mouse_x, mouse_y = event.pos
                
                rectCollisionBlock.x = mouse_x + offsetCollisionRamp_x
                rectRamp.x = rectCollisionBlock.x + 504
                initVel = abs(pygame.mouse.get_rel()[0])
                initVel = max(min(initVel,15),10)



    hits = rectBall.colliderect(rectRamp)
    if hits and not jump:
         jump = True


    pygame.display.update()
       # if event.type == 
    #pygame.surface.convert(texture, textureScreen)
    

