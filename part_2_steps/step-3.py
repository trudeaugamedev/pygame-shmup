"""Cookie class (code inside the class copied and modified)"""

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

class Cookie(pygame.sprite.Sprite):
    def __init__(self, x, y, x_vel, y_vel):
        super().__init__(cookies)

        self.image = cookie_img
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = self.x
        self.rect.y = self.y

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.x_vel = -self.x_vel
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.y_vel = -self.y_vel

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

cookies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

Cookie(0, 0, 5, 2)
Cookie(100, 50, 3, 5)
Cookie(200, 300, -3, 2)

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

    bullets.update()
    cookies.update()

    screen.blit(bg_img, (0, 0))

    bullets.draw(screen)
    cookies.draw(screen)
    screen.blit(player_img, (x, y))

    pygame.display.update()

pygame.quit()