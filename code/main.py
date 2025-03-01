import pygame, random
from pathlib import Path
from os.path import join

#general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display_title = pygame.display.set_caption("Space Shooter")
# icon_path = Path("5games-main\space shooter\images\player.png")
icon = pygame.image.load(join("5games-main", "space shooter", "images", "player.png")).convert_alpha()
pygame.display.set_icon(icon)
running = True
velocity_h = 0.2

#plain surface
surf = pygame.Surface((100, 200))
surf.fill("orange")
x = 100

#importing an image
player_surf = pygame.image.load(join("5games-main", "space shooter", "images", "player.png")).convert_alpha()
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
star_surf = pygame.image.load(join("5games-main", "space shooter", "images", "star.png")).convert_alpha()
star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]
meteor_surf = pygame.image.load(join("5games-main", "space shooter", "images", "meteor.png")).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
laser_surf = pygame.image.load(join("5games-main", "space shooter", "images", "laser.png")).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT-20))

while running:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the game
    display_surface.fill('darkgray')


    for position in star_positions:
        display_surface.blit(star_surf, position)

    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)

    player_rect.left += velocity_h

    if player_rect.right >= WINDOW_WIDTH or player_rect.left <= 0:
        velocity_h = -velocity_h

    display_surface.blit(player_surf, player_rect)

    pygame.display.update()

pygame.quit()