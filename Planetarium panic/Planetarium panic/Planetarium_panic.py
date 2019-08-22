
#Main Game Loop


import pygame,sys,os
import Loader

#loader planetLoader ("Outer Edge.png")




screen = pygame.display.set_mode((0,0), flags = pygame.FULLSCREEN) #CREATES THE FULLSCREEN

tOuterRing = pygame.image.load(os.getcwd()+"\\Outer Edge.png") #LOADS THE OUTER EDGE IMAGE
tOuterRing = pygame.transform.scale(tOuterRing, (800,800)) #SCALES THE OUTER EDGE IMAGE
rectOuterRing = tOuterRing.get_rect()
rectOuterRing = rectOuterRing.move(560,680) #MOVES THE OUTER EDGE IMAGE AND SURFACE TO CENTER BOTTOM

tInnerRing = pygame.image.load(os.getcwd()+"\\Inner Circle.png") # INNER CIRCLE CODE
tInnerRing = pygame.transform.scale(tInnerRing, (720,720))
rectInnerRing = tInnerRing.get_rect()
rectInnerRing = rectInnerRing.move(600,720)
                              
outerRing = screen.blit(tOuterRing, rectOuterRing) #JOINING THE CIRCLE TEXTURES WITH THEIR RECT SURFACES
innerRing = screen.blit(tInnerRing, rectInnerRing)

#planet = screen.blit(innerRing, outerRing)


while 1:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key & pygame.K_q:
                sys.exit

       # if event.type == 
    #pygame.surface.convert(texture, textureScreen)

