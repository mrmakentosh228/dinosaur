import pygame
import os
import random


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Dino(pygame.sprite.Sprite):
    pass


class Strawberry(pygame.sprite.Sprite):
    pass

pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
running = True

dino_sprite = pygame.sprite.Group()
str_sprite = pygame.sprite.Group()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
