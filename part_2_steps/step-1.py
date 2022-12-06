"""Base code from last time (minus the rotation plus background)"""

import pygame
from pygame.locals import *

FPS = 60
WIDTH, HEIGHT = 400, 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHMUP!")
clock = pygame.time.Clock()

player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (36, 56))
cookie_img = pygame.image.load("cookie.png").convert_alpha()
bg_img = pygame.image.load("background.png").convert() # We don't need the background to be transparent, so we use "convert"

x = 180
y = 340

cookie_x = 0
cookie_y = 0
cookie_x_vel = 5
cookie_y_vel = 2
cookie_rect = cookie_img.get_rect()

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

    cookie_x += cookie_x_vel
    cookie_y += cookie_y_vel
    cookie_rect.x = cookie_x
    cookie_rect.y = cookie_y
    if cookie_rect.left < 0 or cookie_rect.right > WIDTH:
        cookie_x_vel = -cookie_x_vel
    if cookie_rect.top < 0 or cookie_rect.bottom > HEIGHT:
        cookie_y_vel = -cookie_y_vel

    screen.blit(bg_img, (0, 0)) # Draw the background image. It's the same size as the window, so we draw from the topleft (0, 0)

    screen.blit(cookie_img, (cookie_x, cookie_y))
    screen.blit(player_img, (x, y))

    pygame.display.update()

pygame.quit()