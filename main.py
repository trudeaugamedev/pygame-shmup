import sys  # Import the system module, literally just for quitting the game cleanly
import pygame
from pygame.locals import *
from random import randint  # Import randint from random, which generates a random number between two numbers

FPS = 60
WIDTH, HEIGHT = 400, 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHMUP!")
clock = pygame.time.Clock()

player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (36, 56))
cookie_img = pygame.image.load("cookie.png").convert_alpha()
bullet_img = pygame.image.load("bullet.png").convert_alpha()    # Load the bullet image
bullet_img = pygame.transform.scale(bullet_img, (12, 28))       # Resize it to the correct size
bg_img = pygame.image.load("background.png").convert() # We don't need the background to be transparent, so we use "convert"

class Player(pygame.sprite.Sprite): # Make the player have stuff that a pygame sprite needs to have (Inheriting from pygame.sprite.Sprite)
    def __init__(self): # The function that gets called when the sprite is created
        super().__init__() # Initialize the player as a pygame sprite

        self.image = player_img             # Set the player's image to the player image. Pygame uses this variable to draw the sprite
        self.rect = player_img.get_rect()   # Generate the player's rect. Pygame uses this variable to know where to draw the sprite

        self.x = 180    # Custom x position variable
        self.y = 340    # Custom y position variable

    def update(self):   # The function that contains player logic
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.x -= 4             # Get keys and move the player, we've done this before :P
        if keys[K_RIGHT]:
            self.x += 4

        self.rect.x = self.x    # Update the player rect position to our x and y variables
        self.rect.y = self.y

        if self.rect.left < 0:                  # Restrict the player's left to inside the screen
            self.x = 0
            self.rect.x = self.x                # Re-update the rect after we do so
        elif self.rect.right > WIDTH:           # Restrict the player's right to inside the screen
            self.x = WIDTH - self.rect.width
            self.rect.x = self.x                # Re-update the rect after we do so

        # "spritecollide" detects collision between a sprite and sprites in a group
        # This function takes a sprite: "self" (the player)
        # takes a group: "cookies"
        # takes a boolean (True/False) that determines whether the collided sprite in the group gets deleted or not
        # and optionally takes a special function: "pygame.sprite.collide_rect_ratio(0.8)"
        # In this case, our special pygame function makes the rects of each sprite 0.8 times smaller (so it's harder to lose, you're welcome)
        if pygame.sprite.spritecollide(self, cookies, False, pygame.sprite.collide_rect_ratio(0.8)):
            pygame.quit()   # If the player collided with something, quit the game
            sys.exit()      # A new thingy that just makes sure the game closes correctly, don't worry about it

    def draw(self, screen): # Function that draw the player
        screen.blit(self.image, self.rect)  # Draw the image at the position of the rect

class Cookie(pygame.sprite.Sprite):
    # The cookie takes 4 arguments in the brackets after __init__:
    # x: the x position of the cookie
    # y: the y position of the cookie
    # x_vel: the x velocity of the cookie
    # y_vel: the y_velocity of the cookie
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

        self.rect.x = self.x      # Set the x position of the rect to draw the image at to be x
        self.rect.y = self.y      # Set the y position of the rect to draw the image at to be y

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
        self.y -= 10                # Constantly move the bullet up

        # Update the center x and y position of the bullet, we are using "center" here so that it's easier to align the bullet with the player
        self.rect.centerx = self.x
        self.rect.centery = self.y

        if self.rect.bottom < 0:    # If the bottom side of the bullet goes above the top of the screen
            self.kill()             # Remove the bullet, .kill() will remove the sprite from all groups, which will essentially delete it

cookies = pygame.sprite.Group() # Create a pygame group for cookies
bullets = pygame.sprite.Group() # Create a pygame group for bullets
player = Player()               # Create the player

spawn_rate = 60 # Extra: the original spawn rate of the cookies (the higher the number, the slower the spawning)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # We are using this type of key press detection because this only detects when the key is pressed down, instead of continuously
        if event.type == KEYDOWN:       # If a key is pressed
            if event.key == K_SPACE:    # If the key is space
                Bullet(player.rect.centerx, player.y)  # Spawn a bullet at the correct position relative to the player

    spawn_rate -= 0.01  # Decrease the spawn rate number, thus increasing the actual spawn rate
    if spawn_rate < 20: # If the spawn rate gets lower than 20
        spawn_rate = 20 # stop it from getting lower (or else do you still want to play?!)
    if randint(0, int(spawn_rate)) == 0:    # A random chance of spawning a cookie on a given frame, the higher the spawn rate, the lower the chance
        # Spawn the cookie at roughly the top half of the screen
        # and also give it a randomized direction by passing in a random velocity
        Cookie(randint(50, WIDTH - 50), randint(50, 100), randint(-5, 5), randint(-5, 5))

    cookies.update()    # Update all cookies
    bullets.update()    # Update all bullets
    player.update()     # Update the player
    # The "groupcollide" function detects collision between two sprite groups
    # This function takes two groups between which you want to test for collision
    # It also takes two booleans (True/False) that determines whether the collided sprites get deleted or not
    # The first and second boolean corresponds to the first and second group, respectively
    # It also takes an optional function, that pygame uses to modify the collision, we are not using that here
    # Go up the the player & cookie collision to see more about this optional function
    pygame.sprite.groupcollide(bullets, cookies, True, True)

    screen.blit(bg_img, (0, 0)) # Draw the background image

    bullets.draw(screen)    # Draw all bullets
    cookies.draw(screen)    # Draw all cookies
    player.draw(screen)     # Draw the player

    pygame.display.update()

pygame.quit()