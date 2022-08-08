import random
from time import time

def spaceships(WIDTH, HEIGHT):
    return {
        'x': WIDTH/2 - 30/2,
        'y': HEIGHT - 30 - 30,
        'size': [30, 30],
        'speed': 0.5,
        'recoil': 0.8
    }

def get_ammo(x, y, time):
    return {
        'x': x,
        'y': y,
        'size': 10,
        'speed': 1,
        'time': time,
        'color': (120, 255, 120)
    }

def get_enemy(WIDTH, HEIGHT, n):
    return {
        'x': random.randint(0.1 * WIDTH, 0.9 * WIDTH),
        'y': 30 + random.randint(0, HEIGHT * 0.2),
        'size': [30, 30],
        'speed': random.choice([-1, 1]) * 0.5,
        'recoil': 0.005,
        'last_shot': time(),
        'color': (random.randint(150, 230), 70, random.randint(60, 140))
    }
