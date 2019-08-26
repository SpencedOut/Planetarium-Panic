import pygame,sys
from pygame.locals import *
pygame.init()

initVel = 10
g = 9.8
getTicksLastFrame = 0
jump = False
deltaT= 1.0/30.0

Display = pygame.display.set_mode((1280,720))
back = pygame.image.load("C:\\Users\\u1271129\\Desktop\\Space.png")
back = pygame.transform.scale(back,(1280,720))
backrect = back.get_rect()
ball = pygame.image.load("C:\\Users\\u1271129\\Desktop\\intro_ball.gif")
ballrect = ball.get_rect()
ballrect.x = 640
ballrect.y = 420



while True:
    Display.blit(back,backrect)  
    Display.blit(ball,ballrect)
    if jump == True:
        if ballrect.y > 420:
            ballrect.y = 420
            deltaT = 1.0/30.0
            jump = False
        else:
            ballrect.y-= initVel*deltaT - g*deltaT*deltaT*0.5
            deltaT+= 1.0/30.0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                if(ballrect.y == 420):
                    jump = True
                    
             
    pygame.display.update()
