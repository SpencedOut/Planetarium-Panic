import pygame,os

pygame.init()
screen = pygame.display.set_mode((1280,720))
texImage = pygame.image.load(os.getcwd() + '\\images\\Outer edge.png')
texImage = pygame.transform.scale(texImage, (640,480))
rectImage = texImage.get_rect()
pygame.display.flip()

def turn (image, angle):
    oldCenter = rectImage.center
    Rimage = pygame.transform.rotate(image, angle)
    rect = Rimage.get_rect()
    rect.center = oldCenter
    texImage = Rimage
    screen.blit(texImage,rect)
    print("Rotating")

while 1:
    angle=10
    turn(texImage, angle)
    screen.blit(texImage, (640,480))
    pygame.display.flip()
