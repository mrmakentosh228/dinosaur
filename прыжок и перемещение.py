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


def jump_coords(y_position, speed):
    y_position -= speed
    if y_position > 790:
        y_position = 790
        global jump_flag
        jump_flag = False
        global current_speed
        current_speed = 200 / fps
    return y_position


class Dino(pygame.sprite.Sprite):
    pass


class Strawberry(pygame.sprite.Sprite):
    pass


pygame.init()
size = 800, 800
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
fps = 60
x_pos = 400
y_pos = 790
x_old = x_pos
y_old = y_pos
current_speed = 200 / fps
clock = pygame.time.Clock()
running = True
jump_flag = False
g = False
t = True
go_right = False
go_left = False

dino_sprite = pygame.sprite.Group()
str_sprite = pygame.sprite.Group()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and t:
                g = True
            if event.key == pygame.K_RIGHT:
                go_right = True
            if event.key == pygame.K_LEFT:
                go_left = True
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_SPACE]:
                g = False
                jump_flag = True
            if event.key in [pygame.K_RIGHT]:
                go_right = False
            if event.key in [pygame.K_LEFT]:
                go_left = False
    # вычисляем координаты по x
    if go_right:
        x_pos += 3
    if go_left:
        x_pos -= 3
    # изменение скорости
    if g and current_speed <= 23:
        current_speed += 0.35
    elif current_speed > 23:
        current_speed = 200 / fps
    # вычисление координат
    if jump_flag:
        x_old = x_pos
        y_old = y_pos
        y_pos = jump_coords(y_pos, current_speed)
        current_speed -= 20 / fps
    # проверка нулевого положения
    if y_pos != 790:
        t = False
    else:
        t = True

    screen.fill((0, 0, 0))
    rect_one = pygame.Rect(x_pos, y_pos, 10, 10)
    pygame.draw.rect(screen, (255, 0, 0), rect_one)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 800 - 23 * 20, 20, 23 * 20), 1)
    if g and t:
        rect_prog = pygame.Rect(0, 800 - abs(int(current_speed) * 20), 20, abs(int(current_speed) * 20))
        pygame.draw.rect(screen, (255, 255, 255), rect_prog)
    clock.tick(fps)
    pygame.display.flip()