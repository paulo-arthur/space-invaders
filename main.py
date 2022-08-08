import pygame, random, sys
from time import time
from elements import spaceships, get_ammo, get_enemy

pygame.init()
#pygame.font.get_init()

pygame.display.set_caption('Space Invaders')

WIDTH = 1000
HEIGHT = 600
BLACK = 50, 40, 70
WHITE = 220, 220, 220

ENEMYS_TIME = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))

spaceship = spaceships(WIDTH, HEIGHT)

ammo = []
enemies = {'number': 5, 'bullet_speed': 1, 'enemies': []}
enemy_ammo = []

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #screen
    screen.fill(BLACK)

    keys = pygame.key.get_pressed()

    #spaceship control & limits
    if keys[pygame.K_w] and spaceship['y'] >= 0:
        spaceship['y'] -= spaceship['speed']
    if keys[pygame.K_s] and spaceship['y'] <= HEIGHT - spaceship['size'][1]:
        spaceship['y'] += spaceship['speed']
    if keys[pygame.K_a] and spaceship['x'] >= 0:
        spaceship['x'] -= spaceship['speed']
    if keys[pygame.K_d] and spaceship['x'] <= WIDTH - spaceship['size'][0]:
        spaceship['x'] += spaceship['speed']

    #ammo
    if keys[pygame.K_SPACE]:
        if len(ammo) == 0 or time() - ammo[-1]['time'] > spaceship['recoil']:
            ammo.append(get_ammo(spaceship['x'] + spaceship['size'][0]/2 - 5, spaceship['y'], time()))

    for bullet in ammo:
        pygame.draw.rect(screen, bullet['color'], pygame.Rect(bullet['x'],
                                                    bullet['y'],
                                                    bullet['size'],
                                                    bullet['size']))
        bullet['y'] -= bullet['speed']

        if bullet['y'] < -10:
            del ammo[ammo.index(bullet)]

    #spaceship
    pygame.draw.rect(screen, WHITE, pygame.Rect(spaceship['x'],
                                                spaceship['y'],
                                                spaceship['size'][0],
                                                spaceship['size'][1]))

    #enemies
    if len(enemies['enemies']) == 0:
        for _ in range(0, enemies['number']):
            enemies['enemies'].append(get_enemy(WIDTH, HEIGHT, enemies['number']))
        enemies['number'] += 1
        enemies['bullet_speed'] += 0.005


    for enemy in enemies['enemies']:
        enemy_rect = pygame.Rect(enemy['x'],
                                 enemy['y'],
                                 enemy['size'][0],
                                 enemy['size'][1])

        pygame.draw.rect(screen, enemy['color'], enemy_rect)
        enemy['x'] += enemy['speed']

        #enemy collision
        if enemy['x'] >= WIDTH - enemy['size'][0] or enemy['x'] <= 0:
            enemy['speed'] *= -0.1 * random.randint(8, 12)

        #enemy's_shot
        if time() - enemy['last_shot'] >= ENEMYS_TIME:
            enemy_bullet = get_ammo(enemy['x'], enemy['y'], None)
            enemy_bullet['speed'] *= 0.5
            enemy_ammo.append(enemy_bullet)
            enemy['last_shot'] = time()
            ENEMYS_TIME -= enemy['recoil'] if ENEMYS_TIME >= 1 else 0

        #enemy's death
        bullet_list = []
        for bullet in ammo:
            bullet_list.append(pygame.Rect(
                bullet['x'], bullet['y'], bullet['size'], bullet['size']
            ))
        enemy_death = enemy_rect.collidelist(bullet_list)

        if enemy_death != -1:
            del enemies['enemies'][enemies['enemies'].index(enemy)]
            del ammo[enemy_death]

    #enemies's shots
    for bullet in enemy_ammo:
        pygame.draw.rect(screen, WHITE, pygame.Rect(
            bullet['x'], bullet['y'], bullet['size'], bullet['size']
        ))
        bullet['y'] += enemies['bullet_speed']

        #spaceship death
        spaceship_death = pygame.Rect(bullet['x'], bullet['y'], bullet['size'], bullet['size']).collidelist([pygame.Rect(spaceship['x'],
                                                    spaceship['y'],
                                                    spaceship['size'][0],
                                                    spaceship['size'][1])])
        if spaceship_death != -1:
            sys.exit()

        #enemies bullets clean
        if bullet['y'] > HEIGHT + 10:
            del enemy_ammo[enemy_ammo.index(bullet)]
    pygame.display.update()
