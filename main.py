"""Separate collision rect"""

import sys
import pygame
from pygame.locals import *
from random import randint

FPS = 60
WIDTH, HEIGHT = 400, 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHMUP!")
clock = pygame.time.Clock()

player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale_by(player_img, 4)
cookie_img = pygame.image.load("cookie.png").convert_alpha()
bullet_img = pygame.image.load("bullet.png").convert_alpha()
bullet_img = pygame.transform.scale_by(bullet_img, 4)
bg_img = pygame.image.load("background.png").convert()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = player_img
        self.rect = player_img.get_rect()

        self.x = 180
        self.y = 340

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.x -= 4
        if keys[K_RIGHT]:
            self.x += 4

        self.rect.x = self.x
        self.rect.y = self.y

        if self.rect.left < 0:
            self.x = 0
            self.rect.x = self.x
        elif self.rect.right > WIDTH:
            self.x = WIDTH - self.rect.width
            self.rect.x = self.x

        if pygame.sprite.spritecollide(self, cookies, False, pygame.sprite.collide_rect_ratio(0.8)):
            pygame.quit()
            sys.exit()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Cookie(pygame.sprite.Sprite):
    def __init__(self, x, y, x_vel, y_vel):
        super().__init__(cookies)

        self.image = cookie_img                 # Set the cookie's image to cookie image
        self.rect = self.image.get_rect()       # Generate a rect from the image

        self.x = x              # The x position of the cookie
        self.y = y              # The y position of the cookie
        self.x_vel = x_vel      # The x velocity (speed) of the cookie
        self.y_vel = y_vel      # The y velocity (speed) of the cookie

    def update(self):
        self.x += self.x_vel    # Add the x velocity to the x position
        self.y += self.y_vel    # Add the y velocity to the y position

        self.rect.centerx = self.x      # Set the center x position of the rect to draw the image at to be x
        self.rect.centery = self.y      # Set the center y position of the rect to draw the image at to be y

        if self.rect.left < 0 or self.rect.right > WIDTH:   # If the left or right side of the rect is outside the window
            self.x_vel = -self.x_vel                        # Reverse the x velocity (bounce)
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:  # If the top or bottom side of the rect is outside the window
            self.y_vel = -self.y_vel                        # Reverse the y velocity (bounce)

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
        self.rect.y = self.y

        if self.rect.bottom < 0:
            self.kill()

cookies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()

spawn_rate = 60

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                Bullet(player.x + player_img.get_width() / 2, player.y - 10)

    spawn_rate -= 0.01
    if spawn_rate < 20:
        spawn_rate = 20
    if randint(0, int(spawn_rate)) == 0:
        Cookie(randint(50, WIDTH - 50), randint(50, 100), randint(-5, 5), randint(-5, 5))
        
    cookies.update()
    bullets.update()
    player.update()
    pygame.sprite.groupcollide(bullets, cookies, True, True)

    screen.blit(bg_img, (0, 0))

    bullets.draw(screen)
    cookies.draw(screen)
    player.draw(screen)

    pygame.display.update()

pygame.quit()