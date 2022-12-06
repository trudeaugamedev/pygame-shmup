"""Bullet class, bullet spawning, bullet update and draw"""

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
bullet_img = pygame.image.load("bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (12, 28))
bg_img = pygame.image.load("background.png").convert()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bullets)

        self.image = bullet_img
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

    def update(self):
        self.y -= 10

        self.rect.centerx = self.x
        self.rect.centery = self.y

        if self.rect.bottom < 0:
            self.kill()

x = 180
y = 340

cookie_x = 0
cookie_y = 0
cookie_x_vel = 5
cookie_y_vel = 2
cookie_rect = cookie_img.get_rect()

bullets = pygame.sprite.Group()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                Bullet(x + player_img.get_width() / 2, y)

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
        
    bullets.update()

    screen.blit(bg_img, (0, 0))

    bullets.draw(screen)
    screen.blit(cookie_img, (cookie_x, cookie_y))
    screen.blit(player_img, (x, y))

    pygame.display.update()

pygame.quit()