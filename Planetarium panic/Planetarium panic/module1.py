import pygame,sys


pygame.init()

FPS = 30 
fpsClock= pygame.time.Clock()


DISPLAYSURF= pygame.display.set_mode((800,800))

pygame.display.set_caption('Planetorium Panic!')

background = pygame.image.load("C:\\Users\\u1271129\\Desktop\\Space.png")
backrect= background.get_rect()
backrect_y = 0
ball= pygame.image.load("C:\\Users\\u1271129\\Desktop\\intro_ball.gif")
ballrect= ball.get_rect()
ballx = 400
bally = 420
m_drag= False
speed = 0

while True:
    DISPLAYSURF.fill((0,0,0))
    DISPLAYSURF.blit(background,(backrect.x,backrect_y))

    DISPLAYSURF.blit(ball,(ballx,bally))
    
    if speed!=0:
        backrect.x -= speed
        speed /= 1.5

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
   
            if event.button == 1:
                m_drag=True
                mouse_x,mouse_y = event.pos
                offset_x = backrect.x - mouse_x
                offset_y = backrect.y - mouse_y
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:    
                m_drag = False
                speed = abs(pygame.mouse.get_rel()[0])
                speed = speed/2

        elif event.type == pygame.MOUSEMOTION:
            if m_drag:
                mouse_x, mouse_y = event.pos
                backrect.x = mouse_x + offset_x
                backrect.y = mouse_y + offset_y


    pygame.display.update()
    fpsClock.tick(FPS)

