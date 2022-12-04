"""Base pygame code"""

import pygame
from pygame.locals import *

FPS = 60
WIDTH, HEIGHT = 400, 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHMUP!")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame.display.update()

pygame.quit()