import pygame
import os

class loaderObjects:
    texture = pygame.image.load(os.getcwd()+"\\images\\404T.png") #DEFAULT 404 TEXTURE
    
    def __init__(self, texInput): #CONSTRUCTOR FOR THE OBJECT
        pygame.sprite.Sprite.__init__(self)
        self.texture = pygame.image.load(os.getcwd()+"\\"+texInput)
        self.rect = self.texture.get_rect()
        self.mask = pygame.mask.from_surface(self.texture)

    #pygame.transform.scale(texLoc,)# to scale the 404 texture to the rectangle
    