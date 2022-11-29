"""Linking user input to movement"""

import pygame
from pygame.locals import *

FPS = 60
WIDTH, HEIGHT = 400, 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHMUP!")
clock = pygame.time.Clock()

player_img = pygame.image.load("player.png").convert_alpha()

x = 180
y = 340

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        x -= 4
    if keys[K_RIGHT]:
        x += 4

    screen.fill((0, 0, 0))

    screen.blit(player_img, (x, y))

    pygame.display.update()

pygame.quit()