import pygame as pg
from random import randint

pg.init()

screen = pg.display.set_mode((1000, 1000))
pg.display.set_caption('Asteroids!')

##### CLASSES #####
    # Asteroid
class Asteroid():
    def __init__(self, pos):
        self.position = [pos, 0]
        self.scale = randint(50, 150)
        self.collider = pg.Rect((self.position[0], self.position[1]), (self.scale, self.scale))
        self.health = self.scale // 50
        self.speed = 0.5

    def move(self):
        self.position[1] += 1
        self.collider = pg.Rect((self.position[0], self.position[1]), (self.scale, self.scale))

    def draw(self):
        pg.draw.rect(screen, (115, 115, 115), (self.position[0], self.position[1], self.scale, self.scale))

    def get_shot(self):
        for bullet in projectiles:
            if self.collider.colliderect(bullet.collider):
                projectiles.remove(bullet)
                asteroids.remove(self)

    # Projectile
class Projectile():
    def __init__(self):
        self.position = player.position
        self.impulse = player.speed / 2 * player.heading
        self.speed = 1
        self.collider = pg.Rect((self.position[0], self.position[1]), (5, 10))

        # Draw projectile
    def draw(self):
        pg.draw.rect(screen, (255, 255, 255), (self.position[0] + 10, self.position[1], 5, 10))

        # Move projectile
    def move(self):
        self.position = [self.position[0] - self.impulse, self.position[1] - self.speed]
        self.collider = pg.Rect((self.position[0], self.position[1]), (5, 10))

    # Player
class Player():
    def __init__(self):
        self.position = [500, 925]
        self.health = 3
        self.heading = 0
        self.speed = 1.5

        # Draw player
    def draw(self):
        pg.draw.rect(screen, (255, 255, 255), (self.position[0], self.position[1], 25, 50))

        # Update player position
    def update_pos(self):
        self.position[0] -= self.speed * self.heading

##### MAIN LOOP #####
running = True
player = Player()
projectiles = []
holding_keys = pg.key.get_pressed()
asteroids = []
respawn_counter = 120
asteroids_barrier = 5

    # Loop
while running:
    player_pos_changed = False
    event = pg.event.get()
        # Quit event
    if event == pg.QUIT:
        running = False

    keys = pg.key.get_pressed()

        # Move player left
    if keys[pg.K_LEFT] and not player.position[0] <= 0:
        player_pos_changed = True
        player.heading = 1

        # Move player right
    elif keys[pg.K_RIGHT] and not player.position[0] >= 975:
        player_pos_changed = True
        player.heading = -1

        # Shoot
    if keys[pg.K_SPACE] and not holding_keys[pg.K_SPACE] and len(projectiles) < 5:
        projectiles.append(Projectile())

        # Set player heading to 0 if not moving
    if not player_pos_changed:
        player.heading = 0

    holding_keys = keys

        # Spawn asteroids
    if respawn_counter == 0:
        if randint(0, 1) == 1 and len(asteroids) < asteroids_barrier:
            asteroids.append(Asteroid(randint(0, 950)))
        else:
            pass
        respawn_counter = 120
    else:
        respawn_counter -= 1

        # Draw all objects
    screen.fill((0, 0, 0))

    for projectile in projectiles:
        projectile.draw()
        projectile.move()

        if projectile.position[0] < 0 or projectile.position[0] > 1000 or projectile.position[1] < 0 or projectile.position[1] > 1000:
            projectiles.remove(projectile)

    for asteroid in asteroids:
        asteroid.draw()
        asteroid.move()
        asteroid.get_shot()
        if asteroid.position[1] >= 1000:
            asteroids.remove(asteroid)

    player.draw()

    if player_pos_changed:
        player.update_pos()

    pg.display.update()


pg.quit()