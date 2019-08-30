
import pygame, sys, os
from pygame.math import Vector2


class Entity(pygame.sprite.Sprite):

    def __init__(self, pos, tex, offset, rotAngle, scale): # rotAngle +ve for clockwise rotation, -ve for anti-clockwise rotation
        super().__init__()
        self.image = pygame.image.load(os.getcwd()+'\\images\\'+tex)
        self.image = pygame.transform.scale(self.image, (scale))
        # A reference to the original image to preserve the quality.
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.orig_image, 10)
        self.pos = Vector2(pos)  # The original center position/pivot point.
        self.offset = Vector2(offset)  # We shift the sprite offset px to the right.
        self.angle = 0
        self.rotAngle = rotAngle
        self.g = 9.8
        self.deltaT = 1.0/30.0

    def updatePos(self,initVel,jump,basePos):
        if jump == True:
            self.pos.y -= initVel -(0.5* self.g *self.deltaT*self.deltaT)
            self.deltaT+= 1.0/30.0
        else:
            self.pos.y = basePos
            self.deltaT = 1.0/30.0
        
    def updateDir(self, dir):
        self.rotAngle = dir

    def initialRot(self,rot):
        self.angle = rot
        self.rotate()

    def update(self):
        self.angle = self.angle + self.rotAngle
        self.rotate()

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos+offset_rotated)

    def getRect(self):
        return self.rect

#class for linear ramp
class linearEntity():
    def __init__(self):
        #self.rect = pygame.Surface((450,30), 0 ,32)
        #self.rect.fill((255,255,255))
        self.rect = pygame.Rect(1280,345,450,30)

    def move(self):
        self.rect.x-=10
