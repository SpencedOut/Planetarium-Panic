
#Main Game Loop


import pygame,sys,os

def startGame():
    loader planetLoader("Outer Edge.png")



while 1:
    screen = pygame.display.set_mode((1280,720))
    texture = pygame.image.load(os.getcwd()+"\\404T.png")
    textureScreen = texture.get_rect()
  
    screen.blit(texture,textureScreen)
    pygame.display.flip()
    #pygame.surface.convert(texture, textureScreen)

print (os.getcwd())

