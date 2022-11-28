"""User input"""

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

    keys = pygame.key.get_pressed()     # Get a list full of keys that are currently pressed
    if keys[K_LEFT]:                    # If the left arrow key is pressed
        print("LEFT")                   # Print "LEFT" in the console
    if keys[K_RIGHT]:                   # If the right arrow key is pressed
        print("RIGHT")                  # Print "RIGHT" in the console

    screen.fill((0, 0, 0))

    pygame.display.update()

pygame.quit()