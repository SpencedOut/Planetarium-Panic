# Pygame sprite group
import pygame, os
from Loader import loaderObjects

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

#loaderObjects bat("sdg.jpg")
    
#grouping the sprite
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
moon = Moon()
all_sprites.add(moon)
other_sprite = pygame.sprite.Group()
other_sprite.add(moon)

# Game loop
running = True
while running:
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
            
        
    # Update
    all_sprites.update()

    #check to see if collision happens
    hits = pygame.sprite.spritecollide(player, other_sprite, False, pygame.sprite.collide_mask)
    if hits:
        print("Overlap")
    # Draw / render
    screen.fill(BLUE)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()
pygame.quit()

