import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter - Eagle Eye View")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load assets
player_img = pygame.image.load("player.png")
zombie_img = pygame.image.load("zombie.png")

# Scale images
player_img = pygame.transform.scale(player_img, (50, 50))
zombie_img = pygame.transform.scale(zombie_img, (50, 50))

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
    
    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
    
    def draw(self):
        screen.blit(player_img, (self.x, self.y))

# Bullet class
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 7
        self.angle = angle
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)

# Zombie class
class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
    
    def move(self, player_x, player_y):
        angle = math.atan2(player_y - self.y, player_x - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed
    
    def draw(self):
        screen.blit(zombie_img, (self.x, self.y))

# Game loop
player = Player(WIDTH // 2, HEIGHT // 2)
bullets = []
zombies = []
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - player.y, mouse_x - player.x)
            bullets.append(Bullet(player.x + 25, player.y + 25, angle))
    
    # Move player
    player.move(keys)
    player.draw()
    
    # Move bullets
    for bullet in bullets:
        bullet.move()
        bullet.draw()
    
    # Spawn zombies randomly
    if random.randint(1, 100) < 2:
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            zombies.append(Zombie(0, random.randint(0, HEIGHT)))
        elif side == "right":
            zombies.append(Zombie(WIDTH, random.randint(0, HEIGHT)))
        elif side == "top":
            zombies.append(Zombie(random.randint(0, WIDTH), 0))
        else:
            zombies.append(Zombie(random.randint(0, WIDTH), HEIGHT))
    
    # Move and draw zombies
    for zombie in zombies:
        zombie.move(player.x, player.y)
        zombie.draw()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()

