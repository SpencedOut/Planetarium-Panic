import pygame, os, Loader, Physics



initVel = 10
g = 9.8
getTicksLastFrame = 0
jump = False
deltaT= 1.0/30.0



class player:

    spriteGroup = None

    def __init__(self):
        self.playerObject = Loader.loaderObjects("ing.png")
        
    def bcCollision(self, spriteGroup):
            
        if spriteGroup == 'L0':
            # GAME END
            print('game over')

        elif spriteGroup == 'L1':
            # L1 COLLISION DETECTED
            print('L1')

        elif spriteGroup == 'L2':
            # L2 COLLISION DETECTED
            print('L2')

        elif spriteGroup == 'L3':
            # L3 COLLISION DETECTED
            print('L3')

        elif spriteGroup == 'L4':
            # L3 COLLISION DETECTED
            print('L4')

        else:
            # NO COLLISION DETECTED
            print('No collision detected')

    def gravity():
        if jump == True: # GRAVITY
            if rectBall.y > 500:
                rectBall.y = 500
                deltaT = 1.0/30.0
                jump = False
            else:
                rectBall.y -= initVel*deltaT - g*deltaT*deltaT*0.5
                deltaT+= 1.0/30.0 # /GRAVITY
